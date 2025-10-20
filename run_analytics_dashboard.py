#!/usr/bin/env python3
"""Streamlit Analytics Dashboard Runner

This script properly sets up the environment and runs the advanced analytics dashboard.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import and run the dashboard
if __name__ == "__main__":
    try:
        import subprocess
        
        # Run streamlit with the analytics dashboard
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(Path(__file__).parent / "viz" / "advanced_analytics.py")
        ])
    except Exception as e:
        print(f"Error running analytics dashboard: {e}")
        sys.exit(1)
