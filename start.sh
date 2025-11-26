#!/bin/bash
#############################################################################
# APPLY - Start Script (Linux/Mac)
#
# Dieses Skript prüft alle Abhängigkeiten und startet das Tool
#############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  APPLY - Startup Check    ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Function to print status messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if running as root (warn if yes)
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root/sudo is not recommended for the GUI application"
    print_warning "The tool will ask for permissions when needed during actual migration"
    echo ""
fi

# 1. Check Python version - Try python3 first, then python
print_status "Checking Python installation..."

PYTHON_CMD=""

# Try python3 first (preferred)
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
# Try python as fallback
elif command -v python &> /dev/null; then
    # Check if it's Python 3
    PYTHON_VERSION_CHECK=$(python -c 'import sys; print(sys.version_info.major)' 2>/dev/null || echo "0")
    if [ "$PYTHON_VERSION_CHECK" = "3" ]; then
        PYTHON_CMD="python"
    else
        print_error "Found 'python' but it's Python 2 (version $PYTHON_VERSION_CHECK)"
        PYTHON_CMD=""
    fi
fi

# If no suitable Python found, show error
if [ -z "$PYTHON_CMD" ]; then
    print_error "Python 3 is not installed or not found in PATH!"
    echo ""
    echo "Please install Python 3.7 or higher:"
    echo ""

    # Detect OS and provide specific instructions
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        case "$ID" in
            ubuntu|debian)
                echo "  sudo apt-get update"
                echo "  sudo apt-get install python3 python3-tk"
                ;;
            fedora|rhel|centos)
                echo "  sudo dnf install python3 python3-tkinter"
                ;;
            arch|manjaro)
                echo "  sudo pacman -S python python-tk"
                ;;
            *)
                echo "  Please install Python 3 for your distribution"
                ;;
        esac
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  brew install python3"
        echo "  or download from: https://www.python.org/downloads/"
    else
        echo "  Ubuntu/Debian: sudo apt-get install python3 python3-tk"
        echo "  Fedora/RHEL:   sudo dnf install python3 python3-tkinter"
        echo "  macOS:         brew install python3"
    fi
    echo ""
    echo "After installation, restart your terminal and run this script again."
    exit 1
fi

# Get Python version
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')

print_success "Python $PYTHON_VERSION found (using '$PYTHON_CMD' command)"

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    print_error "Python 3.7 or higher is required (found $PYTHON_VERSION)"
    echo ""
    echo "Please upgrade your Python installation:"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  brew upgrade python3"
    else
        echo "  Visit https://www.python.org/downloads/ to download a newer version"
    fi
    exit 1
fi

# 2. Check tkinter availability
print_status "Checking tkinter (GUI library)..."
if $PYTHON_CMD -c "import tkinter" 2>/dev/null; then
    print_success "tkinter is available"
else
    print_error "tkinter is not installed!"
    echo ""
    echo "tkinter is required for the GUI. Please install it:"
    echo ""

    # Detect OS and provide specific instructions
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        case "$ID" in
            ubuntu|debian)
                echo "  sudo apt-get update"
                echo "  sudo apt-get install python3-tk"
                ;;
            fedora|rhel|centos)
                echo "  sudo dnf install python3-tkinter"
                ;;
            arch|manjaro)
                echo "  sudo pacman -S tk"
                ;;
            opensuse*)
                echo "  sudo zypper install python3-tk"
                ;;
            *)
                echo "  Please install python3-tkinter for your distribution"
                ;;
        esac
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  tkinter should be included with Python on macOS"
        echo "  If missing, reinstall Python: brew reinstall python@3"
    fi
    echo ""
    echo "After installation, restart your terminal and run this script again."
    exit 1
fi

# 3. Check if we're in the correct directory
print_status "Checking working directory..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

if [ ! -f "main.py" ] || [ ! -f "gui.py" ]; then
    print_error "Required Python files not found!"
    echo "Please ensure you're running this script from the APPLY directory"
    exit 1
fi

print_success "Working directory: $SCRIPT_DIR"

# 4. Check for example data file
print_status "Checking example data file..."
if [ -f "example_collect_data.json" ]; then
    print_success "Example data file found"
else
    print_warning "example_collect_data.json not found (optional)"
fi

# 5. Check Python module imports
print_status "Checking Python modules..."
MISSING_MODULES=0

check_module() {
    if $PYTHON_CMD -c "import $1" 2>/dev/null; then
        print_success "Module '$1' available"
    else
        print_error "Module '$1' missing"
        MISSING_MODULES=1
    fi
}

check_module "json"
check_module "os"
check_module "subprocess"
check_module "pathlib"
check_module "typing"
check_module "threading"
check_module "platform"

if [ $MISSING_MODULES -eq 1 ]; then
    print_error "Some required Python modules are missing"
    echo "These are standard library modules and should be included with Python"
    exit 1
fi

# 6. Check file permissions
print_status "Checking file permissions..."
if [ ! -x "main.py" ]; then
    print_warning "main.py is not executable, fixing..."
    chmod +x main.py
    print_success "main.py is now executable"
else
    print_success "File permissions OK"
fi

# 7. Display system information
echo ""
print_status "System Information:"
echo "  OS: $(uname -s)"
echo "  Architecture: $(uname -m)"
echo "  Python: $PYTHON_VERSION"
echo "  Hostname: $(hostname)"
echo ""

# 8. Check if display is available (for GUI)
print_status "Checking display availability..."
if [ -z "$DISPLAY" ] && [[ "$OSTYPE" != "darwin"* ]]; then
    print_warning "No DISPLAY environment variable set"
    echo ""
    echo "The GUI requires a display. Options:"
    echo "  1. Run on a system with graphical environment"
    echo "  2. Use X11 forwarding: ssh -X user@host"
    echo "  3. Use VNC or similar remote desktop"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    print_success "Display available"
fi

# All checks passed
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  All dependency checks passed! ✓                         ${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Display usage hints
echo -e "${BLUE}Quick Start:${NC}"
echo "  1. The GUI will open automatically"
echo "  2. Click 'Durchsuchen...' and select a COLLECT JSON file"
echo "  3. Choose configurations with checkboxes"
echo "  4. Enable 'Dry Run' for testing (recommended first!)"
echo "  5. Click 'Konfigurationen anwenden'"
echo ""
echo -e "${YELLOW}Important:${NC}"
echo "  - Always test with Dry Run first!"
echo "  - Create a backup before real migration"
echo "  - Check the log output for errors"
echo ""

# Ask to continue
read -p "Press ENTER to start eXpletus APPLY..."
echo ""

# Start the application
print_status "Starting eXpletus APPLY..."
print_status "Using Python command: $PYTHON_CMD"
echo ""

$PYTHON_CMD main.py

# Capture exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    print_success "Tool exited successfully"
else
    print_error "Tool exited with error code: $EXIT_CODE"
fi

exit $EXIT_CODE
