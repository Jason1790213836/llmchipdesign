# LLM-aided Testbench Generation

An automated testbench generation system that leverages Large Language Models (LLMs) to create comprehensive Verilog testbenches with golden reference outputs.

## Overview

This project automates the creation of Verilog testbenches by:
1. Accepting a natural language description of a Verilog module
2. Taking the Verilog code to be tested (which may contain bugs)
3. Generating a comprehensive testbench with all possible test patterns using LLM
4. Creating a Python golden reference model from the natural language description
5. Computing expected outputs by running test patterns through the Python model
6. Updating the testbench with verification logic and expected outputs

## Features

✨ **5-Step Automated Pipeline:**
- **Step 1-2**: Input handling (natural language description + Verilog code)
- **Step 3**: LLM-generated testbench with comprehensive test patterns
- **Step 4**: Python golden model generation and golden output computation
- **Step 5**: Testbench enhancement with verification logic

🎯 **Comprehensive Testing:**
- Corner cases and boundary values
- Typical use cases
- Edge cases
- Random test patterns

🔍 **Verification Features:**
- Automatic pass/fail checking
- Test summary reporting
- Detailed output comparison

## Project Structure

```
LLM-aided-Testbench-Generation/
├── src/
│   ├── __init__.py                 # Package initialization
│   ├── llm_client.py               # LLM API client
│   ├── testbench_generator.py     # Step 3: Generate testbench with patterns
│   ├── golden_model_generator.py  # Step 4: Python golden model generation
│   ├── testbench_updater.py       # Step 5: Add verification logic
│   └── testbench_pipeline.py      # Main orchestrator
├── examples/
│   ├── input/                      # Example input files
│   │   ├── description.txt         # Natural language description
│   │   ├── adder4bit.v            # Example Verilog module
│   │   ├── mux_description.txt    # MUX description
│   │   └── mux2to1.v              # MUX Verilog module
│   └── output/                     # Generated outputs (created at runtime)
├── main.py                         # CLI entry point
├── requirements.txt                # Python dependencies
├── config.yaml                     # Configuration file
└── README.md                       # This file
```

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/FCHXWH823/LLM-aided-Testbench-Generation.git
cd LLM-aided-Testbench-Generation
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up API key (for LLM-powered generation):**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or use the `--api-key` command line option.

## Usage

### Quick Start with Example

Run the tool with the built-in example:

```bash
python main.py --example
```

This will generate a testbench for a 2-to-1 multiplexer and save outputs to `examples/output/`.

### Custom Input Files

Use your own Verilog module and description:

```bash
python main.py --description examples/input/description.txt \
               --verilog examples/input/adder4bit.v \
               --output my_output
```

### Command Line Options

```
usage: main.py [-h] [--description DESCRIPTION] [--verilog VERILOG]
               [--output OUTPUT] [--model MODEL] [--provider {openai}]
               [--api-key API_KEY] [--example]

Options:
  -h, --help            Show help message
  -d, --description     Path to natural language description file
  -v, --verilog         Path to Verilog module file
  -o, --output          Output directory (default: examples/output)
  -m, --model           LLM model to use (default: gpt-4)
  --provider            LLM provider (default: openai)
  --api-key             API key (overrides environment variable)
  -e, --example         Run with built-in example
```

## Example Workflow

### Input Files

**Natural Language Description** (`description.txt`):
```
A 2-to-1 multiplexer (MUX).
The module takes two 1-bit input signals (a and b) and one 1-bit select signal (sel).
When sel is 0, the output y should be equal to input a.
When sel is 1, the output y should be equal to input b.
```

**Verilog Module** (`mux2to1.v`):
```verilog
module mux2to1 (
    input wire a,
    input wire b,
    input wire sel,
    output wire y
);
    assign y = sel ? b : a;
endmodule
```

### Generated Outputs

The tool generates four main files:

1. **`testbench_initial.v`**: Initial testbench with test patterns (no verification)
2. **`golden_model.py`**: Python reference implementation
3. **`test_patterns_with_golden.json`**: Test patterns with expected outputs
4. **`testbench_final.v`**: Complete testbench with verification logic

### Running the Generated Testbench

To simulate the generated testbench with a Verilog simulator:

```bash
# Using Icarus Verilog
iverilog -o sim examples/input/mux2to1.v examples/output/testbench_final.v
vvp sim

# Using ModelSim
vlog examples/input/mux2to1.v examples/output/testbench_final.v
vsim -c work.testbench -do "run -all; quit"
```

## Pipeline Details

### Step 3: Testbench Generation
- Analyzes the Verilog module structure
- Generates comprehensive test patterns covering:
  - Corner cases (all 0s, all 1s)
  - Boundary values
  - Typical cases
  - Random values
- Creates testbench skeleton with test pattern application

### Step 4: Golden Model Generation
- Converts natural language description to Python code
- Implements the expected functionality
- Runs all test patterns through the Python model
- Captures expected outputs for each test case

### Step 5: Testbench Update
- Injects verification logic into the testbench
- Adds expected output comparisons
- Implements pass/fail tracking
- Generates test summary report

## Configuration

Edit `config.yaml` to customize:

```yaml
llm:
  provider: "openai"
  model: "gpt-4"
  temperature: 0.3
  max_tokens: 4000

generation:
  output_dir: "examples/output"
  save_intermediate: true

testbench:
  include_summary: true
  verbose_output: true
```

## Requirements

- Python 3.7+
- OpenAI API access (or compatible LLM provider)
- (Optional) Verilog simulator for testing generated testbenches

## Supported LLM Providers

Currently supported:
- OpenAI (GPT-4, GPT-3.5-turbo, etc.)

Future support planned:
- Anthropic Claude
- Other OpenAI-compatible APIs

## Troubleshooting

### LLM API Key Not Configured

If you see a warning about missing API key:
```
WARNING: LLM API Key Not Configured
```

Set your API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or use the `--api-key` option:
```bash
python main.py --example --api-key your-api-key-here
```

### Module Information Extraction Issues

If the tool has trouble extracting module information, ensure your Verilog code follows standard formatting:
```verilog
module module_name (
    input wire signal_name,
    output wire signal_name
);
```

## Contributing

Contributions are welcome! Areas for improvement:
- Additional LLM provider support
- Enhanced test pattern generation strategies
- Support for sequential circuits and FSMs
- Waveform generation and analysis

## License

This project is open source. Please check the repository for license details.

## Acknowledgments

This project demonstrates the power of LLMs in hardware verification and testbench generation.
