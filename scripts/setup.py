#!/usr/bin/env python3
"""
Setup Script for Sports Analytics Pipeline
Location: /scripts/setup.py
Purpose: One-command setup for new installations

Handles: dependencies, models, directories, configuration, testing
"""

import subprocess
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def run_command(cmd, description):
    """Run shell command with error handling"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        print(f"✅ {description} - DONE")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"   Error: {e.stderr}")
        return False


def check_python_version():
    """Verify Python version"""
    print_header("1/7: Checking Python Version")
    
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        print(f"   Current: {version.major}.{version.minor}")
        print(f"   Please upgrade: https://www.python.org/downloads/")
        return False
    
    print("✅ Python version OK")
    return True


def create_virtual_environment():
    """Create Python virtual environment"""
    print_header("2/7: Creating Virtual Environment")
    
    venv_path = PROJECT_ROOT / "venv"
    
    if venv_path.exists():
        print(f"   Virtual environment already exists: {venv_path}")
        response = input("   Recreate? [y/N]: ")
        if response.lower() != 'y':
            print("✅ Using existing virtual environment")
            return True
        
        # Remove old venv
        import shutil
        shutil.rmtree(venv_path)
    
    return run_command(
        f"{sys.executable} -m venv venv",
        "Creating virtual environment"
    )


def install_dependencies():
    """Install Python dependencies"""
    print_header("3/7: Installing Dependencies")
    
    # Determine pip path
    if sys.platform == "win32":
        pip_path = PROJECT_ROOT / "venv" / "Scripts" / "pip"
    else:
        pip_path = PROJECT_ROOT / "venv" / "bin" / "pip"
    
    # Upgrade pip
    if not run_command(
        f"{pip_path} install --upgrade pip",
        "Upgrading pip"
    ):
        return False
    
    # Install requirements
    if not run_command(
        f"{pip_path} install -r requirements.txt",
        "Installing dependencies (this may take 5-10 minutes)"
    ):
        return False
    
    # Install development dependencies (optional)
    dev_req = PROJECT_ROOT / "requirements-dev.txt"
    if dev_req.exists():
        response = input("\n   Install development dependencies (testing, linting)? [Y/n]: ")
        if response.lower() != 'n':
            run_command(
                f"{pip_path} install -r requirements-dev.txt",
                "Installing dev dependencies"
            )
    
    return True


def download_models():
    """Download YOLO models"""
    print_header("4/7: Downloading YOLO Models")
    
    # Determine python path
    if sys.platform == "win32":
        python_path = PROJECT_ROOT / "venv" / "Scripts" / "python"
    else:
        python_path = PROJECT_ROOT / "venv" / "bin" / "python"
    
    print("\n   Recommended: YOLO11x (110MB, 54.7 mAP, best for football)")
    print("   Alternatives: YOLO11m (50MB), YOLO11s (22MB), YOLO11n (6MB)")
    
    response = input("\n   Download YOLO11x? [Y/n]: ")
    if response.lower() == 'n':
        print("⚠️  Skipping model download")
        print("   Manual download: python scripts/download_models.py --download")
        return True
    
    return run_command(
        f"{python_path} scripts/download_models.py --download",
        "Downloading YOLO11x model"
    )


def create_directories():
    """Ensure all directories exist"""
    print_header("5/7: Creating Directories")
    
    directories = [
        "models",
        "input_videos",
        "output_videos",
        "output_videos/heatmaps",
        "output_videos/visualizations",
        "logs",
        "data",
        "notebooks"
    ]
    
    for directory in directories:
        dir_path = PROJECT_ROOT / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {directory}/")
    
    print("✅ All directories created")
    return True


def run_tests():
    """Run test suite"""
    print_header("6/7: Running Tests")
    
    # Determine python path
    if sys.platform == "win32":
        python_path = PROJECT_ROOT / "venv" / "Scripts" / "python"
    else:
        python_path = PROJECT_ROOT / "venv" / "bin" / "python"
    
    response = input("   Run tests? [Y/n]: ")
    if response.lower() == 'n':
        print("⚠️  Skipping tests")
        return True
    
    return run_command(
        f"{python_path} -m pytest tests/ -v",
        "Running test suite"
    )


def print_next_steps():
    """Print next steps"""
    print_header("7/7: Setup Complete!")
    
    print("\n🎉 Sports Analytics Pipeline is ready!")
    print("\n📋 NEXT STEPS:\n")
    
    print("1️⃣  Activate virtual environment:")
    if sys.platform == "win32":
        print("     venv\\Scripts\\activate")
    else:
        print("     source venv/bin/activate")
    
    print("\n2️⃣  Place match video in input_videos/")
    print("     Example: input_videos/unam_fc_vs_african_stars.mp4")
    
    print("\n3️⃣  Calibrate field (first time only):")
    print("     python tools/define_field_polygon.py input_videos/your_match.mp4")
    
    print("\n4️⃣  Analyze match:")
    print("     python analyze_match.py input_videos/your_match.mp4")
    
    print("\n5️⃣  View results:")
    print("     output_videos/your_match/")
    print("       - your_match_complete_analysis.mp4  (annotated video)")
    print("       - tracking_data.csv                  (player positions)")
    print("       - passes.csv                         (pass analysis)")
    print("       - statistics.json                    (complete stats)")
    print("       - heatmaps/                          (position heatmaps)")
    print("       - visualizations/                    (pass networks)")
    
    print("\n📖 Documentation:")
    print("     docs/PRD_WEB_DASHBOARD.md            (Complete requirements)")
    print("     docs/API_DOCUMENTATION.md            (API reference)")
    print("     docs/UNAM_13_CAMPUSES_STRATEGY.md    (Namibian deployment)")
    
    print("\n🆘 Help:")
    print("     python analyze_match.py --help")
    print("     python scripts/download_models.py --help")
    
    print("\n" + "="*60)


def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("⚽ Sports Analytics Pipeline Setup")
    print("   Focus: Football/Soccer Analysis (Namibian Market)")
    print("   Model: YOLO11x (Recommended)")
    print("="*60)
    
    # Step-by-step setup
    steps = [
        check_python_version,
        create_virtual_environment,
        install_dependencies,
        download_models,
        create_directories,
        run_tests,
        print_next_steps
    ]
    
    for step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_func.__name__}")
            print(f"   Fix the error and run setup again")
            sys.exit(1)
    
    print("\n✅ Setup completed successfully!")
    sys.exit(0)


if __name__ == "__main__":
    main()
