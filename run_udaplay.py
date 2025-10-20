#!/usr/bin/env python3
"""UdaPlay AI Research Agent - CLI Runner

Simple command-line interface for running the UdaPlay agent.
"""

import sys
from pathlib import Path

from src.main import main

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


if __name__ == "__main__":
    main()
