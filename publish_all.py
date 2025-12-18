"""
Script to build and publish all packages to PyPI.

Usage:
    python publish_all.py           # Dry run (build only)
    python publish_all.py --publish # Actually publish to PyPI
"""

import subprocess
import sys
from pathlib import Path


PACKAGES = [
    "retryit",
    "envmaster", 
    "cachely",
    "logfmt",
    "cliprog",
    "validdict",
    "timefunc",
    "pyprojectcheck",
]


def run_command(cmd: list, cwd: Path) -> bool:
    """Run a command and return success status."""
    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ❌ Error: {result.stderr}")
        return False
    return True


def build_package(package_dir: Path) -> bool:
    """Build a package."""
    print(f"\n📦 Building {package_dir.name}...")
    
    # Clean old builds
    dist_dir = package_dir / "dist"
    if dist_dir.exists():
        import shutil
        shutil.rmtree(dist_dir)
    
    # Build
    if not run_command([sys.executable, "-m", "build"], package_dir):
        return False
    
    print(f"  ✅ Built successfully")
    return True


def publish_package(package_dir: Path) -> bool:
    """Publish a package to PyPI."""
    print(f"\n🚀 Publishing {package_dir.name}...")
    
    if not run_command(
        [sys.executable, "-m", "twine", "upload", "dist/*"],
        package_dir
    ):
        return False
    
    print(f"  ✅ Published successfully")
    return True


def main():
    publish = "--publish" in sys.argv
    
    packages_dir = Path(__file__).parent / "packages"
    
    print("=" * 50)
    print("PyPI Warehouse - Package Publisher")
    print("=" * 50)
    
    if not publish:
        print("\n⚠️  DRY RUN MODE - packages will be built but not published")
        print("   Add --publish flag to actually publish to PyPI\n")
    
    # Check dependencies
    print("Checking dependencies...")
    try:
        import build
        import twine
    except ImportError:
        print("Installing build tools...")
        subprocess.run([sys.executable, "-m", "pip", "install", "build", "twine"])
    
    successful = []
    failed = []
    
    for package_name in PACKAGES:
        package_dir = packages_dir / package_name
        
        if not package_dir.exists():
            print(f"\n⚠️  Package directory not found: {package_dir}")
            failed.append(package_name)
            continue
        
        # Build
        if not build_package(package_dir):
            failed.append(package_name)
            continue
        
        # Publish (if flag set)
        if publish:
            if not publish_package(package_dir):
                failed.append(package_name)
                continue
        
        successful.append(package_name)
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"✅ Successful: {len(successful)}")
    for pkg in successful:
        print(f"   - {pkg}")
    
    if failed:
        print(f"❌ Failed: {len(failed)}")
        for pkg in failed:
            print(f"   - {pkg}")
    
    if publish and successful:
        print("\n📦 Published packages:")
        for pkg in successful:
            print(f"   https://pypi.org/project/{pkg}/")


if __name__ == "__main__":
    main()
