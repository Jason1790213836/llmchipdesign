"""
Step 4: Generate Python golden model and compute golden outputs.
"""

import sys
import io
import json
from typing import Dict, Any, List
from .llm_client import LLMClient


class GoldenModelGenerator:
    """Generate Python golden model and compute expected outputs."""
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize golden model generator.
        
        Args:
            llm_client: LLM client instance
        """
        self.llm_client = llm_client
    
    def generate_python_model(self, description: str, module_info: Dict[str, Any]) -> str:
        """
        Generate Python implementation based on natural language description.
        
        Args:
            description: Natural language description of the module
            module_info: Module information (name, inputs, outputs)
            
        Returns:
            Python code implementing the module functionality
        """
        system_prompt = """You are an expert in hardware design and Python programming.
Your task is to create a Python function that implements the exact same functionality
as described in the natural language specification."""

        user_prompt = f"""Given the following natural language description of a hardware module,
create a Python function that implements this functionality.

Natural Language Description:
{description}

Module Information:
- Module Name: {module_info.get('module_name', 'unknown')}
- Inputs: {module_info.get('inputs', [])}
- Outputs: {module_info.get('outputs', [])}

Create a Python function named '{module_info.get('module_name', 'module')}_golden' that:
1. Takes the input signals as parameters
2. Computes and returns the output signals
3. Implements the exact functionality described
4. Handles all edge cases properly
5. Returns outputs as a dictionary with output signal names as keys

Provide ONLY the Python function code, no explanations.
Start with 'def {module_info.get('module_name', 'module')}_golden(' and include complete implementation.
"""

        response = self.llm_client.generate(user_prompt, system_prompt, temperature=0.2, max_tokens=3000)
        
        # Extract Python code
        python_code = self._extract_python_code(response)
        
        return python_code
    
    def compute_golden_outputs(self, python_code: str, test_patterns: List[Dict[str, Any]], 
                               module_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Execute the Python golden model with test patterns to get expected outputs.
        
        Args:
            python_code: Python golden model code
            test_patterns: List of test input patterns
            module_info: Module information
            
        Returns:
            List of test patterns with golden outputs added
        """
        results = []
        
        # Execute the Python code in a safe namespace
        namespace = {}
        try:
            exec(python_code, namespace)
        except Exception as e:
            print(f"Error executing Python code: {e}")
            return results
        
        # Find the golden function
        function_name = f"{module_info.get('module_name', 'module')}_golden"
        golden_func = namespace.get(function_name)
        
        if not golden_func:
            print(f"Error: Could not find function {function_name}")
            return results
        
        # Run each test pattern through the golden model
        for pattern in test_patterns:
            try:
                # Extract input values from the pattern
                inputs = pattern.get('inputs', pattern)
                
                # Call the golden function
                if isinstance(inputs, dict):
                    outputs = golden_func(**inputs)
                else:
                    # If inputs is not a dict, try to call with positional args
                    outputs = golden_func(*inputs.values()) if hasattr(inputs, 'values') else golden_func(inputs)
                
                # Add outputs to the pattern
                result = pattern.copy()
                result['expected_outputs'] = outputs
                results.append(result)
            except Exception as e:
                print(f"Error computing golden output for pattern {pattern}: {e}")
                result = pattern.copy()
                result['expected_outputs'] = None
                result['error'] = str(e)
                results.append(result)
        
        return results
    
    def _extract_python_code(self, text: str) -> str:
        """
        Extract Python code from LLM response.
        
        Args:
            text: LLM response text
            
        Returns:
            Extracted Python code
        """
        # Try to find code between ```python and ```
        if "```python" in text:
            start = text.find("```python") + len("```python")
            end = text.find("```", start)
            if end != -1:
                return text[start:end].strip()
        
        # Try to find code between ``` and ```
        if "```" in text:
            parts = text.split("```")
            if len(parts) >= 3:
                return parts[1].strip()
        
        # If no code blocks found, look for def statement
        if "def " in text:
            lines = text.split('\n')
            code_lines = []
            in_function = False
            for line in lines:
                if line.strip().startswith('def '):
                    in_function = True
                if in_function:
                    code_lines.append(line)
            return '\n'.join(code_lines)
        
        return text.strip()
