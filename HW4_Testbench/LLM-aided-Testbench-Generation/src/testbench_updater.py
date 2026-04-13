"""
Step 5: Update testbench with golden outputs.
"""

from typing import Dict, Any, List
import re
import json
from .llm_client import LLMClient


class TestbenchUpdater:
    """Update generated testbench with golden outputs using LLM."""
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize testbench updater.
        
        Args:
            llm_client: LLM client instance
        """
        self.llm_client = llm_client
    
    def update_testbench(self, testbench_code: str, test_patterns_with_outputs: List[Dict[str, Any]], 
                        module_info: Dict[str, Any]) -> str:
        """
        Update testbench code to include expected outputs and verification.
        
        Args:
            testbench_code: Original testbench code without expected outputs
            test_patterns_with_outputs: Test patterns with golden outputs
            module_info: Module information
            
        Returns:
            Updated testbench code with assertions and expected outputs
        """
        # Use LLM if available, otherwise fall back to rule-based approach
        if self.llm_client.is_available():
            updated_code = self._llm_update_testbench(testbench_code, test_patterns_with_outputs, module_info)
        else:
            # Fallback to rule-based approach
            updated_code = self._add_verification_logic(testbench_code, test_patterns_with_outputs, module_info)
        
        return updated_code
    
    def _llm_update_testbench(self, testbench_code: str, test_patterns_with_outputs: List[Dict[str, Any]], 
                             module_info: Dict[str, Any]) -> str:
        """
        Use LLM to update testbench with verification logic.
        
        Args:
            testbench_code: Original testbench code
            test_patterns_with_outputs: Test patterns with golden outputs
            module_info: Module information
            
        Returns:
            Updated testbench code with verification logic
        """
        system_prompt = """You are an expert in Verilog testbench development and verification.
Your task is to update a testbench by adding comprehensive verification logic and expected output checks.
You should:
1. Add verification for each test case using the provided expected outputs
2. Track passed and failed test counts
3. Display clear pass/fail messages for each output signal
4. Generate a comprehensive test summary at the end
5. Maintain the original testbench structure and style
6. Use proper Verilog syntax and best practices"""

        # Prepare test patterns data for the LLM
        patterns_str = json.dumps(test_patterns_with_outputs, indent=2)
        
        user_prompt = f"""Given the following Verilog testbench and test patterns with expected outputs,
update the testbench to include verification logic that checks the actual outputs against the expected outputs.

Original Testbench Code:
```verilog
{testbench_code}
```

Module Information:
- Module Name: {module_info.get('module_name', 'unknown')}
- Inputs: {module_info.get('inputs', [])}
- Outputs: {module_info.get('outputs', [])}

Test Patterns with Expected Outputs:
```json
{patterns_str}
```

Please update the testbench to:
1. Add integer variables 'passed_tests' and 'failed_tests' at the beginning of the initial block (initialized to 0)
2. After each test case (identified by $display statements), add a delay (#10) for outputs to settle
3. For each output signal, compare the actual value against the expected value from the test patterns
4. Display "✓" for passing checks and "✗" for failing checks with actual and expected values
5. Increment passed_tests for each passing check and failed_tests for each failing check
6. At the end of the initial block (before 'end'), add a test summary showing:
   - Total tests run
   - Number passed
   - Number failed
7. Preserve all original test case displays and structure
8. Use proper indentation and formatting

Provide ONLY the complete updated testbench code, no explanations.
Format your response as:
```verilog
[updated testbench code here]
```
"""

        response = self.llm_client.generate(user_prompt, system_prompt, max_tokens=8000)
        
        # Extract the Verilog code from the response
        updated_code = self._extract_verilog_code(response)
        
        # If extraction failed, fall back to original with rule-based update
        if not updated_code or len(updated_code) < len(testbench_code) // 2:
            print("Warning: LLM response extraction failed, using rule-based approach")
            updated_code = self._add_verification_logic(testbench_code, test_patterns_with_outputs, module_info)
        
        return updated_code
    
    def _extract_verilog_code(self, text: str) -> str:
        """
        Extract Verilog code from LLM response.
        
        Args:
            text: LLM response text
            
        Returns:
            Extracted Verilog code
        """
        # Try to find code between ```verilog and ```
        if "```verilog" in text:
            start = text.find("```verilog") + len("```verilog")
            end = text.find("```", start)
            if end != -1:
                return text[start:end].strip()
        
        # Try to find code between ``` and ```
        if "```" in text:
            parts = text.split("```")
            if len(parts) >= 3:
                # Get the first code block
                code = parts[1].strip()
                # If it starts with a language identifier, remove it
                if code.startswith("verilog\n") or code.startswith("verilog "):
                    code = code.split('\n', 1)[1] if '\n' in code else code
                return code.strip()
        
        # If no code blocks found, look for module or testbench keywords
        if "module " in text or "initial " in text:
            return text.strip()
        
        return ""
    
    def _add_verification_logic(self, testbench_code: str, test_patterns: List[Dict[str, Any]], 
                               module_info: Dict[str, Any]) -> str:
        """
        Add verification logic to the testbench.
        
        Args:
            testbench_code: Original testbench code
            test_patterns: Test patterns with expected outputs
            module_info: Module information
            
        Returns:
            Testbench code with verification logic added
        """
        lines = testbench_code.split('\n')
        updated_lines = []
        
        # Track if we're in the initial block
        in_initial = False
        indent_level = 0
        test_case_num = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Detect initial block
            if 'initial' in stripped and 'begin' in stripped:
                in_initial = True
                updated_lines.append(line)
                # Add test result tracking variables after initial begin
                updated_lines.append("    integer passed_tests = 0;")
                updated_lines.append("    integer failed_tests = 0;")
                updated_lines.append("")
                continue
            
            # Check for test case markers (e.g., $display for test cases)
            if in_initial and '$display' in stripped and ('Test' in stripped or 'test' in stripped):
                # This is likely a test case display
                updated_lines.append(line)
                
                # Add delay to let outputs settle
                indent = len(line) - len(line.lstrip())
                indent_str = ' ' * indent
                updated_lines.append(f"{indent_str}#10; // Wait for outputs to settle")
                
                # Add verification for this test case if we have expected outputs
                if test_case_num < len(test_patterns):
                    pattern = test_patterns[test_case_num]
                    if 'expected_outputs' in pattern and pattern['expected_outputs']:
                        verification_lines = self._generate_verification(
                            pattern, module_info, indent
                        )
                        updated_lines.extend(verification_lines)
                    test_case_num += 1
                continue
            
            # Check for end of initial block
            if in_initial and (stripped == 'end' or stripped.startswith('end')):
                # Add final summary before the end
                indent = len(line) - len(line.lstrip())
                indent_str = ' ' * indent
                updated_lines.append("")
                updated_lines.append(f"{indent_str}// Test Summary")
                updated_lines.append(f'{indent_str}$display("\\n========== Test Summary ==========");')
                updated_lines.append(f'{indent_str}$display("Total Tests: %0d", passed_tests + failed_tests);')
                updated_lines.append(f'{indent_str}$display("Passed: %0d", passed_tests);')
                updated_lines.append(f'{indent_str}$display("Failed: %0d", failed_tests);')
                updated_lines.append(f'{indent_str}$display("==================================\\n");')
                updated_lines.append("")
                updated_lines.append(line)
                in_initial = False
                continue
            
            updated_lines.append(line)
        
        return '\n'.join(updated_lines)
    
    def _generate_verification(self, pattern: Dict[str, Any], module_info: Dict[str, Any], 
                              indent: int) -> List[str]:
        """
        Generate verification code for a single test pattern.
        
        Args:
            pattern: Test pattern with expected outputs
            expected_outputs: Expected output values
            module_info: Module information
            indent: Indentation level
            
        Returns:
            List of verification code lines
        """
        lines = []
        indent_str = ' ' * indent
        
        expected = pattern.get('expected_outputs', {})
        if not expected:
            return lines
        
        # Get output signals
        outputs = module_info.get('outputs', [])
        
        # Generate verification for each output
        for output in outputs:
            output_name = output.split('[')[0].strip()  # Remove bit width if present
            output_name = output_name.split()[-1]  # Get the signal name
            
            if output_name in expected:
                expected_value = expected[output_name]
                
                # Check if expected value is boolean
                if isinstance(expected_value, bool):
                    expected_value = 1 if expected_value else 0
                
                # Generate comparison
                lines.append(f"{indent_str}if ({output_name} === {expected_value}) begin")
                lines.append(f'{indent_str}    $display("  ✓ {output_name} = %b (expected: {expected_value})", {output_name});')
                lines.append(f"{indent_str}    passed_tests = passed_tests + 1;")
                lines.append(f"{indent_str}end else begin")
                lines.append(f'{indent_str}    $display("  ✗ {output_name} = %b (expected: {expected_value})", {output_name});')
                lines.append(f"{indent_str}    failed_tests = failed_tests + 1;")
                lines.append(f"{indent_str}end")
        
        return lines