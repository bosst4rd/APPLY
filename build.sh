#!/bin/bash
#############################################################################
# APPLY - Configuration Migration Tool - Build Script (Linux/Mac)
#
# Erstellt eine ZIP-Datei mit allen Dateien zum Testen
#############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  APPLY - Configuration Migration Tool - Build Script      ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Configuration
VERSION="2.3.0"
TIMESTAMP=$(date +"%Y%m%d_%H%M")
ZIPNAME="APPLY_v${VERSION}_${TIMESTAMP}.zip"
LATEST="APPLY_latest.zip"

echo -e "${BLUE}[INFO]${NC} Building release package..."
echo -e "${BLUE}[INFO]${NC} Version: $VERSION"
echo -e "${BLUE}[INFO]${NC} Timestamp: $TIMESTAMP"
echo ""

# Change to script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create releases folder if not exists
if [ ! -d "releases" ]; then
    echo -e "${BLUE}[INFO]${NC} Creating releases folder..."
    mkdir -p releases
fi

# Main files to include
FILES=(
    "main.py"
    "gui.py"
    "collect_parser.py"
    "config_applier.py"
    "example_collect_data.json"
    "requirements.txt"
    "start.sh"
    "start.bat"
)

# Optional documentation
DOCS=("README.md" "QUICKSTART.md" "INSTALL_PYTHON.md")

# Check if all required files exist
echo -e "${BLUE}[INFO]${NC} Checking files..."
MISSING=0
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}[OK]${NC} $file"
    else
        echo -e "${RED}[ERROR]${NC} Missing file: $file"
        MISSING=1
    fi
done

# Check documentation (optional)
for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo -e "${GREEN}[OK]${NC} $doc"
        FILES+=("$doc")
    else
        echo -e "${BLUE}[INFO]${NC} Optional: $doc (not found)"
    fi
done

# Check expletus Collector folder
if [ -d "expletus Collector" ]; then
    echo -e "${GREEN}[OK]${NC} expletus Collector/"
else
    echo -e "${BLUE}[INFO]${NC} Optional: expletus Collector/ (not found)"
fi

if [ $MISSING -eq 1 ]; then
    echo ""
    echo -e "${RED}[ERROR]${NC} Some files are missing! Cannot create package."
    exit 1
fi

echo ""
echo -e "${BLUE}[INFO]${NC} All files found. Creating ZIP..."

# Create temporary build directory
BUILDDIR=$(mktemp -d)
trap "rm -rf $BUILDDIR" EXIT

# Copy main files
for file in "${FILES[@]}"; do
    cp "$file" "$BUILDDIR/"
done

# Copy expletus Collector folder if exists
if [ -d "expletus Collector" ]; then
    mkdir -p "$BUILDDIR/expletus Collector"
    cp -r "expletus Collector"/* "$BUILDDIR/expletus Collector/" 2>/dev/null || true
fi

# Create ZIP
cd "$BUILDDIR"
zip -r "$SCRIPT_DIR/releases/$ZIPNAME" . -x "*.pyc" -x "__pycache__/*" -x "*.DS_Store"
cd "$SCRIPT_DIR"

if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} Failed to create ZIP file!"
    exit 1
fi

# Also create/update latest version
cp "releases/$ZIPNAME" "releases/$LATEST"

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Build Complete!                                          ${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}[OK]${NC} Created: releases/$ZIPNAME"
echo -e "${GREEN}[OK]${NC} Updated: releases/$LATEST"
echo ""
echo "Included:"
echo "  - APPLY Tool (Python GUI)"
if [ -d "expletus Collector" ]; then
    echo "  - expletus Collector (PowerShell Scripts)"
fi
echo "  - Documentation"
echo ""

# Show file size
SIZE=$(ls -lh "releases/$ZIPNAME" | awk '{print $5}')
echo -e "${BLUE}[INFO]${NC} Package size: $SIZE"
echo ""
echo -e "${BLUE}[INFO]${NC} To test, extract the ZIP and run:"
echo "       ./start.sh (Linux/Mac)"
echo "       start.bat (Windows)"
echo ""
