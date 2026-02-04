#!/bin/bash
# STEP to STL Converter using FreeCAD's Python
# Usage: ./freecad_convert.sh input.step output.stl

if [ "$#" -ne 2 ]; then
    echo "Usage: ./freecad_convert.sh input.step output.stl"
    echo "Example: ./freecad_convert.sh 5X8_COUPLER.STEP 5X8_COUPLER.stl"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file not found: $INPUT_FILE"
    exit 1
fi

# Get absolute paths
INPUT_ABS=$(cd "$(dirname "$INPUT_FILE")" && pwd)/$(basename "$INPUT_FILE")
OUTPUT_ABS=$(cd "$(dirname "$OUTPUT_FILE")" && pwd)/$(basename "$OUTPUT_FILE")

echo "================================="
echo "STEP to STL Converter"
echo "================================="
echo "Input:  $INPUT_ABS"
echo "Output: $OUTPUT_ABS"
echo "================================="
echo ""

# Create Python script for FreeCAD
SCRIPT=$(cat <<PYTHON
import FreeCAD
import Import
import Mesh
import sys

try:
    print("Loading STEP file...")
    Import.insert("$INPUT_ABS", "TempDoc")
    doc = FreeCAD.ActiveDocument
    
    if not doc:
        doc = FreeCAD.newDocument("TempDoc")
        Import.insert("$INPUT_ABS", "TempDoc")
    
    print("Converting to STL...")
    objs = [obj for obj in doc.Objects]
    
    if len(objs) == 0:
        print("Error: No objects found in STEP file")
        sys.exit(1)
    
    Mesh.export(objs, "$OUTPUT_ABS")
    FreeCAD.closeDocument("TempDoc")
    
    print("Success! STL file created: $OUTPUT_ABS")
    sys.exit(0)
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
PYTHON
)

# Run FreeCAD's Python with the script
echo "$SCRIPT" | /Applications/FreeCAD.app/Contents/Resources/bin/python

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Conversion complete!"
    echo "📁 STL file: $OUTPUT_FILE"
    echo ""
    echo "You can now upload this STL file to the 3D CAD Viewer!"
else
    echo ""
    echo "❌ Conversion failed"
    echo ""
    echo "Alternative: Use online converter"
    echo "https://anyconv.com/step-to-stl-converter/"
fi
