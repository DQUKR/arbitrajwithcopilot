"""
Health Check Script - Verify all components
Run this before deploying to make sure everything is OK
"""

import os
import sys
import importlib.util

def check_python_version():
    """Check Python version"""
    print("=" * 50)
    print("PYTHON VERSION CHECK")
    print("=" * 50)
    
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("? Python version is compatible (3.8+)")
        return True
    else:
        print("? Python version too old (need 3.8+)")
        return False

def check_files():
    """Check if all required files exist"""
    print("\n" + "=" * 50)
    print("FILE STRUCTURE CHECK")
    print("=" * 50)
    
    required_files = [
        'app.py',
        'config.py',
        'data_fetcher.py',
        'data_manager.py',
        'price_analyzer.py',
        'commission_calculator.py',
        'requirements.txt',
        'README.md',
        'run.bat',
        'run.sh',
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"? {file}")
        else:
            print(f"? {file} - MISSING!")
            all_exist = False
    
    return all_exist

def check_imports():
    """Check if all required modules can be imported"""
    print("\n" + "=" * 50)
    print("MODULE IMPORT CHECK")
    print("=" * 50)
    
    required_modules = {
        'streamlit': 'Streamlit (UI Framework)',
        'pandas': 'Pandas (Data Processing)',
        'numpy': 'NumPy (Numerical Computing)',
        'requests': 'Requests (HTTP Client)',
        'bs4': 'BeautifulSoup (Web Scraping)',
        'openpyxl': 'OpenPyXL (Excel Export)',
    }
    
    all_available = True
    for module, description in required_modules.items():
        try:
            __import__(module)
            print(f"? {module:<15} - {description}")
        except ImportError:
            print(f"? {module:<15} - {description} - NOT INSTALLED")
            all_available = False
    
    return all_available

def check_code_syntax():
    """Check Python code syntax"""
    print("\n" + "=" * 50)
    print("CODE SYNTAX CHECK")
    print("=" * 50)
    
    python_files = [
        'app.py',
        'config.py',
        'data_fetcher.py',
        'data_manager.py',
        'price_analyzer.py',
        'commission_calculator.py',
    ]
    
    all_valid = True
    for file in python_files:
        if not os.path.exists(file):
            print(f"? {file} - FILE NOT FOUND")
            all_valid = False
            continue
        
        try:
            with open(file, 'r', encoding='utf-8') as f:
                compile(f.read(), file, 'exec')
            print(f"? {file}")
        except SyntaxError as e:
            print(f"? {file} - SYNTAX ERROR: {e}")
            all_valid = False
        except Exception as e:
            print(f"? {file} - ERROR: {e}")
            all_valid = False
    
    return all_valid

def check_config():
    """Check configuration"""
    print("\n" + "=" * 50)
    print("CONFIGURATION CHECK")
    print("=" * 50)
    
    try:
        import config
        
        checks = [
            ('REQUESTS_TIMEOUT', config.REQUESTS_TIMEOUT),
            ('STEAM_COMMISSION_RATE', config.STEAM_COMMISSION_RATE),
            ('SITE_COMMISSIONS', len(config.SITE_COMMISSIONS)),
            ('PRODUCT_TYPES', len(config.PRODUCT_TYPES)),
            ('USER_AGENTS', len(config.USER_AGENTS)),
        ]
        
        all_valid = True
        for name, value in checks:
            if value:
                print(f"? {name}: {value}")
            else:
                print(f"? {name}: {value} - INVALID")
                all_valid = False
        
        return all_valid
    except Exception as e:
        print(f"? Configuration error: {e}")
        return False

def check_data_modules():
    """Check data modules can be imported"""
    print("\n" + "=" * 50)
    print("DATA MODULES CHECK")
    print("=" * 50)
    
    try:
        from data_manager import DataManager
        print("? DataManager can be imported")
        
        from commission_calculator import CommissionCalculator
        print("? CommissionCalculator can be imported")
        
        from price_analyzer import PriceAnalyzer
        print("? PriceAnalyzer can be imported")
        
        from data_fetcher import DataFetcher
        print("? DataFetcher can be imported")
        
        return True
    except Exception as e:
        print(f"? Module import error: {e}")
        return False

def check_requirements():
    """Check if requirements.txt is valid"""
    print("\n" + "=" * 50)
    print("REQUIREMENTS.TXT CHECK")
    print("=" * 50)
    
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
            packages = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
            print(f"? Found {len(packages)} packages")
            
            for package in packages:
                print(f"  - {package}")
            return True
    except Exception as e:
        print(f"? Requirements file error: {e}")
        return False

def main():
    """Run all checks"""
    print("\n")
    print("?" + "=" * 48 + "?")
    print("?" + " CS2 ARBITRAGE APPLICATION - HEALTH CHECK ".center(48) + "?")
    print("?" + "=" * 48 + "?")
    
    results = {
        'Python Version': check_python_version(),
        'File Structure': check_files(),
        'Requirements': check_requirements(),
        'Code Syntax': check_code_syntax(),
        'Configuration': check_config(),
        'Data Modules': check_data_modules(),
        'Module Imports': check_imports(),
    }
    
    print("\n" + "=" * 50)
    print("HEALTH CHECK SUMMARY")
    print("=" * 50)
    
    for check_name, result in results.items():
        status = "? PASS" if result else "? FAIL"
        print(f"{check_name:<30} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 50)
    if all_passed:
        print("? ALL CHECKS PASSED - APPLICATION READY!")
        print("=" * 50)
        print("\nTo start the application, run:")
        print("  streamlit run app.py")
        return 0
    else:
        print("? SOME CHECKS FAILED - FIX ISSUES BEFORE RUNNING")
        print("=" * 50)
        print("\nRun this to install missing packages:")
        print("  pip install -r requirements.txt --upgrade")
        return 1

if __name__ == "__main__":
    sys.exit(main())
