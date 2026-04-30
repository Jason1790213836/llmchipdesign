"""
Test module information extraction from Verilog code
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.testbench_generator import TestbenchGenerator
from src.llm_client import LLMClient


class TestModuleExtraction(unittest.TestCase):
    """Test Verilog module information extraction."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.llm_client = LLMClient()
        self.tb_gen = TestbenchGenerator(self.llm_client)
    
    def test_simple_mux_extraction(self):
        """Test extraction of simple 2-to-1 mux module info."""
        verilog_code = """module mux2to1 (
    input wire a,
    input wire b,
    input wire sel,
    output wire y
);
    assign y = sel ? b : a;
endmodule"""
        
        module_info = self.tb_gen._extract_module_info(verilog_code)
        
        self.assertEqual(module_info['module_name'], 'mux2to1')
        self.assertEqual(len(module_info['inputs']), 3)
        self.assertEqual(len(module_info['outputs']), 1)
    
    def test_adder_extraction(self):
        """Test extraction of 4-bit adder module info."""
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
        
        module_info = self.tb_gen._extract_module_info(verilog_code)
        
        self.assertEqual(module_info['module_name'], 'adder4bit')
        self.assertGreater(len(module_info['inputs']), 0)
        self.assertGreater(len(module_info['outputs']), 0)
    
    def test_empty_module(self):
        """Test extraction from empty/invalid module."""
        verilog_code = ""
        
        module_info = self.tb_gen._extract_module_info(verilog_code)
        
        self.assertEqual(module_info['module_name'], '')
        self.assertEqual(len(module_info['inputs']), 0)
        self.assertEqual(len(module_info['outputs']), 0)


if __name__ == '__main__':
    unittest.main()
