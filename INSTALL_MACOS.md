# macOS Installation Guide for 3D CAD Viewer

## Issue: OpenBLAS Dependency Error

If you're getting the OpenBLAS error on macOS, here are the solutions:

## Solution 1: Install Pre-built Binaries (Recommended)

```bash
# Install using conda (easiest)
conda install -c conda-forge streamlit trimesh numpy pillow scipy

# Or use the simplified requirements (without scipy)
pip install -r requirements_cad_simple.txt
```

## Solution 2: Install OpenBLAS via Homebrew

```bash
# Install Homebrew dependencies
brew install openblas lapack

# Set environment variables
export LDFLAGS="-L/opt/homebrew/opt/openblas/lib"
export CPPFLAGS="-I/opt/homebrew/opt/openblas/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/openblas/lib/pkgconfig"

# Then install requirements
pip install -r requirements_cad.txt
```

## Solution 3: Use Pre-built Wheels (Fastest)

```bash
# Install packages one by one with pre-built wheels
pip install streamlit
pip install trimesh
pip install numpy
pip install pillow

# Skip scipy or install from conda
# pip install scipy  # might fail
conda install scipy  # use conda instead
```

## Solution 4: Simplified Version (No scipy)

The app works fine without scipy! Use this simpler version:

```bash
pip install -r requirements_cad_simple.txt
```

Then run normally:
```bash
streamlit run cad_viewer_app.py
```

## Using Conda (Best for macOS)

```bash
# Create conda environment
conda create -n cad_viewer python=3.11
conda activate cad_viewer

# Install all packages via conda
conda install -c conda-forge streamlit trimesh numpy pillow scipy

# Run the app
streamlit run cad_viewer_app.py
```

## Verification

Test if everything works:
```bash
python test_conversion.py
```

This will create a sample cube and test the conversion pipeline.

## Notes

- Trimesh will work without scipy, just with reduced functionality
- The main features (STL/OBJ/GLB conversion and visualization) work fine
- scipy is only needed for advanced mesh operations

## Still Having Issues?

Try this minimal install:
```bash
pip install --upgrade pip
pip install streamlit trimesh[easy] numpy pillow
```

The `[easy]` option installs trimesh with minimal dependencies.
