import subprocess, re, json, sys

def synthesize(verilog_file, top_module, lib_file='nangate45.lib'):
    script = f"""
read_verilog {verilog_file}
hierarchy -check -top {top_module}
flatten
proc; opt; fsm; opt; memory; opt
techmap; opt
dfflibmap -liberty {lib_file}
abc -liberty {lib_file} -script abc.script
clean
stat -top {top_module} -liberty {lib_file}
"""

    with open("tmp_synth.ys", "w") as f:
        f.write(script)

    result = subprocess.run(
        ['yosys', '-s', 'tmp_synth.ys'],
        capture_output=True,
        text=True
    )

    log = result.stdout + "\n" + result.stderr
    print(log)
    return parse_stats(log)

def parse_stats(log):
    ppa = {}

    m = re.search(r'Chip area for module .*?:\s*([\d.]+)', log)
    ppa['area_um2'] = float(m.group(1)) if m else None

    m = re.search(r'Number of cells:\s*(\d+)', log)
    ppa['cell_count'] = int(m.group(1)) if m else None

    m = re.search(r'Delay =\s*([\d.]+)\s*ps', log)
    ppa['logic_levels'] = float(m.group(1)) if m else None

    return ppa

if __name__ == '__main__':
    ppa = synthesize(sys.argv[1], sys.argv[2])
    print(json.dumps(ppa, indent=2))