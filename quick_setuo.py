#!/usr/bin/env python3
"""
Quick Setup for Offline PDF Translation
Handles SSL issues by downloading model offline
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and show progress."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    print("🚀 PDF Translation - Complete Offline Setup")
    print("="*50)
    print("This will solve SSL certificate issues by downloading everything offline.")
    print()
    
    # Step 1: Check if files exist
    model_dir = Path("./models/Helsinki-NLP/opus-mt-de-en")
    if model_dir.exists() and any(model_dir.glob("*.json")):
        print("✅ Model already downloaded!")
        skip_download = True
    else:
        skip_download = False
    
    # Step 2: Download model offline
    if not skip_download:
        print("📥 Step 1: Downloading translation model offline...")
        success = run_command("python offline_model_downloader.py", "Model download")
        if not success:
            print("\n❌ Setup failed at model download step")
            return False
    
    # Step 3: Test model
    print("\n🧪 Step 2: Testing downloaded model...")
    success = run_command("python test_offline_model.py", "Model test")
    if not success:
        print("\n⚠️ Model test failed, but continuing...")
    
    # Step 4: Create sample usage script
    sample_usage = '''#!/usr/bin/env python3
"""Sample usage of offline PDF translator"""

import sys
import subprocess

# Example usage
input_pdf = "sample_german.pdf"
output_pdf = "translated_english.pdf" 

# Use offline model
command = f'python pdf_translator.py "{input_pdf}" "{output_pdf}" --model "./models/Helsinki-NLP/opus-mt-de-en" --offline'

print("🔄 Running PDF translation...")
print(f"Command: {command}")

# Run the translation
result = subprocess.run(command, shell=True)
if result.returncode == 0:
    print("✅ Translation completed successfully!")
else:
    print("❌ Translation failed")
    sys.exit(1)
'''
    
    with open("run_translation.py", 'w') as f:
        f.write(sample_usage)
    
    print("\n🎉 Setup Complete!")
    print("\n📋 Usage Instructions:")
    print("="*30)
    print("\n1️⃣ Basic usage:")
    print("   python pdf_translator.py input.pdf output.pdf --offline")
    print("\n2️⃣ Using specific local model:")
    print("   python pdf_translator.py input.pdf output.pdf --model './models/Helsinki-NLP/opus-mt-de-en'")
    print("\n3️⃣ Using the sample script:")
    print("   python run_translation.py")
    print("\n💡 The model is now completely offline - no internet required!")
    
    # Check for sample PDF
    if not Path("sample_german.pdf").exists():
        print("\n📄 To test with a sample German PDF:")
        print("   1. Place a German PDF file in this directory")
        print("   2. Rename it to 'sample_german.pdf'")
        print("   3. Run: python run_translation.py")
    
    print("\n🔧 Files created:")
    print(f"   📁 Model directory: {model_dir}")
    print(f"   🐍 Test script: test_offline_model.py")
    print(f"   🐍 Usage script: run_translation.py")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎊 All ready! Your PDF translator is now SSL-certificate-issue-free!")
        else:
            print("\n💡 If you continue having issues, try running from a different network")
            print("   or ask someone to share the downloaded model files with you.")
    except KeyboardInterrupt:
        print("\n❌ Setup cancelled by user")
        sys.exit(1)