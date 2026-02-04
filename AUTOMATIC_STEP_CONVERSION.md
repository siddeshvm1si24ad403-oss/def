# Enabling Automatic STEP File Conversion

## Overview

The 3D CAD Viewer can **automatically convert STEP files** if you have FreeCAD or CadQuery installed. The app will try multiple methods and fall back gracefully if none are available.

## Conversion Methods (Automatic Detection)

The app tries these methods in order:

1. **FreeCAD Python Module** (Best)
2. **CadQuery Library** (Alternative)
3. **FreeCAD Command Line** (Fallback)
4. **Manual Instructions** (If all fail)

---

## Option 1: Install FreeCAD (Recommended)

### macOS
```bash
# Using Homebrew (easiest)
brew install --cask freecad

# After installation, add to Python path (optional)
export PYTHONPATH=/Applications/FreeCAD.app/Contents/Resources/lib:$PYTHONPATH

# Add to your ~/.zshrc or ~/.bash_profile to make permanent
echo 'export PYTHONPATH=/Applications/FreeCAD.app/Contents/Resources/lib:$PYTHONPATH' >> ~/.zshrc
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install freecad

# For Python integration
sudo apt install freecad-python3
```

### Windows
1. Download from: https://www.freecadweb.org/downloads.php
2. Run installer
3. Add to PATH:
   - Right-click "This PC" → Properties
   - Advanced System Settings → Environment Variables
   - Add to PATH: `C:\Program Files\FreeCAD\bin`

---

## Option 2: Install CadQuery (Alternative)

CadQuery is a Python library that can also handle STEP files:

```bash
# Using conda (recommended)
conda install -c conda-forge cadquery

# Or using pip (may have dependency issues)
pip install cadquery
```

---

## Verifying Installation

### Test FreeCAD Installation

```bash
# Try importing FreeCAD in Python
python3 -c "import sys; sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib'); import FreeCAD; print('FreeCAD version:', FreeCAD.Version())"
```

If this works, the app will automatically use FreeCAD!

### Test CadQuery Installation

```bash
python3 -c "import cadquery as cq; print('CadQuery installed successfully')"
```

---

## How Automatic Conversion Works

When you upload a STEP file, the app:

1. **Detects** it's a STEP file (`.step` or `.stp`)
2. **Tries FreeCAD**: Looks for FreeCAD installation
   - Searches common installation paths
   - Attempts to import FreeCAD Python module
   - Uses it to convert STEP → STL → OBJ
3. **Tries CadQuery**: If FreeCAD not found
   - Imports CadQuery library
   - Converts STEP → STL → OBJ
4. **Tries FreeCAD CLI**: Command line conversion
   - Searches for `freecadcmd` executable
   - Creates temporary conversion script
   - Runs FreeCAD in background
5. **Shows Instructions**: If all methods fail
   - Provides installation instructions
   - Suggests online converter
   - Explains how to proceed

---

## Troubleshooting

### FreeCAD Not Detected

**Problem**: You installed FreeCAD but app doesn't find it

**Solutions**:

1. **Add to Python path**:
```bash
# macOS
export PYTHONPATH=/Applications/FreeCAD.app/Contents/Resources/lib:$PYTHONPATH

# Linux
export PYTHONPATH=/usr/lib/freecad/lib:$PYTHONPATH

# Windows
set PYTHONPATH=C:\Program Files\FreeCAD\bin
```

2. **Restart the app** after installation

3. **Check FreeCAD installation path**:
```bash
# macOS
ls /Applications/FreeCAD.app/Contents/Resources/lib

# Linux
ls /usr/lib/freecad/lib

# Windows
dir "C:\Program Files\FreeCAD\bin"
```

### Import Errors

**Problem**: "ImportError: No module named 'FreeCAD'"

**Solution**:
```bash
# Run the app with FreeCAD in path
PYTHONPATH=/Applications/FreeCAD.app/Contents/Resources/lib streamlit run cad_viewer_app.py
```

Or create a launch script:

```bash
#!/bin/bash
# launch_cad_viewer.sh
export PYTHONPATH=/Applications/FreeCAD.app/Contents/Resources/lib:$PYTHONPATH
streamlit run cad_viewer_app.py
```

### Conversion Still Fails

**If automatic conversion fails**, you can:

1. **Convert manually in FreeCAD**:
   - Open FreeCAD
   - File → Open → your STEP file
   - File → Export → STL
   - Upload STL to the viewer

2. **Use online converter**:
   - https://anyconv.com/step-to-stl-converter/
   - Upload STEP, download STL
   - Upload STL to viewer

---

## Advanced: Custom FreeCAD Path

If FreeCAD is installed in a non-standard location, edit the app:

```python
# In cad_viewer_app.py, find the convert_step_to_obj function
# Add your custom path:

freecad_paths = [
    '/Applications/FreeCAD.app/Contents/Resources/lib',  # macOS
    '/usr/lib/freecad/lib',  # Linux
    'C:\\Program Files\\FreeCAD\\bin',  # Windows
    '/your/custom/path/to/freecad',  # Add your path here
]
```

---

## Testing the Conversion

After installing FreeCAD/CadQuery:

1. **Restart the Streamlit app**
2. **Upload a STEP file**
3. **Click "Process File"**
4. **Watch the conversion messages**:
   - ✅ "FreeCAD found! Converting STEP file..." = Success!
   - ⚠️ "FreeCAD not found, trying alternative methods..." = Trying fallbacks
   - ❌ "Automatic STEP conversion failed" = Manual conversion needed

---

## Recommended Setup

For best results:

```bash
# 1. Install FreeCAD
brew install --cask freecad  # macOS
# or download from freecadweb.org

# 2. Add to shell profile
echo 'export PYTHONPATH=/Applications/FreeCAD.app/Contents/Resources/lib:$PYTHONPATH' >> ~/.zshrc

# 3. Restart terminal

# 4. Run the app
streamlit run cad_viewer_app.py

# Now STEP files will convert automatically! 🎉
```

---

## Performance Notes

**Conversion Time**:
- Small STEP files (<1MB): 5-15 seconds
- Medium STEP files (1-10MB): 15-60 seconds
- Large STEP files (>10MB): 1-5 minutes

**Factors affecting speed**:
- Complexity of STEP geometry
- Number of parts/surfaces
- Computer performance
- FreeCAD version

---

## Benefits of Automatic Conversion

✅ **Seamless workflow**: Upload STEP → Get 3D view automatically
✅ **No manual steps**: No need to use external tools
✅ **Batch processing**: Process multiple files easily
✅ **Consistent quality**: Same conversion settings every time
✅ **Error handling**: Graceful fallbacks if conversion fails

---

## Summary

**Quick Setup** (macOS):
```bash
brew install --cask freecad
export PYTHONPATH=/Applications/FreeCAD.app/Contents/Resources/lib:$PYTHONPATH
streamlit run cad_viewer_app.py
```

**Then**: Just upload STEP files and they'll convert automatically! 🚀

---

*For help, see the main USER_GUIDE.md or STEP_FILES_GUIDE.md*
