import json
import os
import re
import importlib
import argparse
from pathlib import Path
from openai import OpenAI
import run_yosys

importlib.reload(run_yosys)

api_key = os.getenv("OPENAI_API_KEY", "").strip()
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set. Please set a valid key before running.")

client = OpenAI(api_key=api_key)


def extract_all_modules(verilog_code: str):
    return re.findall(r"\bmodule\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", verilog_code)


def choose_top_module(verilog_code: str, baseline_path: str, explicit_top: str = None) -> str:
    modules = extract_all_modules(verilog_code)
    if not modules:
        raise ValueError("Cannot detect any module name from baseline Verilog.")

    if explicit_top:
        if explicit_top not in modules:
            raise ValueError(
                f"Specified --top '{explicit_top}' not found in baseline modules: {modules}"
            )
        return explicit_top

    stem = Path(baseline_path).stem

    if stem in modules:
        return stem

    stem_simplified = re.sub(r"_generated$|_gen$|_baseline$|_top$", "", stem, flags=re.IGNORECASE)
    if stem_simplified in modules:
        return stem_simplified

    return modules[-1]


def get_system_prompt(top_module: str) -> str:
    return f"""You are an expert digital circuit designer.
Your goal is to generate synthesizable Verilog for an 8-bit adder.

Respond with ONLY valid synthesizable Verilog code.
No markdown fences.
No commentary.

Hard constraints:
1. Keep top module name exactly {top_module}.
2. Keep same I/O interface as baseline.
3. Must synthesize successfully in Yosys.
"""


MODE_CONFIG = {
    "area": {
        "delay_limit_ps": 320,
        "description": "Minimize area with relaxed timing."
    },
    "delay": {
        "delay_limit_ps": 220,
        "description": "Minimize delay as primary objective."
    },
    "balanced": {
        "delay_limit_ps": 260,
        "description": "Balance area and delay."
    }
}


def llm_generate(history, top_module, model_name="gpt-4o"):
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "system", "content": get_system_prompt(top_module)}] + history,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def build_feedback_prompt(iteration, ppa, best_ppa, mode, top_module):
    cfg = MODE_CONFIG[mode]
    return f"""Iteration {iteration} synthesis results:

Current candidate:
- cell_count: {ppa['cell_count']}
- delay_ps: {ppa['logic_levels']}
- area_um2: {ppa['area_um2']}

Best so far:
- cell_count: {best_ppa['cell_count']}
- delay_ps: {best_ppa['logic_levels']}
- area_um2: {best_ppa['area_um2']}

Optimization mode: {mode}
Mode intent: {cfg['description']}

Please propose a new 8-bit adder Verilog implementation.

Targets:
- Keep delay_ps <= {cfg['delay_limit_ps']} whenever possible.
- For mode=area: prioritize reducing area_um2.
- For mode=delay: prioritize reducing delay_ps.
- For mode=balanced: reduce area_um2 while also improving delay_ps.

Architectural ideas to explore:
- hybrid CLA + RCA
- carry select grouping
- Brent-Kung style prefix tree
- partial prefix carry logic

Important constraints:
- Top module name must remain exactly {top_module}.
- Keep the same I/O interface as the baseline.

Provide ONLY Verilog code.
"""


def is_better(ppa, best_ppa, mode):
    if ppa["logic_levels"] is None or ppa["area_um2"] is None or ppa["cell_count"] is None:
        return False

    if mode == "area":
        return (
            ppa["logic_levels"] <= MODE_CONFIG[mode]["delay_limit_ps"]
            and (
                ppa["area_um2"] < best_ppa["area_um2"]
                or (
                    ppa["area_um2"] == best_ppa["area_um2"]
                    and ppa["cell_count"] < best_ppa["cell_count"]
                )
            )
        )

    if mode == "delay":
        return (
            ppa["logic_levels"] < best_ppa["logic_levels"]
            or (
                ppa["logic_levels"] == best_ppa["logic_levels"]
                and ppa["area_um2"] < best_ppa["area_um2"]
            )
        )

    if mode == "balanced":
        return (
            ppa["logic_levels"] <= MODE_CONFIG[mode]["delay_limit_ps"]
            and (
                (ppa["area_um2"] + 0.05 * ppa["logic_levels"])
                < (best_ppa["area_um2"] + 0.05 * best_ppa["logic_levels"])
            )
        )

    return False


def run_loop(baseline_verilog, out_dir, top, max_iter=10, mode="area", model_name="gpt-4o"):
    history = []
    results = []

    best_ppa = {
        "cell_count": 10**9,
        "logic_levels": 10**9,
        "area_um2": 10**9,
    }
    best_code = baseline_verilog

    history.append({
        "role": "user",
        "content": (
            f"Here is the baseline 8-bit adder Verilog.\n{baseline_verilog}\n"
            f"Optimization mode is '{mode}'. Start from this design. "
            "Your first proposal may be identical."
        )
    })

    for i in range(1, max_iter + 1):
        print(f"\n=== Iteration {i} ({mode}) ===")

        verilog = llm_generate(history, top, model_name=model_name)

        if not re.search(rf"\bmodule\s+{re.escape(top)}\s*\(", verilog):
            print(f"Invalid candidate: top module is not {top}")
            history.append({"role": "assistant", "content": verilog})
            history.append({
                "role": "user",
                "content": (
                    f"Your last output used the wrong top module name. "
                    f"Top module MUST be exactly module {top}."
                )
            })
            continue

        fname = out_dir / f"{mode}_candidate_{i}.v"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(verilog)

        try:
            ppa = run_yosys.synthesize(str(fname), top)
        except Exception as e:
            print(f"Synthesis failed: {e}")
            history.append({"role": "assistant", "content": verilog})
            history.append({
                "role": "user",
                "content": (
                    "Synthesis failed. Likely invalid Verilog, wrong module name, "
                    "or interface mismatch. Fix and resubmit."
                )
            })
            continue

        area_str = f"{ppa['area_um2']:.3f}" if ppa["area_um2"] is not None else "None"

        print(
            f"Cells: {ppa['cell_count']} | "
            f"Delay(ps): {ppa['logic_levels']} | "
            f"Area: {area_str} um^2"
        )

        results.append({
            "iteration": i,
            "ppa": ppa,
            "file": str(fname)
        })

        if is_better(ppa, best_ppa, mode):
            best_ppa = ppa
            best_code = verilog
            print("*** New best! ***")

        history.append({"role": "assistant", "content": verilog})
        history.append({
            "role": "user",
            "content": build_feedback_prompt(i, ppa, best_ppa, mode, top)
        })

    return best_code, best_ppa, results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=str, required=True, help="Path to starting architecture Verilog")
    parser.add_argument("--top", type=str, default=None, help="Optional explicit top module name")
    parser.add_argument("--mode", choices=["area", "delay", "balanced"], required=True)
    parser.add_argument("--out", type=str, required=True, help="Output directory")
    parser.add_argument("--max_iter", type=int, default=10)
    parser.add_argument("--model", type=str, default="gpt-4o")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(args.baseline, "r", encoding="utf-8") as f:
        baseline = f.read()

    top_module = choose_top_module(baseline, args.baseline, args.top)
    print(f"Detected top module: {top_module}")
    print(f"All modules found: {extract_all_modules(baseline)}")

    baseline_check = run_yosys.synthesize(args.baseline, top_module)
    print("Baseline PPA check:", baseline_check)

    best_v, best_ppa, log = run_loop(
        baseline_verilog=baseline,
        out_dir=out_dir,
        top=top_module,
        max_iter=args.max_iter,
        mode=args.mode,
        model_name=args.model
    )

    with open(out_dir / "best_adder.v", "w", encoding="utf-8") as f:
        f.write(best_v)

    with open(out_dir / "optimization_log.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "baseline": args.baseline,
                "top_module": top_module,
                "mode": args.mode,
                "best_ppa": best_ppa,
                "iterations": log
            },
            f,
            indent=2
        )

    print(f"\nBest ({args.mode}): {best_ppa}")