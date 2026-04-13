"""
Integration test for the complete pipeline
"""

import unittest
import sys
import os
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.testbench_pipeline import TestbenchPipeline


class TestPipeline(unittest.TestCase):
    """Integration tests for the complete pipeline."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pipeline = TestbenchPipeline()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_pipeline_runs_without_llm(self):
        """Test that pipeline runs in mock mode without LLM."""
        description = "A simple AND gate with two 1-bit inputs."
        verilog_code = """module and_gate (
    input wire a,
    input wire b,
    output wire y
);
    assign y = a & b;
endmodule"""
        
        result = self.pipeline.run(description, verilog_code, self.temp_dir)
        
        # Check that result contains expected keys
        self.assertIn('description', result)
        self.assertIn('verilog_code', result)
        self.assertIn('module_info', result)
        self.assertIn('initial_testbench', result)
        self.assertIn('python_golden_model', result)
        self.assertIn('final_testbench', result)
        
        # Check that output files were created
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'testbench_initial.v')))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'golden_model.py')))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'test_patterns_with_golden.json')))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'testbench_final.v')))
    
    def test_pipeline_with_mux_example(self):
        """Test pipeline with 2-to-1 MUX example."""
        description = """A 2-to-1 multiplexer.
Input a: 1-bit data input
Input b: 1-bit data input  
Input sel: 1-bit select signal
Output y: Selected output (a when sel=0, b when sel=1)"""
        
        verilog_code = """module mux2to1 (
    input wire a,
    input wire b,
    input wire sel,
    output wire y
);
    assign y = sel ? b : a;
endmodule"""
        
        result = self.pipeline.run(description, verilog_code, self.temp_dir)
        
        # Verify module info exists (in mock mode it may be 'unknown')
        self.assertIn('module_name', result['module_info'])
        
        # Verify output directory structure
        output_files = os.listdir(self.temp_dir)
        self.assertIn('testbench_initial.v', output_files)
        self.assertIn('golden_model.py', output_files)
        self.assertIn('testbench_final.v', output_files)


if __name__ == '__main__':
    unittest.main()
