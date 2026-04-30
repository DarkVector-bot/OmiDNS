#!/usr/bin/env python3
"""
SubD3 - Main Entry Point
"""

import asyncio
import argparse
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from subd3.core.engine import SubD3Engine
from subd3.utils.logger import setup_logger
from subd3.utils.config import load_config


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="SubD3 - Fast Subdomain Discovery Tool",
        epilog="Example: python -m subd3 -d example.com -o results.json --stealth"
    )
    
    # Required
    parser.add_argument("-d", "--domain", required=True, help="Target domain")
    
    # Optional
    parser.add_argument("-w", "--wordlist", help="Custom wordlist file")
    parser.add_argument("-o", "--output", help="Output file (JSON/TXT/CSV)")
    parser.add_argument("-c", "--concurrency", type=int, default=500, help="Concurrent queries (default: 500)")
    parser.add_argument("-t", "--timeout", type=float, default=3.0, help="DNS timeout (default: 3.0)")
    
    # Modes
    parser.add_argument("--stealth", action="store_true", help="Enable stealth mode")
    parser.add_argument("--aggressive", action="store_true", help="Aggressive mode (faster but noisier)")
    parser.add_argument("--no-ai", action="store_true", help="Disable AI prediction")
    parser.add_argument("--no-permutation", action="store_true", help="Disable permutation attack")
    parser.add_argument("--no-passive", action="store_true", help="Disable passive sources")
    
    # Output
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--csv", action="store_true", help="Output as CSV")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--version", action="version", version="SubD3 v2.0.0")
    
    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_args()
    
    # Setup logger
    logger = setup_logger(verbose=args.verbose)
    
    # Load config
    config = load_config()
    
    # Determine output format
    output_format = "txt"
    if args.json:
        output_format = "json"
    elif args.csv:
        output_format = "csv"
    
    # Create engine
    engine = SubD3Engine(
        domain=args.domain.lower(),
        wordlist_file=args.wordlist,
        output_file=args.output,
        output_format=output_format,
        concurrency=args.concurrency,
        timeout=args.timeout,
        stealth=args.stealth,
        aggressive=args.aggressive,
        use_ai=not args.no_ai,
        use_permutation=not args.no_permutation,
        use_passive=not args.no_passive,
        verbose=args.verbose
    )
    
    try:
        # Run scan
        asyncio.run(engine.run())
    except KeyboardInterrupt:
        print("\n[-] Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Fatal error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
