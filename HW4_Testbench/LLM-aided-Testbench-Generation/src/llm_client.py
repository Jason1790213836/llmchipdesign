"""
LLM Client for interacting with language models.
Supports multiple LLM providers (OpenAI, Anthropic, etc.)
"""

import os
import json
from typing import Optional, Dict, Any
from xml.parsers.expat import model
import openai


class LLMClient:
    """Client for interacting with LLM APIs."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4", provider: str = "openai"):
        """
        Initialize LLM client.
        
        Args:
            api_key: API key for the LLM provider (if None, reads from environment)
            model: Model name to use
            provider: LLM provider ('openai', 'anthropic', etc.)
        """
        self.provider = provider
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                 temperature: float = 0.7, max_tokens: int = 4000) -> str:
        """
        Generate text using the LLM.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for the model
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        try:
            if self.provider == "openai":
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return response.choices[0].message.content
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if the LLM client is properly configured."""
        return self.api_key is not None and len(self.api_key) > 0
