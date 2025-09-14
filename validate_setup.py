"""
Clinical Trial Copilot - Setup Validation Script
Validates that all components are properly configured and ready to use.
"""

import os
import sys
import importlib.util
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a required file exists."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} MISSING: {filepath}")
        return False


def check_directory_exists(dirpath, description):
    """Check if a required directory exists."""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}/")
        return True
    else:
        print(f"❌ {description} MISSING: {dirpath}/")
        return False


def check_python_module(module_path, module_name):
    """Check if a Python module can be imported."""
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None:
            print(f"❌ Cannot load module spec: {module_name}")
            return False
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"✅ Python module loads: {module_name}")
        return True
    except ImportError as e:
        print(f"⚠️  Module {module_name} has missing dependencies: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Python module error ({module_name}): {str(e)}")
        return False


def check_dependencies():
    """Check if required Python packages are installed."""
    # Package name -> import name mapping
    packages = {
        'pypdf': 'pypdf',
        'requests': 'requests', 
        'anthropic': 'anthropic',
        'pandas': 'pandas',
        'matplotlib': 'matplotlib',
        'python-dotenv': 'dotenv',  # python-dotenv imports as 'dotenv'
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn'
    }
    
    print("\n📦 Checking Python Dependencies:")
    all_deps_ok = True
    
    for package_name, import_name in packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - Run: pip install {package_name}")
            all_deps_ok = False
        except Exception as e:
            print(f"⚠️  {package_name} - Warning: {str(e)}")
    
    return all_deps_ok


def check_environment_variables():
    """Check if environment variables are properly configured."""
    print("\n🔑 Checking Environment Configuration:")
    
    env_file_exists = os.path.exists('.env')
    env_template_exists = os.path.exists('env_template.txt')
    
    if not env_file_exists and env_template_exists:
        print("❌ .env file not found")
        print("💡 Run: cp env_template.txt .env")
        print("   Then edit .env with your actual API keys")
        return False
    elif not env_file_exists:
        print("❌ .env file not found and no template available")
        return False
    
    print("✅ .env file exists")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        claude_key = os.getenv("CLAUDE_API_KEY")
        cerebras_key = os.getenv("CEREBRAS_API_KEY")
        
        if not claude_key or claude_key == "your_anthropic_api_key_here":
            print("❌ CLAUDE_API_KEY not properly set in .env")
            return False
        else:
            print("✅ CLAUDE_API_KEY configured")
        
        if not cerebras_key or cerebras_key == "your_cerebras_api_key_here":
            print("❌ CEREBRAS_API_KEY not properly set in .env")
            return False
        else:
            print("✅ CEREBRAS_API_KEY configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading environment: {str(e)}")
        return False


def validate_project_structure():
    """Validate the complete project structure."""
    print("🏗️ Clinical Trial Copilot - Setup Validation")
    print("=" * 50)
    
    structure_ok = True
    
    # Core files
    print("\n📁 Checking Project Structure:")
    structure_ok &= check_file_exists("main.py", "Main pipeline script")
    structure_ok &= check_file_exists("requirements.txt", "Dependencies file")
    structure_ok &= check_file_exists("README.md", "Project documentation")
    structure_ok &= check_file_exists("SETUP_INSTRUCTIONS.md", "Setup guide")
    structure_ok &= check_file_exists("env_template.txt", "Environment template")
    structure_ok &= check_file_exists("run_example.py", "Example runner")
    structure_ok &= check_file_exists(".gitignore", "Git ignore file")
    
    # Directories
    structure_ok &= check_directory_exists("src", "Source code directory")
    structure_ok &= check_directory_exists("data", "Input data directory")
    structure_ok &= check_directory_exists("outputs", "Output directory")
    
    # Source modules
    print("\n🐍 Checking Source Modules:")
    structure_ok &= check_file_exists("src/__init__.py", "Package init file")
    structure_ok &= check_file_exists("src/cerebras_client.py", "Cerebras client")
    structure_ok &= check_file_exists("src/claude_client.py", "Claude client")
    structure_ok &= check_file_exists("src/analysis.py", "Analysis engine")
    structure_ok &= check_file_exists("src/api.py", "FastAPI server")
    
    # Check if modules can be imported (only if dependencies are available)
    print("\n🔧 Checking Module Imports:")
    module_ok = True
    module_ok &= check_python_module("src/cerebras_client.py", "cerebras_client")
    module_ok &= check_python_module("src/claude_client.py", "claude_client")
    module_ok &= check_python_module("src/analysis.py", "analysis")
    module_ok &= check_python_module("main.py", "main")
    
    # Don't fail structure check if modules have dependency issues
    if not module_ok:
        print("⚠️  Some modules have dependency issues - this is normal if packages aren't installed yet")
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Check environment
    env_ok = check_environment_variables()
    
    # Final summary
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    if structure_ok and deps_ok and env_ok:
        print("✅ ALL CHECKS PASSED!")
        print("\n🚀 Your Clinical Trial Copilot is ready to use!")
        print("\n💡 Next steps:")
        print("   1. Place a clinical trial PDF in the data/ directory")
        print("   2. Run: python main.py data/your_file.pdf")
        print("   3. Or try: python run_example.py")
        return True
    else:
        print("❌ SOME CHECKS FAILED")
        print("\n🔧 Issues found:")
        if not structure_ok:
            print("   - Project structure incomplete")
        if not deps_ok:
            print("   - Missing Python dependencies")
        if not env_ok:
            print("   - Environment configuration issues")
        
        print("\n💡 Run the following to fix:")
        if not deps_ok:
            print("   py -m pip install pypdf requests anthropic pandas matplotlib python-dotenv fastapi uvicorn")
        if not env_ok:
            print("   copy env_template.txt .env")
            print("   # Then edit .env with your actual API keys")
        
        return False


if __name__ == "__main__":
    success = validate_project_structure()
    sys.exit(0 if success else 1)
