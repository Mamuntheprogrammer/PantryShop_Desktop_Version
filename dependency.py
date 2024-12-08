
# From txt file
# pip install -r requirements.txt


import subprocess
import sys
import importlib.util

# List of packages to install
packages = [
    'loader==2017.9.11',
    'matplotlib==3.9.3',
    'packaging==24.2',
    'pandas==2.2.3',
    'reportlab==4.2.5',
    'tkcalendar==1.6.1',
    'ttkthemes==3.2.2'
]

# Function to check if a package is installed
def is_package_installed(package):
    # Try to find the package using importlib.util
    package_name = package.split('==')[0]  # Extract the package name (ignore version)
    spec = importlib.util.find_spec(package_name)
    return spec is not None

# Function to install the packages
def install_packages(packages):
    for package in packages:
        package_name = package.split('==')[0]  # Extract the package name
        if is_package_installed(package_name):
            print(f"Package '{package_name}' is already installed.")
        else:
            print(f"Package '{package_name}' is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install the packages
install_packages(packages)
