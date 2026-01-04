#!/usr/bin/env python3
"""
Model Download Script
Location: /scripts/download_models.py
Purpose: Download and setup YOLO models for football analysis

Downloads YOLO11x (recommended) and optionally YOLOv8x for comparison.
Handles integrity verification and proper placement.
"""

import os
import sys
from pathlib import Path
import hashlib
import urllib.request
from tqdm import tqdm

# Add parent directory to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import Settings

# Model URLs (Ultralytics official releases)
MODELS = {
    'yolo11x': {
        'url': 'https://github.com/ultralytics/assets/releases/download/v8.1.0/yolo11x.pt',
        'size_mb': 110,
        'description': 'YOLO11x - Highest accuracy (54.7 mAP), recommended for football',
        'recommended': True
    },
    'yolo11m': {
        'url': 'https://github.com/ultralytics/assets/releases/download/v8.1.0/yolo11m.pt',
        'size_mb': 50,
        'description': 'YOLO11m - Balanced accuracy/speed (51.5 mAP)',
        'recommended': False
    },
    'yolo11s': {
        'url': 'https://github.com/ultralytics/assets/releases/download/v8.1.0/yolo11s.pt',
        'size_mb': 22,
        'description': 'YOLO11s - Fast, lower accuracy (47.0 mAP)',
        'recommended': False
    },
    'yolo11n': {
        'url': 'https://github.com/ultralytics/assets/releases/download/v8.1.0/yolo11n.pt',
        'size_mb': 6,
        'description': 'YOLO11n - Fastest, lowest accuracy (39.5 mAP)',
        'recommended': False
    },
    'yolov8x': {
        'url': 'https://github.com/ultralytics/assets/releases/download/v8.0.0/yolov8x.pt',
        'size_mb': 130,
        'description': 'YOLOv8x - Legacy model (53.9 mAP), for comparison',
        'recommended': False
    }
}


class ModelDownloader:
    """Downloads and verifies YOLO models"""
    
    def __init__(self, models_dir=None):
        """
        Initialize downloader
        
        Args:
            models_dir: Directory to save models (default: PROJECT_ROOT/models/)
        """
        self.models_dir = Path(models_dir) if models_dir else Settings.MODELS_DIR
        self.models_dir.mkdir(parents=True, exist_ok=True)
    
    def download_model(self, model_name, force=False):
        """
        Download a specific model
        
        Args:
            model_name: Model key from MODELS dict
            force: Force re-download if file exists
            
        Returns:
            Path to downloaded model
        """
        if model_name not in MODELS:
            print(f"❌ Unknown model: {model_name}")
            print(f"   Available: {', '.join(MODELS.keys())}")
            return None
        
        model_info = MODELS[model_name]
        model_path = self.models_dir / f"{model_name}.pt"
        
        # Check if already exists
        if model_path.exists() and not force:
            print(f"✅ Model already exists: {model_path}")
            print(f"   Use --force to re-download")
            return model_path
        
        # Download
        print(f"📥 Downloading {model_name}...")
        print(f"   {model_info['description']}")
        print(f"   Size: ~{model_info['size_mb']}MB")
        print(f"   URL: {model_info['url']}")
        
        try:
            # Create progress bar
            def reporthook(block_num, block_size, total_size):
                if not hasattr(reporthook, 'pbar'):
                    reporthook.pbar = tqdm(
                        total=total_size,
                        unit='B',
                        unit_scale=True,
                        desc=model_name
                    )
                downloaded = block_num * block_size
                if downloaded < total_size:
                    reporthook.pbar.update(block_size)
                else:
                    reporthook.pbar.close()
                    delattr(reporthook, 'pbar')
            
            # Download
            temp_path = model_path.with_suffix('.tmp')
            urllib.request.urlretrieve(model_info['url'], temp_path, reporthook)
            
            # Rename to final
            temp_path.rename(model_path)
            
            print(f"✅ Downloaded: {model_path}")
            return model_path
        
        except Exception as e:
            print(f"❌ Download failed: {e}")
            print(f"   Manual download: {model_info['url']}")
            print(f"   Save to: {model_path}")
            return None
    
    def download_all_recommended(self, force=False):
        """
        Download all recommended models
        
        Args:
            force: Force re-download
            
        Returns:
            List of downloaded model paths
        """
        downloaded = []
        
        for model_name, model_info in MODELS.items():
            if model_info['recommended']:
                path = self.download_model(model_name, force)
                if path:
                    downloaded.append(path)
        
        return downloaded
    
    def download_all(self, force=False):
        """
        Download all available models
        
        Args:
            force: Force re-download
            
        Returns:
            List of downloaded model paths
        """
        downloaded = []
        
        for model_name in MODELS.keys():
            path = self.download_model(model_name, force)
            if path:
                downloaded.append(path)
        
        return downloaded
    
    def verify_model(self, model_path):
        """
        Verify model integrity by loading it
        
        Args:
            model_path: Path to model file
            
        Returns:
            True if valid, False otherwise
        """
        try:
            from ultralytics import YOLO
            print(f"🔍 Verifying {model_path}...")
            
            model = YOLO(str(model_path))
            print(f"✅ Model valid: {model_path}")
            print(f"   Architecture: {model.model.yaml.get('backbone', 'Unknown')}")
            print(f"   Classes: {len(model.names)} ({', '.join(list(model.names.values())[:5])}...)")
            return True
        
        except Exception as e:
            print(f"❌ Model verification failed: {e}")
            return False
    
    def create_symlink(self, model_name='yolo11x'):
        """
        Create best.pt symlink pointing to specified model
        
        Args:
            model_name: Model to link (default: yolo11x)
        """
        source = self.models_dir / f"{model_name}.pt"
        target = self.models_dir / "best.pt"
        
        if not source.exists():
            print(f"❌ Source model not found: {source}")
            return False
        
        # Remove existing symlink/file
        if target.exists() or target.is_symlink():
            target.unlink()
        
        # Create symlink
        try:
            target.symlink_to(source.name)  # Relative symlink
            print(f"✅ Created symlink: best.pt → {model_name}.pt")
            return True
        except Exception as e:
            # Symlinks may fail on Windows, copy instead
            import shutil
            shutil.copy(source, target)
            print(f"✅ Copied model: best.pt ← {model_name}.pt")
            return True
    
    def list_models(self):
        """List all models in directory"""
        print(f"\n📂 Models in {self.models_dir}:")
        print("-" * 60)
        
        model_files = sorted(self.models_dir.glob("*.pt"))
        
        if not model_files:
            print("   (No models found)")
            print("\n💡 Run: python scripts/download_models.py --download")
            return
        
        for model_file in model_files:
            size_mb = model_file.stat().st_size / (1024 * 1024)
            is_symlink = model_file.is_symlink()
            
            if is_symlink:
                target = model_file.resolve().name
                print(f"   🔗 {model_file.name} → {target} ({size_mb:.1f}MB)")
            else:
                print(f"   📦 {model_file.name} ({size_mb:.1f}MB)")
        
        print("-" * 60)


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="⚽ Download YOLO models for football analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download recommended model (YOLO11x)
  python scripts/download_models.py --download
  
  # Download specific model
  python scripts/download_models.py --model yolo11x
  
  # Download all models
  python scripts/download_models.py --all
  
  # List existing models
  python scripts/download_models.py --list
  
  # Verify model integrity
  python scripts/download_models.py --verify models/yolo11x.pt
        """
    )
    
    parser.add_argument(
        '--download',
        action='store_true',
        help='Download recommended model (YOLO11x)'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        choices=list(MODELS.keys()),
        help='Download specific model'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Download all available models'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all models in directory'
    )
    
    parser.add_argument(
        '--verify',
        type=str,
        help='Verify model integrity'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-download even if file exists'
    )
    
    parser.add_argument(
        '--symlink',
        type=str,
        help='Create best.pt symlink to specified model'
    )
    
    args = parser.parse_args()
    
    downloader = ModelDownloader()
    
    # List models
    if args.list:
        downloader.list_models()
        return
    
    # Verify model
    if args.verify:
        if downloader.verify_model(args.verify):
            sys.exit(0)
        else:
            sys.exit(1)
    
    # Create symlink
    if args.symlink:
        if downloader.create_symlink(args.symlink):
            sys.exit(0)
        else:
            sys.exit(1)
    
    # Download models
    if args.download:
        # Download recommended (YOLO11x)
        print("🎯 Downloading recommended model for football analysis...")
        paths = downloader.download_all_recommended(force=args.force)
        
        if paths:
            print(f"\n✅ Downloaded {len(paths)} model(s)")
            
            # Create symlink
            downloader.create_symlink('yolo11x')
            
            # Verify
            for path in paths:
                downloader.verify_model(path)
        
        sys.exit(0)
    
    elif args.model:
        # Download specific model
        path = downloader.download_model(args.model, force=args.force)
        
        if path:
            # Ask to create symlink
            response = input(f"\nCreate best.pt → {args.model}.pt symlink? [Y/n]: ")
            if response.lower() != 'n':
                downloader.create_symlink(args.model)
            
            # Verify
            downloader.verify_model(path)
        
        sys.exit(0)
    
    elif args.all:
        # Download all models
        print("📥 Downloading all available models...")
        paths = downloader.download_all(force=args.force)
        
        if paths:
            print(f"\n✅ Downloaded {len(paths)} model(s)")
            
            # Create symlink to yolo11x
            downloader.create_symlink('yolo11x')
        
        sys.exit(0)
    
    else:
        # No action specified, show help
        parser.print_help()
        print("\n" + "="*60)
        print("📊 AVAILABLE MODELS:")
        print("="*60)
        
        for model_name, info in MODELS.items():
            star = "⭐" if info['recommended'] else "  "
            print(f"{star} {model_name:12s} - {info['description']}")
        
        print("\n💡 Quick start: python scripts/download_models.py --download")


if __name__ == "__main__":
    main()
