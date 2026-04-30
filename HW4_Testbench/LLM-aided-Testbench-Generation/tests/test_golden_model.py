"""
Test Python golden model execution
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.golden_model_generator import GoldenModelGenerator
from src.llm_client import LLMClient


class TestGoldenModel(unittest.TestCase):
    """Test Python golden model generation and execution."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.llm_client = LLMClient()
        self.golden_gen = GoldenModelGenerator(self.llm_client)
    
    def test_python_code_extraction_with_markers(self):
        """Test extraction of Python code from LLM response with markers."""
        response = """Here's the Python code:

```python
def mux2to1_golden(a, b, sel):
    if sel == 0:
        return {'y': a}
    else:
        return {'y': b}
```

This implements the 2-to-1 mux."""
        
        code = self.golden_gen._extract_python_code(response)
        
        self.assertIn('def mux2to1_golden', code)
        self.assertIn('return', code)
    
    def test_python_code_extraction_without_markers(self):
        """Test extraction of Python code without markdown markers."""
        response = """def simple_func(x):
    return x * 2"""
        
        code = self.golden_gen._extract_python_code(response)
        
        self.assertIn('def simple_func', code)
    
    def test_compute_golden_outputs_simple(self):
        """Test computing golden outputs with a simple function."""
        python_code = """def test_golden(a, b):
    return {'sum': a + b}"""
        
        test_patterns = [
            {'inputs': {'a': 1, 'b': 2}},
            {'inputs': {'a': 3, 'b': 4}},
        ]
        
        module_info = {'module_name': 'test'}
        
        results = self.golden_gen.compute_golden_outputs(
            python_code, test_patterns, module_info
        )
        
        self.assertEqual(len(results), 2)
        if results[0].get('expected_outputs'):
            self.assertEqual(results[0]['expected_outputs']['sum'], 3)
        if results[1].get('expected_outputs'):
            self.assertEqual(results[1]['expected_outputs']['sum'], 7)
    
    def test_compute_golden_outputs_error_handling(self):
        """Test error handling when golden model execution fails."""
        python_code = """def test_golden(a, b):
    raise ValueError("Test error")"""
        
        test_patterns = [
            {'inputs': {'a': 1, 'b': 2}},
        ]
        
        module_info = {'module_name': 'test'}
        
        results = self.golden_gen.compute_golden_outputs(
            python_code, test_patterns, module_info
        )
        
        self.assertEqual(len(results), 1)
        # Should have error recorded
        self.assertIn('error', results[0].keys())


if __name__ == '__main__':
    unittest.main()
