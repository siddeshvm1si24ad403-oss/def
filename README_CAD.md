# 3D CAD File Viewer & Analyzer

A comprehensive web application for visualizing and analyzing STEP and STL files with automatic format conversion and geometric data extraction.

## 🎯 Features

### File Processing Pipeline
1. **Upload** STEP or STL files
2. **Automatic Conversion**: STEP/STL → OBJ → GLB
3. **3D Visualization** with interactive viewer
4. **Geometric Analysis** with detailed metrics
5. **Feature Detection** and operations analysis

### Capabilities

#### 🔄 Format Conversion
- **Input**: STEP (.step, .stp) and STL (.stl) files
- **Process**: Automatic conversion through OBJ intermediate format
- **Output**: GLB format for web visualization + OBJ export

#### 🎨 3D Viewer
- Interactive 3D model visualization using Three.js
- Mouse controls: Rotate, zoom, pan
- Professional lighting and grid system
- Automatic model centering and scaling
- Real-time rendering

#### 📊 Geometric Data Extraction
- **Mesh Statistics**:
  - Vertex count
  - Face count
  - Edge count
  - Euler number

- **Physical Properties**:
  - Volume calculation
  - Surface area
  - Bounding box dimensions
  - Centroid position

- **Quality Metrics**:
  - Watertight check (closed solid)
  - Convex hull analysis
  - Topology validation

#### ⚙️ Operations & Feature Detection
- Solid body validation
- Topology analysis (holes, genus)
- Space utilization metrics
- Mesh quality assessment
- Automated feature recognition

## 🚀 Quick Start

### Installation

1. **Install Python dependencies**:
```bash
pip install -r requirements_cad.txt
```

2. **Run the application**:
```bash
streamlit run cad_viewer_app.py
```

3. **Access the app**:
Open your browser at `http://localhost:8501`

## 📖 Usage Guide

### Step 1: Upload File
- Click "Browse files" in the sidebar
- Select a STEP (.step, .stp) or STL (.stl) file
- Click "Process File"

### Step 2: View Conversion Progress
The app will automatically:
1. Convert your file to OBJ format
2. Convert OBJ to GLB for web viewing
3. Extract all geometric data
4. Analyze features and operations

### Step 3: Explore Results

#### 3D Viewer Tab
- **Interact** with your 3D model
- **Rotate**: Left-click and drag
- **Zoom**: Mouse wheel
- **Pan**: Right-click and drag
- **Download**: Export as GLB file

#### Geometric Data Tab
- View detailed measurements
- Check mesh statistics
- Analyze dimensions and bounds
- Export data as JSON

#### Operations Tab
- See detected features
- Review model quality
- Check topology information
- Analyze space utilization

## 📊 Data Output

### Geometric Data (JSON)
```json
{
  "vertices_count": 1234,
  "faces_count": 2468,
  "volume": 125.67,
  "surface_area": 234.56,
  "dimensions": {
    "x": 10.5,
    "y": 8.3,
    "z": 12.1
  },
  "is_watertight": true,
  "centroid": [0.0, 0.0, 0.0]
}
```

### Operations Detected
- Solid body validation
- Watertight analysis
- Topology features
- Hole detection
- Mesh quality metrics

## 🔧 Technical Details

### Supported Formats

**Input**:
- STEP files (.step, .stp) - CAD standard format
- STL files (.stl) - Mesh format

**Output**:
- GLB (GL Transmission Format Binary) - for 3D viewer
- OBJ (Wavefront) - intermediate format
- JSON - geometric data export

### Technology Stack

- **Backend**: Python with Streamlit
- **3D Processing**: Trimesh, numpy-stl
- **Visualization**: Three.js (WebGL)
- **UI**: Streamlit components

### Architecture

```
Upload File
    ↓
STEP/STL → OBJ (Trimesh conversion)
    ↓
OBJ → GLB (Trimesh export)
    ↓
Geometric Analysis (Trimesh)
    ↓
Feature Detection (Custom algorithms)
    ↓
3D Visualization (Three.js + WebGL)
```

## ⚠️ Important Notes

### STEP File Support
- STEP conversion uses a simplified pipeline through Trimesh
- For production use with complex STEP files, consider:
  - **pythonocc** (OpenCASCADE wrapper)
  - **CAD Exchanger SDK**
  - **FreeCAD Python API**
  - **Assimp library**

### Performance Considerations
- Large models (>100K faces) may take longer to process
- Browser performance depends on GPU capabilities
- Complex STEP assemblies may need specialized parsers

## 🔄 Upgrading STEP Support

For professional STEP file handling, replace the `convert_step_to_obj` function:

```python
# Using pythonocc (requires separate installation)
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh

def convert_step_to_obj_advanced(step_path, obj_path):
    reader = STEPControl_Reader()
    reader.ReadFile(step_path)
    reader.TransferRoots()
    shape = reader.OneShape()
    
    # Convert to mesh and export
    # ... (implementation details)
```

## 🛠️ Customization

### Adding Custom Analysis
Edit the `analyze_operations()` function to add:
- Custom feature detection
- Manufacturing analysis
- Cost estimation
- Material properties

### Styling the Viewer
Modify the HTML in `create_3d_viewer_html()`:
- Change colors and lighting
- Add measurement tools
- Include cross-sections
- Add annotations

## 📦 Export Options

- **GLB File**: For use in other 3D applications
- **Geometric Data**: JSON format for further analysis
- **Screenshots**: Capture from the viewer

## 🐛 Troubleshooting

**"Error converting STEP to OBJ"**:
- STEP files may need specialized parsers
- Try converting to STL first using CAD software
- Check file integrity

**"Model not displaying"**:
- Check file size (<100MB recommended)
- Verify file is not corrupted
- Try refreshing the page

**"Geometric data missing"**:
- Ensure model is properly closed
- Check for degenerate faces
- Validate mesh topology

## 📚 Resources

- [Trimesh Documentation](https://trimsh.org/)
- [Three.js Documentation](https://threejs.org/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🤝 Contributing

To enhance STEP support:
1. Install pythonocc or CAD Exchanger
2. Replace conversion functions
3. Add advanced geometry extraction
4. Implement feature recognition

## 📄 License

This application uses open-source libraries. Check individual library licenses for commercial use.

## 🎓 Learning Resources

- **CAD Format Specs**: ISO 10303 (STEP), STL specification
- **3D Geometry**: Computational geometry fundamentals
- **WebGL**: Three.js tutorials for 3D web graphics

---

**Need Help?** Check the Streamlit logs for detailed error messages during processing.
