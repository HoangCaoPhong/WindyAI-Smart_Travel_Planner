#!/usr/bin/env python3
"""
Script to run all tests and generate coverage report
Usage: python run_tests.py
"""
import subprocess
import sys
import os


def run_tests():
    """Run pytest with coverage"""
    print("=" * 70)
    print("Running Smart Travel Project Test Suite")
    print("20 Comprehensive Test Cases")
    print("=" * 70)
    print()
    
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_comprehensive.py",
        "-v",
        "--tb=short",
        "--cov=core",
        "--cov-report=term-missing",
        "--cov-report=html",
        "-x"  # Stop on first failure
    ]
    
    try:
        result = subprocess.run(cmd, check=False)
        
        print()
        print("=" * 70)
        if result.returncode == 0:
            print("✓ ALL TESTS PASSED!")
            print()
            print("Coverage report generated in htmlcov/index.html")
            print("Open it in your browser to see detailed coverage.")
        else:
            print("✗ Some tests failed. Please check the output above.")
        print("=" * 70)
        
        return result.returncode
    
    except FileNotFoundError:
        print("Error: pytest not found. Please install it:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
