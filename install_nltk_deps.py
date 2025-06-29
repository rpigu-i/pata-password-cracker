#!/usr/bin/env python3
"""
Script to install NLTK dependencies required by pata-password-cracker.

This script handles the NLTK WordNet corpus installation that was previously
handled by the custom install command in setup.py.
"""

def install_nltk_dependencies():
    """Install NLTK dependencies needed by the library."""
    try:
        import nltk
        print("Installing WordNet corpus...")
        nltk.download('wordnet', quiet=True)
        print("WordNet corpus installed successfully.")
    except ImportError:
        print("NLTK is not installed. Please install it first: pip install nltk")
        return False
    except Exception as e:
        print(f"Error installing NLTK dependencies: {e}")
        return False
    return True

if __name__ == "__main__":
    success = install_nltk_dependencies()
    exit(0 if success else 1)