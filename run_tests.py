#!/usr/bin/env python3
"""
Test harness and runner for Rock Paper Scissors game.

Usage:
    python3 run_tests.py              # Run all tests
    python3 run_tests.py --verbose    # Run with verbose output
    python3 run_tests.py --coverage   # Run with coverage report (requires coverage module)
"""

import sys
import unittest
import argparse
from io import StringIO


def run_tests(verbosity=1, coverage=False):
    """
    Run the test suite.

    Args:
        verbosity: Verbosity level (0, 1, or 2)
        coverage: Whether to generate a coverage report

    Returns:
        True if all tests passed, False otherwise
    """
    # Load tests from test module
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')

    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n✓ All tests passed!")
        return True
    else:
        print("\n✗ Some tests failed")
        return False


def print_test_categories():
    """Print a summary of test categories."""
    categories = {
        "Unit Tests": [
            "TestGetComputerChoice - Random choice generation",
            "TestDetermineWinner - Game logic for all 9 combinations",
            "TestPlayRound - Round execution and output",
        ],
        "Integration Tests": [
            "TestMainGameFlow - Full game scenarios",
            "  - Human wins match (5 wins)",
            "  - Computer wins match (5 wins)",
            "  - Game with ties",
            "  - Input validation",
            "  - Case-insensitive input",
            "  - Score tracking",
        ],
        "Edge Cases": [
            "TestEdgeCases - Boundary conditions",
            "  - All choice combinations validity",
            "  - Exact 5 win boundary",
        ],
    }

    print("\n" + "=" * 70)
    print("TEST COVERAGE")
    print("=" * 70)
    for category, tests in categories.items():
        print(f"\n{category}:")
        for test in tests:
            print(f"  • {test}")
    print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Test harness for Rock Paper Scissors game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 run_tests.py              # Run all tests
  python3 run_tests.py --verbose    # Verbose output
  python3 run_tests.py --info       # Show test categories
        """
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose test output'
    )
    parser.add_argument(
        '--info',
        action='store_true',
        help='Show test categories and exit'
    )
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Generate coverage report (requires coverage module)'
    )

    args = parser.parse_args()

    if args.info:
        print_test_categories()
        return 0

    # Determine verbosity
    verbosity = 2 if args.verbose else 1

    # Run tests
    print("Running Rock Paper Scissors Game Tests...")
    success = run_tests(verbosity=verbosity, coverage=args.coverage)

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
