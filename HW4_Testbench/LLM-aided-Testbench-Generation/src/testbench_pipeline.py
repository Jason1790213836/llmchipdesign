"""
Main pipeline orchestrating the entire testbench generation process.
"""

import json
import os
from typing import Dict, Any, Optional
from .llm_client import LLMClient
from .testbench_generator import TestbenchGenerator
from .golden_model_generator import GoldenModelGenerator
from .testbench_updater import TestbenchUpdater
import subprocess

class TestbenchPipeline:
    """
    Main pipeline for LLM-aided testbench generation.
    
    Steps:
    1. Accept natural language description and Verilog code
    2. Generate testbench with test patterns (no golden outputs)
    3. Generate Python golden model from description
    4. Execute golden model with test patterns to get expected outputs
    5. Update testbench with golden outputs and verification logic
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4", provider: str = "openai"):
        """
        Initialize the pipeline.
        
        Args:
            api_key: API key for LLM provider
            model: Model name to use
            provider: LLM provider name
        """
        self.llm_client = LLMClient(api_key, model, provider)
        self.testbench_gen = TestbenchGenerator(self.llm_client)
        self.golden_gen = GoldenModelGenerator(self.llm_client)
        self.testbench_updater = TestbenchUpdater(self.llm_client)
        
    def run(self, description: str, verilog_code: str, output_dir: str = "output") -> Dict[str, Any]:
        """
        Run the complete testbench generation pipeline.
        
        Args:
            description: Natural language description of the module
            verilog_code: Verilog code to be tested
            output_dir: Directory to save output files
            
        Returns:
            Dictionary containing all generated artifacts
        """
        print("=" * 80)
        print("LLM-Aided Testbench Generation Pipeline")
        print("=" * 80)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Step 1 & 2: Input handling (description and verilog code are already provided)
        print("\n[Step 1-2] Input: Natural language description and Verilog code received")
        print(f"Description length: {len(description)} characters")
        print(f"Verilog code length: {len(verilog_code)} characters")
        
        # Step 3: Generate testbench with test patterns
        print("\n[Step 3] Generating testbench with test patterns...")
        if not self.llm_client.is_available():
            print("WARNING: LLM client not configured. Using mock generation.")
            testbench_result = self._mock_testbench_generation(verilog_code)
        else:
            testbench_result = self.testbench_gen.generate_testbench(description, verilog_code)
        
        print(f"  - Generated testbench with {len(testbench_result['test_patterns'])} test patterns")
        print(f"  - Module: {testbench_result['module_info']['module_name']}")
        
        # Save initial testbench (without golden outputs)
        initial_tb_path = os.path.join(output_dir, "testbench_initial.v")
        with open(initial_tb_path, 'w') as f:
            f.write(testbench_result['testbench_code'])
        print(f"  - Saved initial testbench to: {initial_tb_path}")
        
        # Step 4: Generate Python golden model and compute golden outputs
        print("\n[Step 4] Generating Python golden model and computing expected outputs...")
        if not self.llm_client.is_available():
            print("WARNING: LLM client not configured. Using mock golden model.")
            python_code = self._mock_python_model(testbench_result['module_info'])
        else:
            python_code = self.golden_gen.generate_python_model(
                description, 
                testbench_result['module_info']
            )
        
        print(f"  - Generated Python golden model ({len(python_code)} characters)")
        
        # change testbench_result['test_patterns'] value to integral values
        patterns = []
        for pattern in testbench_result['test_patterns']:
            for key in pattern:
                if isinstance(pattern[key], str):
                    pattern[key] = int(pattern[key], 2)
            patterns.append(pattern)
        testbench_result['test_patterns'] = patterns

        # Save Python golden model
        python_path = os.path.join(output_dir, "golden_model.py")
        with open(python_path, 'w') as f:
            f.write(python_code)
        print(f"  - Saved Python golden model to: {python_path}")
        
        # Compute golden outputs
        print("  - Computing golden outputs for all test patterns...")
        test_patterns_with_outputs = self.golden_gen.compute_golden_outputs(
            python_code,
            testbench_result['test_patterns'],
            testbench_result['module_info']
        )
        
        successful_patterns = sum(1 for p in test_patterns_with_outputs 
                                 if 'expected_outputs' in p and p['expected_outputs'] is not None)
        print(f"  - Successfully computed outputs for {successful_patterns}/{len(test_patterns_with_outputs)} patterns")
        
        # Save test patterns with golden outputs
        patterns_path = os.path.join(output_dir, "test_patterns_with_golden.json")
        with open(patterns_path, 'w') as f:
            json.dump(test_patterns_with_outputs, f, indent=2)
        print(f"  - Saved test patterns with golden outputs to: {patterns_path}")
        
        # Step 5: Update testbench with golden outputs
        print("\n[Step 5] Updating testbench with golden outputs and verification logic...")
        final_testbench = self.testbench_updater.update_testbench(
            testbench_result['testbench_code'],
            test_patterns_with_outputs,
            testbench_result['module_info']
        )
        
        # Save final testbench
        final_tb_path = os.path.join(output_dir, "testbench_final.v")
        with open(final_tb_path, 'w') as f:
            f.write(final_testbench)
        print(f"  - Saved final testbench to: {final_tb_path}")
        
        print("\n" + "=" * 80)
        print("Pipeline completed successfully!")
        print("=" * 80)
        print(f"\nGenerated files in '{output_dir}':")
        print(f"  - testbench_initial.v    : Initial testbench with test patterns")
        print(f"  - golden_model.py        : Python reference implementation")
        print(f"  - test_patterns_with_golden.json : Test patterns with expected outputs")
        print(f"  - testbench_final.v      : Final testbench with verification")
        print()
        
        return {
            'description': description,
            'verilog_code': verilog_code,
            'module_info': testbench_result['module_info'],
            'test_patterns': testbench_result['test_patterns'],
            'initial_testbench': testbench_result['testbench_code'],
            'python_golden_model': python_code,
            'test_patterns_with_outputs': test_patterns_with_outputs,
            'final_testbench': final_testbench,
            'output_dir': output_dir
        }
    
    def _mock_testbench_generation(self, verilog_code: str) -> Dict[str, Any]:
        """Mock testbench generation when LLM is not available."""
        return {
            'testbench_code': '// Mock testbench - LLM not configured\n' + verilog_code,
            'test_patterns': [],
            'module_info': {
                'module_name': 'unknown',
                'inputs': [],
                'outputs': []
            }
        }
    
    def _mock_python_model(self, module_info: Dict[str, Any]) -> str:
        """Mock Python model generation when LLM is not available."""
        return f"# Mock Python model - LLM not configured\ndef {module_info['module_name']}_golden():\n    pass\n"