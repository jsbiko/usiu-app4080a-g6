#!/usr/bin/env python3
"""
USIU G6 Test Runner
===================
Runs all tests: server, integration, and automated client tests.

Usage:
    python run_all_tests.py              # Run all tests
    python run_all_tests.py --server     # Run only server tests
    python run_all_tests.py --integration # Run only integration tests
    python run_all_tests.py --client     # Run only client tests
"""

import sys
import os
import subprocess
import argparse


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(text.center(70))
    print("="*70 + "\n")


def check_server():
    """Check if Flask server is running"""
    import requests
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        return True
    except:
        return False


def run_test_file(test_file, name):
    """Run a specific test file"""
    print_header(f"Running {name}")
    
    test_path = os.path.join(os.path.dirname(__file__), test_file)
    result = subprocess.run([sys.executable, test_path], cwd=os.path.dirname(__file__))
    
    return result.returncode == 0


def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description='Run USIU G6 test suite')
    parser.add_argument('--server', action='store_true', help='Run only server tests')
    parser.add_argument('--integration', action='store_true', help='Run only integration tests')
    parser.add_argument('--client', action='store_true', help='Run only automated client tests')
    
    args = parser.parse_args()
    
    # If no specific flag, run all tests
    run_all = not (args.server or args.integration or args.client)
    
    print_header("USIU G6 TEST SUITE")
    print("📋 Test Suite Configuration")
    print("   - Server Tests: 12 tests")
    print("   - Integration Tests: 4 tests")
    print("   - Automated Client Tests: 10 tests")
    print("   - Total: 26 tests\n")
    
    results = {}
    
    # Check if server is running for client tests
    if args.client or run_all:
        print("🔍 Checking if Flask server is running...")
        if not check_server():
            print("⚠️  Warning: Flask server is not running on http://localhost:5000")
            print("   Client tests will be skipped.")
            print("   Start server with: cd server && python app.py\n")
            if args.client:
                return 1
        else:
            print("✅ Server is running\n")
    
    # Run tests based on arguments
    if args.server or run_all:
        results['server'] = run_test_file('test_server.py', 'Server Tests')
    
    if args.integration or run_all:
        results['integration'] = run_test_file('test_integration.py', 'Integration Tests')
    
    if args.client or run_all:
        if check_server():
            results['client'] = run_test_file('test_client_automated.py', 'Automated Client Tests')
        else:
            results['client'] = False
    
    # Print final summary
    print_header("FINAL TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_type, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_type.upper():15} {status}")
    
    print(f"\n{'='*70}")
    print(f"Overall: {passed}/{total} test suites passed")
    print(f"{'='*70}\n")
    
    # Return 0 if all passed, 1 if any failed
    return 0 if all(results.values()) else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
