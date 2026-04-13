# Final Project Report: LLM-Based Hardware Design Experience

This report summarizes the experience of using Large Language Models (LLMs) for automated hardware design generation, optimization, and verification in this project. The evaluation focuses on design quality, correctness, testbench generation, limitations, and best practices discovered during iterative optimization of 8-bit adders.

---

## 1. Experience with LLM-Based Hardware Design

In this project, LLMs were used as iterative hardware design assistants to generate synthesizable Verilog implementations of 8-bit adders under different optimization objectives:

* **Area minimization**
* **Delay minimization**
* **Balanced area-delay tradeoff**

### Iterative Workflow
The workflow consisted of the following stages:
1.  Providing baseline architectures (`RCA8`, `CLA8`, `KSA8`).
2.  Running iterative LLM-guided redesign loops.
3.  Synthesizing each candidate using **Yosys**.
4.  Evaluating **PPA metrics**:
    * Cell count
    * Logic delay
    * Area (µm²)
5.  Feeding synthesis feedback back into the LLM.

### Observed Benefits
LLMs demonstrated a strong ability in:
* ✅ **Speed:** Generating syntactically correct Verilog quickly.
* ✅ **Diversity:** Proposing structurally diverse architectures.
* ✅ **Exploration:** Exploring alternative carry strategies including Ripple carry, Carry lookahead, Carry-select hybrids, and Prefix-inspired carry logic.

### Example Successes
The LLM successfully discovered:
* **RCA-derived:** Balanced optimized ripple structure.
* **CLA-derived:** Delay-optimized hybrid CSA-like structure.
> These optimized architectures significantly improved PPA relative to baseline designs.

---

## 2. Accuracy and Limitations of LLM-Generated Code

### Accuracy Strengths
Most generated Verilog designs were:
* ✅ Synthesizable in **Yosys**.
* ✅ Structurally valid and compatible with module interfaces.
* ✅ Often functionally correct after equivalence checking.

### Common Limitations Observed

#### (1) Repetitive Convergence / Local Optimum Locking
In many runs (especially CLA delay mode), the process often reached the best design by Iteration 2, with later iterations repeating identical architectures.
```text
Example: CLA delay run repeatedly returned:
31 cells / 175.57 delay / 52.668 µm²
```

#### (2) False “Optimized” Candidates
Occasionally, the LLM generated suspiciously tiny designs that were not true adders.

```bash
// Example of a "Fake" Adder implementation
assign sum = a ^ b; 
assign cout = 0;
```
- Cause: LLM generated incomplete logic which synthesized successfully but failed equivalence checking.

#### (3) Misleading Architectural Labels
LLMs often labeled ripple carry chains as "prefix tree" or "carry-select style" even when the actual logic remained RCA-like.

#### (4) Mixed Structural Style Inconsistency
Some designs mixed different coding styles, such as using one FA (Full Adder) instance while the remaining bits used assign logic, resulting in inconsistent RTL.

### 3. Quality of LLM-Generated Testbenches
##### Strengths
Generated testbenches usually included a comprehensive PASS/FAIL reporting format and covered:

- Zero input: 00 + 00
- Simple arithmetic: 01 + 01
- Carry chain stress: 0F + 01
- Overflow boundary: FF + 01, FF + FF

#### Weaknesses
- Limited Randomization: Rarely included random test vectors or exhaustive loops.
- Missing Self-Checking: Some lacked if (actual != expected) logic, relying only on waveform display.
- Timing Mistakes: Occasional race conditions or missing #delay before checking outputs.

Overall Assessment: Rating: Good but requires human review.

### 4. Lessons Learned and Best Practices
### Lesson 1: Always Run Equivalence Checking
Synthesis success alone is NOT enough. A required verification pipeline must include:
LLM Candidate → Yosys Synthesis → Functional Simulation → Equivalence Checking.

### Lesson 2: Use Multi-Start Exploration
Single baseline optimization converged too early. A better strategy involves:

RCA8 → Area/Balanced

CLA8 → Delay

### Lesson 3: Prompt Diversity Matters
Low "temperature" settings caused repetitive architectures. Use explicit prompts like:

Plaintext
"Do not repeat prior CLA structure. Generate a structurally distinct carry architecture."
### Lesson 4: Detect Duplicate Architectures
Reject repeated candidates automatically to save synthesis time.

### Lesson 5: Bit-Width Impact
At 8 bits, architectural advantages (like KSA vs RCA) are modest. Larger adders (32/64-bit) would better expose performance differences.

### 5. Recommendations for Using LLMs in Hardware Design
Recommended Use Cases
✅ RTL prototyping and architectural brainstorming.

✅ Alternative microarchitecture generation.

✅ Testbench scaffolding and Design-space exploration.

Not Recommended Without Human Oversight
❌ Final signoff RTL or safety-critical hardware.

❌ Formal correctness guarantees.

Recommended Workflow
Human architect defines constraints.

LLM proposes candidates.

Automated synthesis + formal verification.

Human reviews selected finalists.

### 6. Final Conclusion
This project demonstrated that LLMs can significantly accelerate hardware design iteration. While they struggle with functional correctness guarantees and local optima, they are powerful co-design tools.

Final Project Outcome Summary
Both optimized final adders achieved:

✅ Functional simulation pass

✅ Equivalence verification pass

✅ Improved PPA over baseline designs

Final Assessment: LLM-assisted hardware optimization is practical, valuable, and promising for future EDA workflows, provided human verification remains a core part of the loop.