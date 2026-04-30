#!/usr/bin/env python3
"""
Main CLI for LLM-aided Testbench Generation

Usage:
    python main.py --description <desc_file> --verilog <verilog_file> [options]
    
    Or run with example:
    python main.py --example
"""

import argparse
import sys
import os
from src.testbench_pipeline import TestbenchPipeline
import subprocess

def main():
    parser = argparse.ArgumentParser(
        description='LLM-aided Testbench Generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with custom input files
  python main.py --description examples/input/description.txt --verilog examples/input/module.v
  
  # Run with example files
  python main.py --example
  
  # Specify custom output directory
  python main.py --example --output my_output
  
  # Use specific LLM model
  python main.py --example --model gpt-3.5-turbo
        """
    )
    
    parser.add_argument('--description', '-d', 
                       default='examples/input/mux_description.txt',
                       help='Path to file containing natural language description')
    parser.add_argument('--verilog', '-v', 
                       default='examples/input/mux2to1.v',
                       help='Path to Verilog module file to be tested')
    parser.add_argument('--output', '-o', 
                       default='examples/output',
                       help='Output directory for generated files (default: examples/output)')
    parser.add_argument('--model', '-m',
                       default='gpt-4o',
                       help='LLM model to use (default: gpt-4)')
    parser.add_argument('--provider',
                       default='openai',
                       choices=['openai'],
                       help='LLM provider (default: openai)')
    parser.add_argument('--api-key',
                       default=os.environ.get('TbGeneration'),
                       help='API key for LLM provider (overrides OPENAI_API_KEY env var)')
    parser.add_argument('--example', '-e',
                       action='store_true',
                       help='Run with built-in example')
    
    args = parser.parse_args()
    
    # Determine input source
    if args.example:
        print("Running with example inputs...")
        description = """A 2-to-1 multiplexer (MUX).
The module takes two 1-bit input signals (a and b) and one 1-bit select signal (sel).
When sel is 0, the output y should be equal to input a.
When sel is 1, the output y should be equal to input b.
This is a combinational logic circuit."""
        
        verilog_code = """module mux2to1 (
    input wire a,
    input wire b,
    input wire sel,
    output wire y
);
    assign y = sel ? b : a;
endmodule"""
        
    else:
        # Check if required arguments are provided
        if not args.description or not args.verilog:
            parser.error("--description and --verilog are required when not using --example")
        
        # Read description file
        try:
            with open(args.description, 'r') as f:
                description = f.read()
        except FileNotFoundError:
            print(f"Error: Description file not found: {args.description}")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading description file: {e}")
            sys.exit(1)
        
        # Read Verilog file
        try:
            with open(args.verilog, 'r') as f:
                verilog_code = f.read()
        except FileNotFoundError:
            print(f"Error: Verilog file not found: {args.verilog}")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading Verilog file: {e}")
            sys.exit(1)
    
    # Initialize pipeline
    pipeline = TestbenchPipeline(
        api_key=args.api_key,
        model=args.model,
        provider=args.provider
    )
    
    # Check if LLM is configured
    if not pipeline.llm_client.is_available():
        print("\n" + "=" * 80)
        print("WARNING: LLM API Key Not Configured")
        print("=" * 80)
        print("To use the full LLM-powered generation, set your API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        print("Or use the --api-key option.")
        print("\nContinuing with mock generation for demonstration...")
        print("=" * 80 + "\n")
    
    # Run the pipeline
    try:
        result = pipeline.run(description, verilog_code, args.output)
        print("\n✓ Testbench generation completed successfully!")
        # Step 5: Update testbench with golden outputs
        print("\n[Step 6] iverilog simulation of the final testbench and golden verilog model...")
        iverilog_command = f"iverilog -g2012 -o {args.output}/out.vvp {args.verilog} {args.output}/testbench_final.v"
        print("Testbench Compilation......")
        result = subprocess.run(iverilog_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=120)
        if result.stderr:
            print(f"Compilation error: {result.stderr}")
        else:
            print("Testbench Simulation......")
            result = subprocess.run(f"vvp {args.output}/out.vvp", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=120)
            if result.stdout:
                print(f"result:\n{result.stdout}")
        
        
        return 0
    except Exception as e:
        print(f"\n✗ Error during testbench generation: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    # print(os.environ.get('TbGeneration'))
    sys.exit(main())
