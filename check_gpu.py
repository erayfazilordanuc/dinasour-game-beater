"""
GPU Detection Script - Check if your GPU is properly detected by Python
"""

import torch
import subprocess
import platform

def check_gpu():
    """Check GPU availability and details"""
    
    print("=" * 60)
    print("GPU Detection Check")
    print("=" * 60)
    
    # System Information
    print(f"\n📱 System Information:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Python Version: {platform.python_version()}")
    print(f"   PyTorch Version: {torch.__version__}")
    
    # Check NVIDIA GPU
    print(f"\n🎮 NVIDIA GPU Detection:")
    try:
        nvidia_output = subprocess.check_output(['nvidia-smi']).decode()
        gpu_available = torch.cuda.is_available()
        print(f"   CUDA Available: {gpu_available}")
        if gpu_available:
            print(f"   GPU Count: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"   GPU {i}: {torch.cuda.get_device_name(i)}")
                device = torch.device(f'cuda:{i}')
                props = torch.cuda.get_device_properties(device)
                print(f"      Memory: {props.total_memory / 1e9:.2f} GB")
        else:
            print("   ❌ CUDA is not available")
    except FileNotFoundError:
        print("   ⚠️  nvidia-smi not found - NVIDIA GPU likely not detected")
    except Exception as e:
        print(f"   ⚠️  Error checking NVIDIA GPU: {e}")
    
    # Check Apple Silicon GPU (MPS)
    print(f"\n🍎 Apple Silicon GPU Detection (MPS):")
    try:
        mps_available = torch.backends.mps.is_available()
        print(f"   MPS Available: {mps_available}")
        if mps_available:
            print(f"   ✅ Metal Performance Shaders (MPS) is available!")
        else:
            print(f"   ℹ️  MPS is not available on this system")
    except Exception as e:
        print(f"   ⚠️  Error checking MPS: {e}")
    
    # Summary and Recommendation
    print(f"\n{'=' * 60}")
    print("Summary & Recommendations:")
    print(f"{'=' * 60}")
    
    if torch.cuda.is_available():
        device = torch.device('cuda')
        print(f"✅ Use device parameter: device=0")
        print(f"   Example: yolo detect train ... device=0")
    elif torch.backends.mps.is_available():
        print(f"✅ Use device parameter: device=mps")
        print(f"   Example: yolo detect train ... device=mps")
    else:
        print(f"ℹ️  No GPU detected, falling back to CPU")
        print(f"   Use device parameter: device=cpu")
        print(f"   Example: yolo detect train ... device=cpu")
    
    print(f"{'=' * 60}\n")

if __name__ == "__main__":
    check_gpu()
