"""Check Python version and exit with helpful message.

Requires Python >= 3.11 and < 3.14 (project-tested)

Run this before installing dependencies to avoid build-from-source issues
for packages like `pydantic-core` and `psycopg2-binary` on very new Python
versions where wheels might not be available.
"""
import sys

MIN = (3, 11)
MAX = (3, 14)

if sys.version_info < MIN or sys.version_info >= MAX:
    print("\nERROR: Unsupported Python version detected:\n")
    print(f"  Detected: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"  Supported: >= {MIN[0]}.{MIN[1]} and < {MAX[0]}.{MAX[1]}\n")
    print("Recommended actions:")
    print("  - Install Python 3.11 or 3.12 and use a virtual environment")
    print("  - OR install Rust toolchain (rustup) and PostgreSQL development tools (pg_config) to build packages from source")
    print("\nSee LOCAL_SETUP.md for details.\n")
    sys.exit(1)

print(f"Python version OK: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
sys.exit(0)
