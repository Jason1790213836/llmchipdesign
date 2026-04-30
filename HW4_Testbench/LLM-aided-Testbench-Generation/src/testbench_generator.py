"""
Step 3: Generate testbench with test patterns (without golden outputs).
"""

from typing import Dict, Any, List
from .llm_client import LLMClient


class TestbenchGenerator:
    """Generate Verilog testbench with test patterns using LLM."""
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize testbench generator.
        
        Args:
            llm_client: LLM client instance
        """
        self.llm_client = llm_client
    
    def generate_testbench(self, description: str, verilog_code: str) -> Dict[str, Any]:
        """
        Generate testbench with comprehensive test patterns.
        
        Args:
            description: Natural language description of the Verilog module
            verilog_code: Verilog code to be tested
            
        Returns:
            Dictionary containing:
                - testbench_code: Verilog testbench code (without expected outputs)
                - test_patterns: List of test input patterns
                - module_info: Information about module (name, inputs, outputs)
        """
        # First, extract module information
        module_info = self._extract_module_info(verilog_code)
        
        # Generate comprehensive test patterns
        system_prompt = """You are an expert in Verilog testbench generation. 
Your task is to generate comprehensive test patterns for a given Verilog module.
Generate test patterns that cover:
1. All corner cases
2. Boundary values
3. Typical use cases
4. Edge cases
5. Random values for thorough testing"""

        user_prompt = f"""Given the following Verilog module and its natural language description, 
generate a comprehensive Verilog testbench that includes ALL possible test patterns.

Natural Language Description:
{description}

Verilog Module Code:
{verilog_code}

Generate a Verilog testbench that:
1. Declares all necessary signals
2. Instantiates the module under test
3. Includes a systematic set of test patterns covering all cases
4. Uses $display to show inputs for each test (all $display statements are in the initial block and before $finish statement.)
5. Does NOT include expected outputs or assertions yet (we will add those later)
6. Numbers each test case

Please provide:
1. The complete testbench code
2. A list of test patterns in JSON format with test number and input values

Format your response as:
TESTBENCH_CODE:
```verilog
[testbench code here]
```

TEST_PATTERNS (a list of dictionaries. Each dictionary contains only input signal names mapped to their values as plain binary strings (no prefixes like 0b, no spaces). Do not include any test_number field):
```json
[array of test patterns]
```
"""

        response = self.llm_client.generate(user_prompt, system_prompt, max_tokens=4000)
        
        # Parse the response
        testbench_code = self._extract_section(response, "TESTBENCH_CODE:", "```verilog", "```")
        test_patterns_json = self._extract_section(response, "TEST_PATTERNS:", "```json", "```")
        
        try:
            test_patterns = eval(test_patterns_json) if test_patterns_json else []
        except:
            test_patterns = []
            print("Warning: Could not parse test patterns JSON")
        
        return {
            "testbench_code": testbench_code,
            "test_patterns": test_patterns,
            "module_info": module_info,
            "raw_response": response
        }
    
    def _extract_module_info(self, verilog_code: str) -> Dict[str, Any]:
        """
        Extract module information (name, inputs, outputs) from Verilog code.
        
        Args:
            verilog_code: Verilog module code
            
        Returns:
            Dictionary with module information
        """
        lines = verilog_code.strip().split('\n')
        module_name = ""
        inputs = []
        outputs = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('module'):
                # Extract module name
                parts = line.split()
                if len(parts) >= 2:
                    module_name = parts[1].split('(')[0]
            elif 'input' in line:
                # Extract input signals
                input_part = line.replace('input', '').replace(';', '').replace(',', '').strip()
                if input_part:
                    inputs.append(input_part)
            elif 'output' in line:
                # Extract output signals
                output_part = line.replace('output', '').replace(';', '').replace(',', '').strip()
                if output_part:
                    outputs.append(output_part)
        
        return {
            "module_name": module_name,
            "inputs": inputs,
            "outputs": outputs
        }
    
    def _extract_section(self, text: str, marker: str, start_delim: str, end_delim: str) -> str:
        """
        Extract a section from the LLM response between delimiters.
        
        Args:
            text: Full response text
            marker: Section marker to find
            start_delim: Start delimiter (e.g., "```verilog")
            end_delim: End delimiter (e.g., "```")
            
        Returns:
            Extracted section content
        """
        try:
            # Find the marker
            marker_idx = text.find(marker)
            if marker_idx == -1:
                return ""
            
            # Find the start delimiter after the marker
            start_idx = text.find(start_delim, marker_idx)
            if start_idx == -1:
                return ""
            start_idx += len(start_delim)
            
            # Find the end delimiter
            end_idx = text.find(end_delim, start_idx)
            if end_idx == -1:
                return ""
            
            return text[start_idx:end_idx].strip()
        except Exception as e:
            print(f"Error extracting section: {e}")
            return ""
