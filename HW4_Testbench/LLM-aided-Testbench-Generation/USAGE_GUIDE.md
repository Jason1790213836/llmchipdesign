# Usage Guide: LLM-aided Testbench Generation

This guide provides detailed instructions on how to use the LLM-aided Testbench Generation tool effectively.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Step-by-Step Workflow](#step-by-step-workflow)
3. [Input File Formats](#input-file-formats)
4. [Output Files](#output-files)
5. [Advanced Usage](#advanced-usage)
6. [Troubleshooting](#troubleshooting)

## Quick Start

### Running with Built-in Example

The fastest way to see the tool in action:

```bash
python main.py --example
```

This uses the built-in 2-to-1 multiplexer example and generates all output files in `examples/output/`.

### Running with Your Own Verilog Module

```bash
python main.py \
    --description examples/input/mux_description.txt \
    --verilog examples/input/mux2to1.v \
    --output my_output
```

## Step-by-Step Workflow

### Step 1: Prepare Your Input Files

You need two input files:

1. **Natural Language Description**: A text file describing what your Verilog module should do
2. **Verilog Module Code**: The actual Verilog code to be tested

Example description file (`my_module_desc.txt`):
```
A simple AND gate.
The module takes two 1-bit inputs (a and b) and produces one 1-bit output (y).
The output y should be 1 only when both inputs a and b are 1.
Otherwise, the output should be 0.
```

Example Verilog file (`and_gate.v`):
```verilog
module and_gate (
    input wire a,
    input wire b,
    output wire y
);
    assign y = a & b;
endmodule
```

### Step 2: Configure API Key (Optional but Recommended)

For full LLM-powered generation, set your OpenAI API key:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or provide it via command line:

```bash
python main.py --api-key your-api-key-here --example
```

**Note:** Without an API key, the tool runs in mock mode for demonstration purposes.

### Step 3: Run the Tool

```bash
python main.py \
    --description my_module_desc.txt \
    --verilog and_gate.v \
    --output my_testbench_output
```

### Step 4: Review Generated Files

The tool creates four main files in your output directory:

```
my_testbench_output/
├── testbench_initial.v              # Initial testbench (patterns only)
├── golden_model.py                  # Python reference model
├── test_patterns_with_golden.json   # Test data with expected outputs
└── testbench_final.v                # Complete testbench with verification
```

### Step 5: Simulate the Testbench

Use your preferred Verilog simulator to run the generated testbench:

**Using Icarus Verilog:**
```bash
iverilog -o simulation and_gate.v my_testbench_output/testbench_final.v
vvp simulation
```

**Using ModelSim:**
```bash
vlog and_gate.v my_testbench_output/testbench_final.v
vsim -c work.testbench -do "run -all; quit"
```

## Input File Formats

### Natural Language Description

The description should clearly explain:
- What the module does
- Input signal names and their purpose
- Output signal names and their purpose
- Expected behavior for different input conditions

**Good Example:**
```
A 4-bit adder module.
Inputs:
  - a: 4-bit unsigned number
  - b: 4-bit unsigned number
Outputs:
  - sum: 4-bit sum of a and b
  - carry: 1-bit carry output

The module adds two 4-bit unsigned numbers.
If the sum exceeds 15, the carry bit should be set to 1.
```

**Poor Example:**
```
An adder.
```
(Too vague - doesn't specify bit widths or expected behavior)

### Verilog Module Code

Your Verilog code should:
- Follow standard Verilog syntax
- Clearly declare inputs and outputs
- Be properly formatted with consistent indentation

**Supported:**
```verilog
module my_module (
    input wire [3:0] a,
    input wire [3:0] b,
    output wire [3:0] sum,
    output wire carry
);
    // module implementation
endmodule
```

**Note:** The tool works best with combinational logic. Sequential circuits and FSMs are supported but may require additional verification.

## Output Files

### 1. testbench_initial.v

This is the first-stage testbench containing:
- Signal declarations
- Module instantiation
- Test pattern application
- Basic $display statements

**Does NOT contain:**
- Expected output values
- Pass/fail verification
- Assertions

### 2. golden_model.py

A Python implementation of the module's functionality based on the natural language description.

Example:
```python
def mux2to1_golden(a, b, sel):
    """
    Golden model for 2-to-1 multiplexer.
    """
    if sel == 0:
        return {'y': a}
    else:
        return {'y': b}
```

You can run this independently to verify behavior:
```bash
python -c "from golden_model import mux2to1_golden; print(mux2to1_golden(1, 0, 1))"
```

### 3. test_patterns_with_golden.json

JSON file containing all test cases with their expected outputs:

```json
[
  {
    "test_num": 1,
    "inputs": {"a": 0, "b": 0, "sel": 0},
    "expected_outputs": {"y": 0}
  },
  {
    "test_num": 2,
    "inputs": {"a": 1, "b": 0, "sel": 0},
    "expected_outputs": {"y": 1}
  }
]
```

### 4. testbench_final.v

The complete testbench with:
- All features from testbench_initial.v
- Expected output values for each test
- Automatic pass/fail checking
- Test summary at the end

When simulated, it produces output like:
```
Test 1: a=0, b=0, sel=0
  ✓ y = 0 (expected: 0)
Test 2: a=1, b=0, sel=0
  ✓ y = 1 (expected: 1)
...
========== Test Summary ==========
Total Tests: 8
Passed: 8
Failed: 0
==================================
```

## Advanced Usage

### Using Different LLM Models

Specify a different model (e.g., GPT-3.5-turbo for faster/cheaper generation):

```bash
python main.py --example --model gpt-3.5-turbo
```

### Custom Output Directory

Organize outputs by module name:

```bash
python main.py \
    --description my_desc.txt \
    --verilog my_module.v \
    --output outputs/my_module_testbenches
```

### Batch Processing Multiple Modules

Create a shell script to process multiple modules:

```bash
#!/bin/bash
for module in module1 module2 module3; do
    python main.py \
        --description inputs/${module}_desc.txt \
        --verilog inputs/${module}.v \
        --output outputs/${module}
done
```

## Troubleshooting

### Issue: "No OpenAI API key provided"

**Solution:** Set the environment variable or use --api-key:
```bash
export OPENAI_API_KEY='your-key'
# or
python main.py --api-key your-key --example
```

### Issue: Module information not extracted correctly

**Problem:** The tool shows "Module: unknown" or missing inputs/outputs.

**Solution:** Ensure your Verilog code follows standard formatting:
- Use `input wire` and `output wire` declarations
- Put each port declaration on its own line or separate with commas
- Avoid complex port declarations in the module header

### Issue: Python golden model doesn't execute correctly

**Problem:** Error computing golden outputs.

**Causes:**
1. Natural language description is ambiguous
2. Generated Python code has syntax errors
3. Input/output signal names don't match

**Solution:**
1. Provide a clearer, more detailed description
2. Manually review and fix the generated Python code in `golden_model.py`
3. Re-run just step 4-5 with the corrected Python code

### Issue: Testbench doesn't compile in simulator

**Problem:** Verilog syntax errors in generated testbench.

**Solution:**
1. Check for bit width mismatches
2. Verify signal declarations match your module
3. Manually edit the testbench if needed
4. Report issues to improve the generator

### Issue: All tests fail even though module is correct

**Problem:** The golden model might be incorrect.

**Solution:**
1. Review the natural language description for accuracy
2. Manually verify the Python golden model
3. Run individual test cases to identify discrepancies
4. Correct the golden model and regenerate step 5

## Best Practices

1. **Write Clear Descriptions:** The quality of generated testbenches depends heavily on the clarity of your natural language description.

2. **Start Simple:** Begin with simple combinational modules to understand the tool's behavior before moving to complex designs.

3. **Verify the Golden Model:** Always review the generated Python code to ensure it matches your expectations.

4. **Iterate if Needed:** If results aren't perfect, refine your description and regenerate.

5. **Use Version Control:** Keep your input files and generated outputs in version control for traceability.

6. **Review Generated Tests:** Check that the test patterns cover all important cases for your module.

## Examples

### Example 1: Simple Logic Gate

**Description:**
```
An OR gate with two 1-bit inputs a and b, and one 1-bit output y.
Output y is 1 when at least one input is 1, otherwise 0.
```

**Command:**
```bash
python main.py --description or_gate_desc.txt --verilog or_gate.v
```

### Example 2: Arithmetic Module

**Description:**
```
A 4-bit unsigned subtractor.
Inputs: a (4-bit), b (4-bit)
Outputs: diff (4-bit), borrow (1-bit)
Computes diff = a - b.
If a < b, borrow is set to 1.
```

**Command:**
```bash
python main.py --description subtractor_desc.txt --verilog subtractor.v
```

## Getting Help

- Check the main README.md for installation and setup
- Review examples in the `examples/input/` directory
- Run `python main.py --help` for command-line options

## Conclusion

This tool automates the tedious process of writing comprehensive testbenches, allowing you to focus on design and verification. By combining LLM intelligence with systematic testing, you can quickly generate high-quality testbenches for your Verilog modules.
