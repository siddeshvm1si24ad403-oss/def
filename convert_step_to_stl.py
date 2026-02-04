#!/usr/bin/env python3
"""
STEP to STL Converter
Converts STEP files to STL format for use with the 3D CAD Viewer

Usage: python convert_step_to_stl.py input.step output.stl
"""

import sys
import os

def convert_with_freecad(step_file, stl_file):
    """Convert using FreeCAD (if installed)"""
    try:
        import FreeCAD
        import Import
        import Mesh
        
        print("✅ FreeCAD detected - using for conversion")
        
        # Import STEP file
        print(f"📂 Loading STEP file: {step_file}")
        Import.insert(step_file, "Unnamed")
        
        # Get the imported objects
        doc = FreeCAD.ActiveDocument
        if not doc:
            doc = FreeCAD.newDocument("Temp")
            Import.insert(step_file, "Temp")
        
        # Export to STL
        print(f"💾 Exporting to STL: {stl_file}")
        objs = [obj for obj in doc.Objects]
        Mesh.export(objs, stl_file)
        
        print("✅ Conversion successful!")
        return True
        
    except ImportError:
        print("❌ FreeCAD not found")
        return False
    except Exception as e:
        print(f"❌ Error during FreeCAD conversion: {e}")
        return False

def convert_with_cadquery(step_file, stl_file):
    """Convert using CadQuery (if installed)"""
    try:
        import cadquery as cq
        
        print("✅ CadQuery detected - using for conversion")
        
        # Import STEP
        print(f"📂 Loading STEP file: {step_file}")
        result = cq.importers.importStep(step_file)
        
        # Export to STL
        print(f"💾 Exporting to STL: {stl_file}")
        result.val().exportStl(stl_file)
        
        print("✅ Conversion successful!")
        return True
        
    except ImportError:
        print("❌ CadQuery not found")
        return False
    except Exception as e:
        print(f"❌ Error during CadQuery conversion: {e}")
        return False

def print_usage():
    """Print usage instructions"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║               STEP to STL Converter                            ║
╚════════════════════════════════════════════════════════════════╝

Usage:
    python convert_step_to_stl.py input.step output.stl

Requirements (install at least one):

1. FreeCAD (Recommended):
   macOS:    brew install --cask freecad
   Linux:    sudo apt install freecad
   Windows:  Download from freecadweb.org
   
   After install, add to PATH or use:
   export PYTHONPATH=/Applications/FreeCAD.app/Contents/Resources/lib:$PYTHONPATH

2. CadQuery:
   conda install -c conda-forge cadquery

3. Online Converters (No installation):
   - https://anyconv.com/step-to-stl-converter/
   - https://www.greentoken.de/onlineconv.aspx
   - https://products.aspose.app/3d/conversion/step-to-stl

Alternative Methods:
   - Use FreeCAD GUI: File → Export → Select STL format
   - Use Blender: Import STEP addon + Export STL
   - Use online CAD tools
    """)

def main():
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)
    
    step_file = sys.argv[1]
    stl_file = sys.argv[2]
    
    # Check if input file exists
    if not os.path.exists(step_file):
        print(f"❌ Error: Input file not found: {step_file}")
        sys.exit(1)
    
    print("="*60)
    print("STEP to STL Conversion")
    print("="*60)
    print(f"Input:  {step_file}")
    print(f"Output: {stl_file}")
    print("="*60)
    print()
    
    # Try different converters
    success = False
    
    # Try FreeCAD first
    if not success:
        print("Trying FreeCAD...")
        success = convert_with_freecad(step_file, stl_file)
    
    # Try CadQuery
    if not success:
        print("\nTrying CadQuery...")
        success = convert_with_cadquery(step_file, stl_file)
    
    if not success:
        print("\n" + "="*60)
        print("❌ CONVERSION FAILED")
        print("="*60)
        print("\nNo suitable converter found!")
        print("\nPlease install one of the following:")
        print("  1. FreeCAD:  brew install --cask freecad")
        print("  2. CadQuery: conda install -c conda-forge cadquery")
        print("\nOr use an online converter:")
        print("  - https://anyconv.com/step-to-stl-converter/")
        print("  - https://www.greentoken.de/onlineconv.aspx")
        print()
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ CONVERSION COMPLETE!")
    print("="*60)
    print(f"\nYou can now upload {stl_file} to the 3D CAD Viewer!")
    print()

if __name__ == "__main__":
    main()
