#!/usr/bin/env python3
"""
Utility scripts for the Twitch IA FastAPI project.
Run these with: uv run python scripts.py <command>
"""

import sys
import subprocess
import os

def dev():
    """Start development server with hot reload"""
    subprocess.run([
        "uvicorn", "main:app", 
        "--reload", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])

def start():
    """Start production server"""
    subprocess.run([
        "uvicorn", "main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])

def format_code():
    """Format code with black"""
    subprocess.run(["black", "."])

def lint():
    """Lint code with flake8"""
    subprocess.run(["flake8", "."])

def sort_imports():
    """Sort imports with isort"""
    subprocess.run(["isort", "."])

def test():
    """Run tests"""
    subprocess.run(["pytest"])

def install_dev():
    """Install with dev dependencies"""
    subprocess.run(["uv", "sync", "--extra", "dev"])

def help_text():
    """Show available commands"""
    print("""
Available commands:
  dev              - Start development server with hot reload
  start            - Start production server  
  format           - Format code with black
  lint             - Lint code with flake8
  sort-imports     - Sort imports with isort
  test             - Run tests
  install-dev      - Install with dev dependencies
  help             - Show this help message

Usage: uv run python scripts.py <command>
Examples:
  uv run python scripts.py dev
  uv run python scripts.py format
  uv run python scripts.py test
    """)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        help_text()
        sys.exit(1)
    
    command = sys.argv[1]
    
    commands = {
        "dev": dev,
        "start": start,
        "format": format_code,
        "lint": lint,
        "sort-imports": sort_imports,
        "test": test,
        "install-dev": install_dev,
        "help": help_text,
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"Unknown command: {command}")
        help_text()
        sys.exit(1)
