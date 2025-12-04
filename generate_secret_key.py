#!/usr/bin/env python
"""
Generate a Django SECRET_KEY for use in production environments.

Usage:
    python generate_secret_key.py
"""

import os
import sys

# Add the project directory to Python path to import Django settings
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from django.core.management.utils import get_random_secret_key
    
    def generate_secret_key():
        """Generate and display a random secret key."""
        secret_key = get_random_secret_key()
        print("=" * 60)
        print("Django SECRET_KEY Generated Successfully!")
        print("=" * 60)
        print("\nCopy this key and use it as your SECRET_KEY environment variable:\n")
        print(secret_key)
        print("\n" + "=" * 60)
        print("\nExample usage in .env file:")
        print(f"SECRET_KEY={secret_key}")
        print("\nOr set it as an environment variable:")
        print(f"export SECRET_KEY='{secret_key}'")
        print("\n" + "=" * 60)
        return secret_key
    
    if __name__ == "__main__":
        generate_secret_key()
        
except ImportError:
    # Fallback method if Django is not installed
    import secrets
    import string
    
    def generate_secret_key_fallback():
        """Generate a secret key without Django (fallback method)."""
        chars = string.ascii_letters + string.digits + string.punctuation
        secret_key = ''.join(secrets.choice(chars) for _ in range(50))
        
        print("=" * 60)
        print("Django SECRET_KEY Generated (Fallback Method)")
        print("=" * 60)
        print("\nNOTE: Django is not installed. Using fallback method.")
        print("\nCopy this key and use it as your SECRET_KEY environment variable:\n")
        print(secret_key)
        print("\n" + "=" * 60)
        print("\nExample usage in .env file:")
        print(f"SECRET_KEY={secret_key}")
        print("\nOr set it as an environment variable:")
        print(f"export SECRET_KEY='{secret_key}'")
        print("\n" + "=" * 60)
        return secret_key
    
    if __name__ == "__main__":
        generate_secret_key_fallback()

