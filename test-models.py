#!/usr/bin/env python3
"""Test which Claude models are available with the API key"""
import os
from anthropic import Anthropic

# Load API key from .env
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("ERROR: No API key found in .env")
    exit(1)

client = Anthropic(api_key=api_key)

# Try different model names
models_to_try = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]

print("Testing which models are accessible with your API key...\n")

for model in models_to_try:
    try:
        response = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"[OK] {model} - WORKS!")
        break  # Stop after first working model
    except Exception as e:
        error_type = type(e).__name__
        print(f"[FAIL] {model} - {error_type}")

print("\nDone!")
