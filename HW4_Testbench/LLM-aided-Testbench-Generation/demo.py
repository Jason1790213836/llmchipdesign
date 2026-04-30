#!/usr/bin/env python3
"""
Demo script showcasing LLM-aided Testbench Generation capabilities.

This script demonstrates the complete workflow with example modules.
"""

import sys
import os
from src.testbench_pipeline import TestbenchPipeline


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80 + "\n")


def demo_mux():
    """Demonstrate testbench generation for a 2-to-1 MUX."""
    print_section("DEMO 1: 2-to-1 Multiplexer")
    
    description = """A 2-to-1 multiplexer (MUX).

The module takes two 1-bit input signals (a and b) and one 1-bit select signal (sel).

Functionality:
- Input 'a': First data input (1-bit)
- Input 'b': Second data input (1-bit)
- Input 'sel': Select signal (1-bit)
- Output 'y': Selected output (1-bit)

When sel is 0, the output y should be equal to input a.
When sel is 1, the output y should be equal to input b.

This is a combinational logic circuit with no state or memory."""

    verilog_code = """module mux2to1 (
    input wire a,
    input wire b,
    input wire sel,
    output wire y
);
    assign y = sel ? b : a;
endmodule"""

    print("Natural Language Description:")
    print("-" * 80)
    print(description)
    print("\n")
    
    print("Verilog Code:")
    print("-" * 80)
    print(verilog_code)
    print("\n")
    
    # Run pipeline
    pipeline = TestbenchPipeline()
    result = pipeline.run(description, verilog_code, "demo_output/mux")
    
    return result


def demo_adder():
    """Demonstrate testbench generation for a 4-bit adder."""
    print_section("DEMO 2: 4-bit Adder")
    
    description = """A simple 4-bit adder module.

The module takes two 4-bit input signals (a and b) and produces a 4-bit sum output and a 1-bit carry output.

Functionality:
- Input 'a': 4-bit unsigned number
- Input 'b': 4-bit unsigned number  
- Output 'sum': 4-bit result of a + b (lower 4 bits)
- Output 'carry': 1-bit carry-out flag (set to 1 if result exceeds 15)

The adder performs unsigned addition of the two 4-bit inputs.
If the result is greater than 15 (0xF), the carry output should be set to 1."""

    verilog_code = """module adder4bit (
    input wire [3:0] a,
    input wire [3:0] b,
    output wire [3:0] sum,
    output wire carry
);
    wire [4:0] result;
    assign result = a + b;
    assign sum = result[3:0];
    assign carry = result[4];
endmodule"""

    print("Natural Language Description:")
    print("-" * 80)
    print(description)
    print("\n")
    
    print("Verilog Code:")
    print("-" * 80)
    print(verilog_code)
    print("\n")
    
    # Run pipeline
    pipeline = TestbenchPipeline()
    result = pipeline.run(description, verilog_code, "demo_output/adder")
    
    return result


def main():
    """Run all demos."""
    print("\n" + "█" * 80)
    print(" " * 20 + "LLM-AIDED TESTBENCH GENERATION DEMO")
    print("█" * 80)
    
    print("\nThis demo showcases the 5-step automated testbench generation process:")
    print("  Step 1-2: Accept natural language description and Verilog code")
    print("  Step 3:   Generate testbench with comprehensive test patterns")
    print("  Step 4:   Create Python golden model and compute expected outputs")
    print("  Step 5:   Update testbench with verification logic")
    
    # Check if LLM is configured
    from src.llm_client import LLMClient
    llm = LLMClient()
    if not llm.is_available():
        print("\n" + "!" * 80)
        print("NOTE: Running in DEMO MODE without LLM")
        print("!" * 80)
        print("\nFor full LLM-powered generation, set your API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        print("\nThe demo will still show the complete workflow with mock generation.")
        input("\nPress Enter to continue...")
    
    # Run demos
    try:
        demo_mux()
        print("\n" + "✓" * 80)
        print("Demo 1 completed successfully!")
        print("✓" * 80)
        
        input("\nPress Enter to run Demo 2...")
        
        demo_adder()
        print("\n" + "✓" * 80)
        print("Demo 2 completed successfully!")
        print("✓" * 80)
        
        print_section("DEMO COMPLETE")
        print("Generated testbenches are available in:")
        print("  - demo_output/mux/")
        print("  - demo_output/adder/")
        print("\nYou can simulate these testbenches using:")
        print("  iverilog -o sim <module.v> <testbench_final.v>")
        print("  vvp sim")
        print("\nThank you for trying LLM-aided Testbench Generation!")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
