import streamlit as st
import trimesh
import numpy as np
import tempfile
import os
import json
from pathlib import Path
import base64

# Page configuration
st.set_page_config(
    page_title="3D CAD Viewer & Analyzer",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional CAD Interface
st.markdown("""
    <style>
    /* Global Layout */
    .main {
        padding: 0;
        background: #f8f9fa;
    }
    .block-container {
        padding: 0.5rem 1rem;
        max-width: 100%;
    }
    
    /* Professional Header */
    h1 {
        margin: 0;
        padding: 0.8rem 0;
        font-size: 1.5rem;
        font-weight: 600;
        color: #1a1a1a;
        border-bottom: 2px solid #0066cc;
    }
    
    /* Card Style Containers */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        margin-bottom: 0.8rem;
    }
    
    /* Metrics - Professional Card Style */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }
    .stMetric label {
        color: rgba(255,255,255,0.9);
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stMetric [data-testid="stMetricValue"] {
        font-size: 1.4rem;
        font-weight: 700;
        color: white;
    }
    
    /* Section Headers */
    h2, h3 {
        color: #2c3e50;
        font-weight: 600;
        margin-top: 0;
        margin-bottom: 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid #e0e0e0;
    }
    h2 { font-size: 1.1rem; }
    h3 { font-size: 1rem; }
    
    /* Data Text */
    p, .stMarkdown {
        color: #34495e;
        line-height: 1.6;
        margin-bottom: 0.3rem;
    }
    
    /* Buttons - Professional Style */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
        transition: all 0.3s;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Download Buttons */
    .stDownloadButton button {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        width: 100%;
        margin-bottom: 0.3rem;
    }
    .stDownloadButton button:hover {
        background: #667eea;
        color: white;
    }
    
    /* Remove unwanted spacing */
    .element-container { margin-bottom: 0; }
    hr { 
        margin: 0.5rem 0;
        border: none;
        border-top: 1px solid #e0e0e0;
    }
    
    /* Compact spacing */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        gap: 0.3rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Professional Title
st.markdown("# 🔧 CAD Viewer & Analysis Platform")
st.markdown("")  # Spacing

# Session state initialization
if 'model_data' not in st.session_state:
    st.session_state.model_data = None
if 'geometric_data' not in st.session_state:
    st.session_state.geometric_data = None

def convert_stl_to_obj(stl_path, obj_path):
    """Convert STL to OBJ format"""
    try:
        mesh_data = trimesh.load(stl_path)
        mesh_data.export(obj_path)
        return True, "STL → OBJ conversion successful"
    except Exception as e:
        return False, f"Error converting STL to OBJ: {str(e)}"

def convert_step_to_stl(step_path, stl_path):
    """Convert STEP to STL format using available converters"""
    
    # Try Method 1: FreeCAD Python Module
    try:
        st.info("🔄 Converting STEP to STL with FreeCAD...")
        import sys
        
        # Common FreeCAD paths
        freecad_paths = [
            '/Applications/FreeCAD.app/Contents/Resources/lib',  # macOS
            '/usr/lib/freecad/lib',  # Linux
            '/usr/lib/freecad-python3/lib',  # Linux alternative
            'C:\\Program Files\\FreeCAD\\bin',  # Windows
        ]
        
        # Try to add FreeCAD to path
        for path in freecad_paths:
            if os.path.exists(path) and path not in sys.path:
                sys.path.append(path)
        
        import FreeCAD
        import Import
        import Mesh
        
        st.success("✅ FreeCAD found! Converting...")
        
        # Import STEP file
        Import.insert(step_path, "TempDoc")
        doc = FreeCAD.ActiveDocument
        
        if not doc:
            doc = FreeCAD.newDocument("TempDoc")
            Import.insert(step_path, "TempDoc")
        
        # Export to STL
        objs = [obj for obj in doc.Objects]
        Mesh.export(objs, stl_path)
        
        # Clean up
        try:
            FreeCAD.closeDocument("TempDoc")
        except:
            pass
        
        if os.path.exists(stl_path) and os.path.getsize(stl_path) > 0:
            st.success("✅ STEP → STL conversion successful!")
            return True, "STEP → STL conversion successful via FreeCAD"
        
    except ImportError:
        st.warning("⚠️ FreeCAD Python module not found, trying alternatives...")
    except Exception as e:
        st.warning(f"⚠️ FreeCAD conversion failed: {str(e)}")
    
    # Try Method 2: CadQuery
    try:
        st.info("🔄 Converting STEP to STL with CadQuery...")
        import cadquery as cq
        
        result = cq.importers.importStep(step_path)
        result.val().exportStl(stl_path)
        
        if os.path.exists(stl_path) and os.path.getsize(stl_path) > 0:
            st.success("✅ STEP → STL conversion successful!")
            return True, "STEP → STL conversion successful via CadQuery"
        
    except ImportError:
        st.warning("⚠️ CadQuery not found, trying alternatives...")
    except Exception as e:
        st.warning(f"⚠️ CadQuery conversion failed: {str(e)}")
    
    # Try Method 3: FreeCAD Command Line
    try:
        st.info("🔄 Converting STEP to STL with FreeCAD CLI...")
        import subprocess
        
        # Create conversion script
        conversion_script = f"""
import FreeCAD
import Import
import Mesh
import sys

try:
    Import.insert("{step_path}", "TempDoc")
    doc = FreeCAD.ActiveDocument
    if doc:
        objs = [obj for obj in doc.Objects]
        Mesh.export(objs, "{stl_path}")
        FreeCAD.closeDocument("TempDoc")
        sys.exit(0)
    else:
        sys.exit(1)
except Exception as e:
    print(f"Error: {{e}}")
    sys.exit(1)
"""
        
        import tempfile
        script_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script_path = script_file.name
        script_file.write(conversion_script)
        script_file.close()
        
        # Try different FreeCAD commands
        freecad_commands = [
            'freecadcmd',
            'FreeCADCmd',
            '/Applications/FreeCAD.app/Contents/MacOS/FreeCAD',
            'freecad',
        ]
        
        for cmd in freecad_commands:
            try:
                result = subprocess.run(
                    [cmd, script_path],
                    capture_output=True,
                    timeout=180,  # 3 minute timeout
                    text=True
                )
                
                if result.returncode == 0 and os.path.exists(stl_path) and os.path.getsize(stl_path) > 0:
                    st.success("✅ STEP → STL conversion successful!")
                    try:
                        os.remove(script_path)
                    except:
                        pass
                    return True, "STEP → STL conversion successful via FreeCAD CLI"
            except FileNotFoundError:
                continue
            except subprocess.TimeoutExpired:
                st.warning(f"⏱️ Conversion timeout with {cmd}")
                continue
            except Exception:
                continue
        
        # Clean up
        try:
            os.remove(script_path)
        except:
            pass
            
    except Exception as e:
        st.warning(f"⚠️ FreeCAD CLI conversion failed: {str(e)}")
    
    # All methods failed
    return False, "STEP conversion requires FreeCAD or CadQuery"

def convert_obj_to_glb(obj_path, glb_path):
    """Convert OBJ to GLB format"""
    try:
        mesh_data = trimesh.load(obj_path)
        mesh_data.export(glb_path, file_type='glb')
        return True, "OBJ → GLB conversion successful"
    except Exception as e:
        return False, f"Error converting OBJ to GLB: {str(e)}"

def extract_geometric_data(mesh_obj):
    """Extract geometric data from mesh"""
    try:
        # Handle Scene objects (GLB files) - convert to single mesh
        if hasattr(mesh_obj, 'geometry') and len(mesh_obj.geometry) > 0:
            # It's a Scene object, get the actual mesh
            if hasattr(mesh_obj, 'dump'):
                # Combine all geometries into one mesh
                meshes = []
                for geom in mesh_obj.geometry.values():
                    if hasattr(geom, 'vertices'):
                        meshes.append(geom)
                if meshes:
                    mesh_obj = trimesh.util.concatenate(meshes)
            else:
                mesh_obj = list(mesh_obj.geometry.values())[0]
        
        data = {
            'vertices_count': len(mesh_obj.vertices),
            'faces_count': len(mesh_obj.faces),
            'edges_count': len(mesh_obj.edges) if hasattr(mesh_obj, 'edges') else 'N/A',
            'volume': mesh_obj.volume if mesh_obj.is_volume else 0,
            'surface_area': mesh_obj.area,
            'is_watertight': mesh_obj.is_watertight,
            'is_convex': mesh_obj.is_convex,
            'bounds': {
                'min': mesh_obj.bounds[0].tolist(),
                'max': mesh_obj.bounds[1].tolist()
            },
            'centroid': mesh_obj.centroid.tolist(),
            'bounding_box_volume': mesh_obj.bounding_box.volume,
            'euler_number': mesh_obj.euler_number,
        }
        
        # Calculate dimensions
        dimensions = mesh_obj.bounds[1] - mesh_obj.bounds[0]
        data['dimensions'] = {
            'x': dimensions[0],
            'y': dimensions[1],
            'z': dimensions[2]
        }
        
        return data
    except Exception as e:
        st.error(f"Error extracting geometric data: {str(e)}")
        return None

def analyze_operations(mesh_obj):
    """Analyze and identify required manufacturing operations with dimensions"""
    operations = []
    
    try:
        # Handle Scene objects (GLB files) - convert to single mesh
        if hasattr(mesh_obj, 'geometry') and len(mesh_obj.geometry) > 0:
            if hasattr(mesh_obj, 'dump'):
                meshes = []
                for geom in mesh_obj.geometry.values():
                    if hasattr(geom, 'vertices'):
                        meshes.append(geom)
                if meshes:
                    mesh_obj = trimesh.util.concatenate(meshes)
            else:
                mesh_obj = list(mesh_obj.geometry.values())[0]
        
        # Get overall dimensions in cm
        bounds = mesh_obj.bounds
        dimensions = bounds[1] - bounds[0]
        length = dimensions[0] / 10  # Convert to cm
        width = dimensions[1] / 10
        height = dimensions[2] / 10
        
        # Detect actual manufacturing operations with dimensions
        
        # 1. Detect holes/drilling operations
        euler = mesh_obj.euler_number
        genus = 1 - (euler / 2)
        if genus > 0:
            num_holes = int(genus)
            # Estimate hole diameter (approximate based on model size)
            estimated_hole_dia = min(length, width, height) * 0.1  # in cm
            if num_holes == 1:
                operations.append(f"Drilling - Ø{estimated_hole_dia:.1f} cm")
            else:
                operations.append(f"Drilling - {num_holes} holes, Ø{estimated_hole_dia:.1f} cm")
        
        # 2. Milling operations (if non-convex geometry)
        if not mesh_obj.is_convex and mesh_obj.is_watertight:
            # Calculate milling depth (rough estimate)
            bbox_volume = mesh_obj.bounding_box.volume
            if mesh_obj.volume > 0:
                material_removal = bbox_volume - mesh_obj.volume
                removal_percentage = (material_removal / bbox_volume) * 100
                operations.append(f"Milling - {removal_percentage:.1f}% material removal")
        
        # 3. Overall machining dimensions
        operations.append(f"Stock Size - {length:.1f} × {width:.1f} × {height:.1f} cm")
        
        # 4. Surface finishing (if high detail)
        if len(mesh_obj.faces) > 5000:
            surface_area = mesh_obj.area / 100  # Convert to cm²
            operations.append(f"Finishing - {surface_area:.1f} cm² area")
        
        # 5. Grinding/polishing (if very high detail)
        if len(mesh_obj.faces) > 20000:
            operations.append(f"Grinding - Fine surface (Ra < 0.8 μm)")
        
        # 6. Turning operations (if simple/convex)
        if mesh_obj.is_convex and genus == 0:
            # Estimate if it's cylindrical
            max_dim = max(length, width, height)
            min_dim = min(length, width)
            if abs(length - width) < max_dim * 0.3:  # roughly circular
                operations.append(f"Turning - Ø{max(length, width):.1f} cm × {height:.1f} cm")
        
        # Default if no operations identified
        if len(operations) == 0:
            operations.append(f"Casting - {length:.1f} × {width:.1f} × {height:.1f} cm")
        
    except Exception as e:
        operations.append("Analysis Required")
    
    return operations

def create_3d_viewer_html(glb_path):
    """Create HTML viewer for GLB file using Three.js"""
    import time
    cache_buster = int(time.time())  # Add timestamp to force reload
    
    with open(glb_path, 'rb') as f:
        glb_data = f.read()
        glb_base64 = base64.b64encode(glb_data).decode()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; overflow: hidden; background: #f5f5f5; }}
            #container {{ width: 100%; height: 450px; }}
        </style>
    </head>
    <body>
        <div id="container"></div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
        
        <script>
            let scene, camera, renderer, controls, model;
            
            function init() {{
                const container = document.getElementById('container');
                
                // Scene with white background like CAD software
                scene = new THREE.Scene();
                scene.background = new THREE.Color(0xffffff);  // White background
                
                // Camera setup - Isometric view
                camera = new THREE.OrthographicCamera(
                    container.clientWidth / -200,
                    container.clientWidth / 200,
                    container.clientHeight / 200,
                    container.clientHeight / -200,
                    0.1,
                    1000
                );
                
                // Set isometric angle (45 degrees from top)
                const isoDistance = 10;
                camera.position.set(isoDistance, isoDistance, isoDistance);
                camera.lookAt(0, 0, 0);
                
                // Renderer with antialiasing
                renderer = new THREE.WebGLRenderer({{ 
                    antialias: true,
                    alpha: true 
                }});
                renderer.setSize(container.clientWidth, container.clientHeight);
                renderer.setPixelRatio(window.devicePixelRatio);
                renderer.shadowMap.enabled = true;
                renderer.shadowMap.type = THREE.PCFSoftShadowMap;
                container.appendChild(renderer.domElement);
                
                // Controls - Free rotation enabled
                controls = new THREE.OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;
                controls.dampingFactor = 0.05;
                controls.rotateSpeed = 1.0;
                controls.zoomSpeed = 1.2;
                controls.panSpeed = 0.8;
                controls.minDistance = 1;
                controls.maxDistance = 50;
                controls.enableRotate = true;  // Free rotation
                controls.enableZoom = true;
                controls.enablePan = true;
                controls.minPolarAngle = 0;  // Allow full vertical rotation
                controls.maxPolarAngle = Math.PI;  // Allow full vertical rotation
                
                // Lighting setup - with internal lighting for holes
                const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);  // Brighter ambient
                scene.add(ambientLight);
                
                const keyLight = new THREE.DirectionalLight(0xffffff, 1.0);
                keyLight.position.set(5, 10, 7);
                keyLight.castShadow = true;
                scene.add(keyLight);
                
                const fillLight = new THREE.DirectionalLight(0xffffff, 0.7);
                fillLight.position.set(-5, 5, -5);
                scene.add(fillLight);
                
                const backLight = new THREE.DirectionalLight(0xffffff, 0.6);
                backLight.position.set(0, 5, -10);
                scene.add(backLight);
                
                // Add internal light to illuminate holes from inside
                const internalLight1 = new THREE.PointLight(0xffffff, 0.8, 100);
                internalLight1.position.set(0, 0, 0);
                scene.add(internalLight1);
                
                const internalLight2 = new THREE.PointLight(0xffffff, 0.6, 100);
                internalLight2.position.set(0, 5, 0);
                scene.add(internalLight2);
                
                const hemiLight = new THREE.HemisphereLight(0xffffff, 0xcccccc, 0.5);
                hemiLight.position.set(0, 20, 0);
                scene.add(hemiLight);
                
                // Load GLB model
                const loader = new THREE.GLTFLoader();
                const glbData = atob('{glb_base64}');
                const arrayBuffer = new ArrayBuffer(glbData.length);
                const view = new Uint8Array(arrayBuffer);
                for (let i = 0; i < glbData.length; i++) {{
                    view[i] = glbData.charCodeAt(i);
                }}
                
                loader.parse(arrayBuffer, '', function(gltf) {{
                    model = gltf.scene;
                    
                    // Center and scale model - LARGER size
                    const box = new THREE.Box3().setFromObject(model);
                    const center = box.getCenter(new THREE.Vector3());
                    const size = box.getSize(new THREE.Vector3());
                    const maxDim = Math.max(size.x, size.y, size.z);
                    const scale = 8 / maxDim;  // Increased from 5 to 8 for larger display
                    
                    model.scale.setScalar(scale);
                    model.position.sub(center.multiplyScalar(scale));
                    
                    // Use embedded colors from GLB but add edge highlighting for holes
                    console.log("Model loaded, enhancing visibility for holes and edges");
                    
                    model.traverse(function(child) {{
                        if (child.isMesh) {{
                            // Keep the material from GLB but enable double-sided rendering
                            if (child.material) {{
                                child.material.side = THREE.DoubleSide;  // Show both sides
                                child.material.wireframe = false;
                            }}
                            
                            // Add edge lines to highlight holes and features
                            const edges = new THREE.EdgesGeometry(child.geometry, 15);  // Angle threshold
                            const lineMaterial = new THREE.LineBasicMaterial({{ 
                                color: 0x333333,  // Dark gray edges
                                linewidth: 1 
                            }});
                            const edgeLines = new THREE.LineSegments(edges, lineMaterial);
                            child.add(edgeLines);
                        }}
                    }});
                    
                    scene.add(model);
                    
                    // Adjust camera for isometric view - CLOSER to model
                    const distance = maxDim * 1.2;  // Reduced from 2 to 1.2 for closer view
                    camera.position.set(distance, distance, distance);
                    camera.lookAt(0, 0, 0);
                    
                    // Update orthographic camera frustum - TIGHTER framing
                    const aspect = container.clientWidth / container.clientHeight;
                    const frustumSize = distance * 0.6;  // Reduced frustum for larger appearance
                    camera.left = -frustumSize * aspect;
                    camera.right = frustumSize * aspect;
                    camera.top = frustumSize;
                    camera.bottom = -frustumSize;
                    camera.updateProjectionMatrix();
                    
                    controls.update();
                    
                }}, undefined, function(error) {{
                    console.error('Error loading model:', error);
                }});
                
                // Handle window resize
                window.addEventListener('resize', onWindowResize);
                
                // Keyboard shortcuts for views
                document.addEventListener('keydown', function(event) {{
                    const isoDistance = 10;
                    
                    // Ctrl+T or T - Top view
                    if ((event.ctrlKey && event.key === 't') || event.key === 't') {{
                        camera.position.set(0, isoDistance, 0);
                        camera.lookAt(0, 0, 0);
                        controls.update();
                        event.preventDefault();
                    }}
                    
                    // Ctrl+F or F - Front view
                    if ((event.ctrlKey && event.key === 'f') || event.key === 'f') {{
                        camera.position.set(0, 0, isoDistance);
                        camera.lookAt(0, 0, 0);
                        controls.update();
                        event.preventDefault();
                    }}
                    
                    // Ctrl+R or R - Right view
                    if ((event.ctrlKey && event.key === 'r') || event.key === 'r') {{
                        camera.position.set(isoDistance, 0, 0);
                        camera.lookAt(0, 0, 0);
                        controls.update();
                        event.preventDefault();
                    }}
                    
                    // Ctrl+I or I - Isometric view
                    if ((event.ctrlKey && event.key === 'i') || event.key === 'i') {{
                        camera.position.set(isoDistance, isoDistance, isoDistance);
                        camera.lookAt(0, 0, 0);
                        controls.update();
                        event.preventDefault();
                    }}
                    
                    // Ctrl+B or B - Bottom view
                    if ((event.ctrlKey && event.key === 'b') || event.key === 'b') {{
                        camera.position.set(0, -isoDistance, 0);
                        camera.lookAt(0, 0, 0);
                        controls.update();
                        event.preventDefault();
                    }}
                    
                    // Ctrl+L or L - Left view
                    if ((event.ctrlKey && event.key === 'l') || event.key === 'l') {{
                        camera.position.set(-isoDistance, 0, 0);
                        camera.lookAt(0, 0, 0);
                        controls.update();
                        event.preventDefault();
                    }}
                }});
                
                animate();
            }}
            
            function onWindowResize() {{
                const container = document.getElementById('container');
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }}
            
            function animate() {{
                requestAnimationFrame(animate);
                controls.update();
                renderer.render(scene, camera);
            }}
            
            init();
        </script>
    </body>
    </html>
    """
    return html

# Sidebar - File Upload
with st.sidebar:
    st.header("📁 Upload 3D File")
    uploaded_file = st.file_uploader(
        "Choose a STEP or STL file",
        type=['step', 'stp', 'stl'],
        help="Upload your 3D CAD file for analysis"
    )
    
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        
        if st.button("🔄 Process File", type="primary"):
            with st.spinner("Processing your 3D model..."):
                # Create temporary directory
                with tempfile.TemporaryDirectory() as tmpdir:
                    # Save uploaded file with proper name (avoiding special characters)
                    safe_filename = uploaded_file.name.replace(' ', '_').replace('(', '').replace(')', '')
                    input_path = os.path.join(tmpdir, safe_filename)
                    
                    # Write file in binary mode
                    with open(input_path, 'wb') as f:
                        f.write(uploaded_file.getvalue())
                    
                    # Verify file was written correctly
                    if not os.path.exists(input_path):
                        st.error("❌ Error saving uploaded file. Please try again.")
                        st.stop()
                    
                    # Determine file type
                    file_ext = Path(uploaded_file.name).suffix.lower()
                    
                    # Define conversion paths
                    stl_path = os.path.join(tmpdir, "model.stl")
                    obj_path = os.path.join(tmpdir, "model.obj")
                    glb_path = os.path.join(tmpdir, "model.glb")
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Validate file
                    file_size = os.path.getsize(input_path)
                    if file_size == 0:
                        st.error("❌ Uploaded file is empty. Please try uploading again.")
                        st.stop()
                    
                    st.info(f"📊 File size: {file_size / 1024 / 1024:.2f} MB")
                    
                    # Step 1: Convert to STL (if needed) or use directly
                    if file_ext == '.stl':
                        # Already STL, just copy it
                        status_text.text("Step 1/4: File is already STL format...")
                        progress_bar.progress(25)
                        import shutil
                        shutil.copy(input_path, stl_path)
                        st.success("✅ STL file loaded!")
                        success = True
                        stl_for_download = None  # No need to save, already STL
                    else:  # STEP file
                        status_text.text("Step 1/4: Converting STEP to STL...")
                        progress_bar.progress(25)
                        st.info("🔄 Converting STEP → STL (this may take a moment for large files)...")
                        success, message = convert_step_to_stl(input_path, stl_path)
                        
                        # Save STL file for user download if conversion successful
                        if success and os.path.exists(stl_path):
                            stl_output_path = os.path.join('/mnt/user-data/outputs', safe_filename.replace('.step', '.stl').replace('.stp', '.stl').replace('.STEP', '.stl').replace('.STP', '.stl'))
                            import shutil
                            shutil.copy(stl_path, stl_output_path)
                            stl_for_download = stl_output_path
                            st.success(f"✅ STL file created and saved for download!")
                        else:
                            stl_for_download = None
                    
                    if not success:
                        st.error("❌ STEP to STL conversion failed")
                        st.error("Please use one of these alternatives:")
                        st.markdown("""
                        ### ✅ Quick Solutions:
                        
                        **Option 1: Online Converter (Fastest - 2 minutes)**
                        1. Go to: https://anyconv.com/step-to-stl-converter/
                        2. Upload your STEP file
                        3. Download the STL file
                        4. Upload the STL here ✅
                        
                        **Option 2: Install FreeCAD**
                        ```bash
                        brew install --cask freecad
                        export PYTHONPATH=/Applications/FreeCAD.app/Contents/Resources/lib:$PYTHONPATH
                        ```
                        Then restart this app and try again!
                        
                        **Option 3: Use FreeCAD Desktop**
                        1. Open FreeCAD
                        2. File → Open → Your STEP file
                        3. File → Export → Save as STL
                        4. Upload STL here ✅
                        """)
                        st.stop()
                    
                    # Step 2: Convert STL to OBJ
                    status_text.text("Step 2/4: Converting STL to OBJ...")
                    progress_bar.progress(50)
                    
                    success, message = convert_stl_to_obj(stl_path, obj_path)
                    if not success:
                        st.error(message)
                        st.stop()
                    
                    st.success(message)
                    
                    # Step 3: Convert OBJ to GLB
                    status_text.text("Step 3/4: Converting OBJ to GLB...")
                    progress_bar.progress(75)
                    
                    # Load mesh and set visual properties BEFORE converting to GLB
                    try:
                        mesh_for_glb = trimesh.load(obj_path)
                        # Set light blue color in the mesh itself
                        if hasattr(mesh_for_glb, 'visual'):
                            # Set vertex colors to light blue
                            light_blue = [173, 216, 230, 255]  # Light blue RGBA
                            vertex_colors = np.tile(light_blue, (len(mesh_for_glb.vertices), 1))
                            mesh_for_glb.visual.vertex_colors = vertex_colors
                        # Export with colors
                        mesh_for_glb.export(glb_path, file_type='glb')
                        success = True
                        message = "OBJ → GLB conversion successful"
                    except Exception as e:
                        success = False
                        message = f"Error converting OBJ to GLB: {str(e)}"
                    
                    if not success:
                        st.error(message)
                        st.stop()
                    
                    st.success(message)
                    
                    # Step 4: Extract data
                    status_text.text("Step 4/4: Extracting geometric data...")
                    progress_bar.progress(100)
                    
                    # Load mesh for analysis from OBJ (more reliable than GLB)
                    mesh_obj = trimesh.load(obj_path)
                    
                    # Extract geometric data
                    geo_data = extract_geometric_data(mesh_obj)
                    operations = analyze_operations(mesh_obj)
                    
                    # Read GLB file for viewer
                    with open(glb_path, 'rb') as f:
                        glb_content = f.read()
                    
                    # Store in session state
                    st.session_state.model_data = glb_content
                    st.session_state.geometric_data = geo_data
                    st.session_state.operations = operations
                    st.session_state.glb_path = glb_path
                    st.session_state.stl_download_path = stl_for_download  # Save STL path for download
                    
                    status_text.text("✅ Processing complete!")
                    progress_bar.progress(100)

# Main content
if st.session_state.model_data is None:
    st.info("👈 Upload a STEP or STL file from the sidebar to begin analysis")
    
    # Show example features
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🔄 File Conversion")
        st.write("Automatic conversion pipeline:")
        st.write("- STEP/STL → OBJ")
        st.write("- OBJ → GLB")
        st.write("- Interactive 3D visualization")
    
    with col2:
        st.markdown("### 📊 Geometric Analysis")
        st.write("Extract key data:")
        st.write("- Vertices & faces count")
        st.write("- Volume & surface area")
        st.write("- Dimensions & bounds")
        st.write("- Centroid position")
    
    with col3:
        st.markdown("### 🔍 Feature Detection")
        st.write("Automatic detection of:")
        st.write("- Solid vs surface models")
        st.write("- Topology analysis")
        st.write("- Holes & features")
        st.write("- Space utilization")

else:
    # Hide sidebar after processing to maximize space
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Add a button to show sidebar again if needed
    if st.button("📁 Upload New File"):
        st.session_state.model_data = None
        st.rerun()
    
    # Compact single-screen layout
    
    # Top row: 3D Viewer (left) + Key Metrics (right)
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("🎨 3D Model")
        
        # Create temporary file for viewer
        with tempfile.NamedTemporaryFile(delete=False, suffix='.glb') as tmp:
            tmp.write(st.session_state.model_data)
            tmp_path = tmp.name
        
        # Display 3D viewer - optimized height to fit with all data
        html_viewer = create_3d_viewer_html(tmp_path)
        st.components.v1.html(html_viewer, height=450, scrolling=False)
        
        # Clean up temp file
        try:
            os.unlink(tmp_path)
        except:
            pass
    
    with col_right:
        st.subheader("📊 GEOMETRIC METRICS")
        
        geo_data = st.session_state.geometric_data
        
        if geo_data:
            # Compact 2-column layout for metrics
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Vertices", f"{geo_data['vertices_count']:,}")
                st.metric("Volume", f"{geo_data['volume']/1000:.2f} cm³")
            with col_m2:
                st.metric("Faces", f"{geo_data['faces_count']:,}")
                st.metric("Area", f"{geo_data['surface_area']/100:.2f} cm²")
            
            st.markdown("**Properties:**")
            
            # Material selection
            materials = {
                "Steel": {"density": 7.85, "cost_per_kg": 210},  # g/cm³, ₹/kg
                "Aluminum": {"density": 2.70, "cost_per_kg": 335},
                "Stainless Steel": {"density": 8.00, "cost_per_kg": 420},
                "Titanium": {"density": 4.50, "cost_per_kg": 2900},
                "Brass": {"density": 8.50, "cost_per_kg": 585},
                "Copper": {"density": 8.96, "cost_per_kg": 750},
                "Plastic (ABS)": {"density": 1.05, "cost_per_kg": 290},
                "Nylon": {"density": 1.15, "cost_per_kg": 375},
            }
            
            selected_material = st.selectbox("Material:", list(materials.keys()), key="material_select")
            material_data = materials[selected_material]
            
            # Calculate weight (volume in cm³ × density in g/cm³ ÷ 1000 = kg)
            volume_cm3 = geo_data['volume'] / 1000  # Convert from mm³ to cm³
            weight_kg = (volume_cm3 * material_data['density']) / 1000
            
            # Calculate material cost
            material_cost = weight_kg * material_data['cost_per_kg']
            
            # Calculate manufacturing cost (rough estimate)
            # Based on complexity, volume, and operations
            complexity_factor = 1.0
            if len(st.session_state.operations) > 3:
                complexity_factor = 1.5
            if len(st.session_state.operations) > 5:
                complexity_factor = 2.0
            
            # Base manufacturing cost factors (in ₹)
            setup_cost = 4200  # Base setup cost in ₹
            machining_cost_per_cm3 = 42  # ₹ per cm³ removed
            finishing_cost = 1650 if geo_data['faces_count'] > 5000 else 840
            
            manufacturing_cost = (setup_cost + (volume_cm3 * machining_cost_per_cm3 * complexity_factor) + finishing_cost)
            
            total_cost = material_cost + manufacturing_cost
            
            # Determine if single part or assembly
            part_type = "Single Part"
            if hasattr(st.session_state, 'mesh_components'):
                if st.session_state.mesh_components > 1:
                    part_type = f"Assembly ({st.session_state.mesh_components} parts)"
            
            st.write(f"✓ Type: {part_type} | Quality: {'Solid' if geo_data['is_watertight'] else 'Surface'}")
            st.write(f"💪 Weight: **{weight_kg:.3f} kg** ({weight_kg*1000:.1f} g)")
            st.write(f"💰 Material Cost: **₹{material_cost:.2f}**")
            st.write(f"🏭 Manufacturing Cost: **₹{manufacturing_cost:.2f}**")
            st.write(f"💵 **Total Cost: ₹{total_cost:.2f}**")
    
    # Bottom row: Geometric Details (left) + Operations (center) + Downloads (right)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📦 BOUNDING BOX")
        if geo_data:
            bbox_x = (geo_data['bounds']['max'][0] - geo_data['bounds']['min'][0]) / 10
            bbox_y = (geo_data['bounds']['max'][1] - geo_data['bounds']['min'][1]) / 10
            bbox_z = (geo_data['bounds']['max'][2] - geo_data['bounds']['min'][2]) / 10
            
            st.write(f"**Length:** {bbox_x:.2f} cm")
            st.write(f"**Width:** {bbox_y:.2f} cm")
            st.write(f"**Height:** {bbox_z:.2f} cm")
            st.write(f"**Volume:** {geo_data['bounding_box_volume']/1000:.2f} cm³")
    
    with col2:
        st.subheader("⚙️ Operations")
        operations = st.session_state.operations
        
        if operations:
            for op in operations:
                st.write(f"• {op}")
        else:
            st.write("No operations needed")
    
    with col3:
        st.subheader("📥 Downloads")
        
        st.download_button(
            label="GLB File",
            data=st.session_state.model_data,
            file_name="model.glb",
            mime="model/gltf-binary",
            use_container_width=True
        )
        
        # STL download if available
        if 'stl_download_path' in st.session_state and st.session_state.stl_download_path:
            with open(st.session_state.stl_download_path, 'rb') as f:
                stl_data = f.read()
            st.download_button(
                label="STL File",
                data=stl_data,
                file_name=os.path.basename(st.session_state.stl_download_path),
                mime="application/sla",
                use_container_width=True
            )
        
        # JSON download
        if geo_data:
            geo_json = json.dumps(geo_data, indent=2)
            st.download_button(
                label="JSON Data",
                data=geo_json,
                file_name="data.json",
                mime="application/json",
                use_container_width=True
            )

# Footer
st.markdown("---")
st.markdown("*3D CAD Viewer powered by Trimesh and Three.js*")
