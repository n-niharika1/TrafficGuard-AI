import os
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io
import sys
import types

# Create comprehensive cv2 stub BEFORE importing anything else that uses cv2
def create_cv2_stub():
    """Create a stub for OpenCV that prevents import errors in headless environments"""
    _cv2_stub = types.SimpleNamespace()
    
    # Constants
    _cv2_stub.FONT_HERSHEY_SIMPLEX = 0
    _cv2_stub.FONT_HERSHEY_PLAIN = 1
    _cv2_stub.FONT_HERSHEY_DUPLEX = 2
    _cv2_stub.FONT_HERSHEY_COMPLEX = 3
    _cv2_stub.FONT_HERSHEY_TRIPLEX = 4
    _cv2_stub.FONT_HERSHEY_COMPLEX_SMALL = 5
    _cv2_stub.FONT_HERSHEY_SCRIPT_SIMPLEX = 6
    _cv2_stub.FONT_HERSHEY_SCRIPT_COMPLEX = 7
    _cv2_stub.FONT_ITALIC = 16
    
    _cv2_stub.LINE_4 = 4
    _cv2_stub.LINE_8 = 8
    _cv2_stub.LINE_AA = 16
    
    _cv2_stub.COLOR_BGR2RGB = 4
    _cv2_stub.COLOR_RGB2BGR = 5
    _cv2_stub.COLOR_BGR2GRAY = 6
    _cv2_stub.COLOR_GRAY2BGR = 8
    
    _cv2_stub.IMREAD_COLOR = 1
    _cv2_stub.IMREAD_GRAYSCALE = 0
    _cv2_stub.IMREAD_UNCHANGED = -1
    
    # Functions
    def rectangle(img, pt1, pt2, color, thickness=1):
        return img
    
    def putText(img, text, org, font, fontScale, color, thickness=1, lineType=None):
        return img
    
    def circle(img, center, radius, color, thickness=-1):
        return img
    
    def line(img, pt1, pt2, color, thickness=1):
        return img
    
    def cvtColor(img, code):
        """Convert image color space"""
        try:
            if img is None:
                return img
            
            if code == _cv2_stub.COLOR_BGR2RGB or code == 4:
                if len(img.shape) == 3 and img.shape[2] == 3:
                    return img[:, :, ::-1].copy()
                return img
            elif code == _cv2_stub.COLOR_RGB2BGR or code == 5:
                if len(img.shape) == 3 and img.shape[2] == 3:
                    return img[:, :, ::-1].copy()
                return img
            elif code == _cv2_stub.COLOR_BGR2GRAY or code == 6:
                if len(img.shape) == 3:
                    return np.dot(img[..., :3], [0.114, 0.587, 0.299]).astype(np.uint8)
                return img
            else:
                return img
        except Exception as e:
            print(f"Error in cvtColor: {e}")
            return img
    
    def imdecode(buf, flags):
        """Decode image from bytes using PIL"""
        try:
            if buf is None or len(buf) == 0:
                return None
            
            img_pil = Image.open(io.BytesIO(buf))
            if img_pil.mode != 'RGB':
                img_pil = img_pil.convert('RGB')
            
            img_array = np.array(img_pil)
            img_bgr = img_array[:, :, ::-1].copy()
            
            return img_bgr
        except Exception as e:
            print(f"Error in imdecode: {e}")
            return None
    
    def imencode(ext, img):
        """Encode image to bytes"""
        try:
            if img is None:
                return (False, b'')
            
            if len(img.shape) == 3 and img.shape[2] == 3:
                img_rgb = img[:, :, ::-1]
            else:
                img_rgb = img
            
            img_pil = Image.fromarray(img_rgb.astype(np.uint8))
            buf = io.BytesIO()
            img_pil.save(buf, format='PNG')
            return (True, buf.getvalue())
        except Exception as e:
            print(f"Error in imencode: {e}")
            return (False, b'')
    
    def imread(filename, flags=1):
        """Read image from file"""
        try:
            if filename is None or not os.path.exists(filename):
                return None
            
            img_pil = Image.open(filename)
            if img_pil.mode != 'RGB':
                img_pil = img_pil.convert('RGB')
            
            img_array = np.array(img_pil)
            img_bgr = img_array[:, :, ::-1].copy()
            return img_bgr
        except Exception as e:
            print(f"Error in imread: {e}")
            return None
    
    def imwrite(filename, img):
        """Write image to file"""
        try:
            if img is None or filename is None:
                return False
            
            os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
            
            if len(img.shape) == 3 and img.shape[2] == 3:
                img_rgb = img[:, :, ::-1]
            else:
                img_rgb = img
            
            img_pil = Image.fromarray(img_rgb.astype(np.uint8))
            img_pil.save(filename)
            return True
        except Exception as e:
            print(f"Error in imwrite: {e}")
            return False
    
    def imshow(winname, mat):
        pass
    
    def destroyAllWindows():
        pass
    
    def waitKey(delay=0):
        return -1
    
    _cv2_stub.rectangle = rectangle
    _cv2_stub.putText = putText
    _cv2_stub.circle = circle
    _cv2_stub.line = line
    _cv2_stub.cvtColor = cvtColor
    _cv2_stub.imdecode = imdecode
    _cv2_stub.imencode = imencode
    _cv2_stub.imread = imread
    _cv2_stub.imwrite = imwrite
    _cv2_stub.imshow = imshow
    _cv2_stub.destroyAllWindows = destroyAllWindows
    _cv2_stub.waitKey = waitKey
    
    return _cv2_stub

# Install cv2 stub BEFORE any other imports
try:
    import cv2
except (ImportError, AttributeError):
    cv2_stub = create_cv2_stub()
    sys.modules['cv2'] = cv2_stub

try:
    from streamlit_webrtc import webrtc_streamer
    import av
    WEBRTC_AVAILABLE = True
except ImportError:
    WEBRTC_AVAILABLE = False
    print("Warning: streamlit-webrtc not available")

from ai_pipeline import ai_system
import database
import utils

# Set page configuration
st.set_page_config(
    page_title="TrafficGuard AI",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
st.sidebar.title("TrafficGuard AI 🚦")
st.sidebar.markdown("---")

role = st.sidebar.radio("Login As:", ["Admin", "Traffic Officer"])

if role == "Admin":
    st.sidebar.markdown("### Admin Menu")
    menu = st.sidebar.selectbox("Select Page", ["Dashboard", "Manage Officers", "Violation Logs", "Settings"])
    
    if menu == "Dashboard":
        st.title("Admin Dashboard")
        st.markdown("Overview of traffic violations and system metrics.")
        
        try:
            # Fetch data
            df = database.fetch_all_violations()
            total_violations = len(df)
            revenue = df['fine_amount'].sum() if total_violations > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Violations", f"{total_violations}")
            col2.metric("Revenue (₹)", f"{revenue:,.2f}")
            col3.metric("Repeat Offenders", "TBD")
            col4.metric("Active Officers", "24")
            
            st.subheader("Recent Violations")
            if total_violations > 0:
                st.dataframe(df.tail(10), use_container_width=True)
            else:
                st.info("No violations recorded yet.")
        except Exception as e:
            st.error(f"Error loading dashboard: {e}")
        
    elif menu == "Manage Officers":
        st.title("Manage Traffic Officers")
        st.write("Add, update, or remove traffic officers from the system.")
        
    elif menu == "Violation Logs":
        st.title("System Violation Logs")
        st.write("Detailed view of all violations recorded by the AI and officers.")
        try:
            df = database.fetch_all_violations()
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading violation logs: {e}")
        
    elif menu == "Settings":
        st.title("System Settings")
        st.write("Configure fine amounts and thresholds for repeat offenders.")

elif role == "Traffic Officer":
    st.sidebar.markdown("### Officer Menu")
    menu = st.sidebar.selectbox("Select Action", ["Live Camera Feed", "Upload Evidence", "Issue Challan", "Search Vehicle"])
    
    if menu == "Live Camera Feed":
        st.title("Live Camera Feed - AI Detection")
        st.write("Real-time traffic monitoring for helmet detection and number plate recognition.")
        
        if WEBRTC_AVAILABLE:
            try:
                # Callback function for processing WebRTC video frames
                def video_frame_callback(frame):
                    img = frame.to_ndarray(format="bgr24")
                    # Process the frame using our AI pipeline
                    annotated_img, detections = ai_system.process_frame(img)
                    return av.VideoFrame.from_ndarray(annotated_img, format="bgr24")

                webrtc_streamer(key="traffic_guard_live", video_frame_callback=video_frame_callback)
            except Exception as e:
                st.error(f"Error with live camera feed: {e}")
        else:
            st.warning("WebRTC not available in this environment. Please use 'Upload Evidence' instead.")
        
    elif menu == "Upload Evidence":
        st.title("Upload Evidence")
        uploaded_file = st.file_uploader("Upload an image of the violation", type=["jpg", "png", "jpeg"])
        
        if uploaded_file is not None:
            try:
                # Use PIL to decode the image directly
                img_pil = Image.open(uploaded_file)
                
                # Convert to RGB if needed
                if img_pil.mode != 'RGB':
                    img_pil = img_pil.convert('RGB')
                
                # Convert PIL to numpy array (RGB format)
                img_rgb = np.array(img_pil)
                
                # Convert RGB to BGR for AI processing
                img_bgr = img_rgb[:, :, ::-1].copy()
                
                st.success("File uploaded successfully. AI processing...")
                
                with st.spinner("Running YOLOv8 and OCR..."):
                    annotated_img, detections = ai_system.process_frame(img_bgr)
                
                # Display results
                col1, col2 = st.columns([2, 1])
                with col1:
                    # Convert BGR back to RGB for Streamlit display
                    if annotated_img is not None:
                        display_img = annotated_img[:, :, ::-1]
                        st.image(display_img, caption="AI Detection Results", use_container_width=True)
                    else:
                        st.error("Failed to process image")
                
                with col2:
                    st.subheader("Detections")
                    if not detections:
                        st.info("No relevant vehicles detected.")
                    else:
                        for i, det in enumerate(detections):
                            with st.expander(f"Detection {i+1} ({det['type']})", expanded=True):
                                st.write(f"**Confidence:** {det['confidence']:.2f}")
                                st.write(f"**Plate:** {det.get('plate_text', 'Not detected')}")
                                st.write(f"**Helmet Missing:** {det.get('helmet_missing', False)}")
                                if st.button("Generate Challan", key=f"challan_btn_{i}"):
                                    try:
                                        plate = det.get('plate_text', 'UNKNOWN')
                                        fine = 1000.0
                                        # Save to DB
                                        database.insert_violation(plate, 'AI Detected Offence', fine)
                                        
                                        # Generate PDF
                                        v_data = {
                                            'vehicle_number': plate,
                                            'owner_name': 'Unknown (Fetch from DB)',
                                            'violation_type': 'AI Detected Offence',
                                            'fine_amount': fine,
                                            'status': 'PENDING'
                                        }
                                        pdf_path = utils.generate_challan_pdf(v_data)
                                        
                                        st.success(f"Challan generated and saved to database for {plate}!")
                                        
                                        # Provide download button for the PDF
                                        with open(pdf_path, "rb") as pdf_file:
                                            st.download_button(
                                                label="Download Challan PDF",
                                                data=pdf_file,
                                                file_name=os.path.basename(pdf_path),
                                                mime="application/pdf"
                                            )
                                    except Exception as e:
                                        st.error(f"Error generating challan: {e}")
                
            except Exception as e:
                st.error(f"Error processing image: {e}")
        
    elif menu == "Issue Challan":
        st.title("Issue Manual Challan")
        st.write("Generate a challan for a specific vehicle.")
        
        with st.form("manual_challan_form"):
            veh_num = st.text_input("Vehicle Number Plate")
            viol_type = st.selectbox("Violation Type", ["Speeding", "Helmet Missing", "Signal Jump", "Wrong Lane"])
            fine_amt = st.number_input("Fine Amount (₹)", min_value=100.0, step=100.0)
            
            if st.form_submit_button("Issue Challan"):
                if veh_num:
                    try:
                        database.insert_violation(veh_num, viol_type, fine_amt)
                        
                        v_data = {
                            'vehicle_number': veh_num,
                            'owner_name': 'Manual Entry',
                            'violation_type': viol_type,
                            'fine_amount': fine_amt,
                            'status': 'PENDING'
                        }
                        pdf_path = utils.generate_challan_pdf(v_data)
                        
                        st.success(f"Manual Challan issued for {veh_num}!")
                        with open(pdf_path, "rb") as pdf_file:
                            st.download_button(
                                label="Download Challan PDF",
                                data=pdf_file,
                                file_name=os.path.basename(pdf_path),
                                mime="application/pdf"
                            )
                    except Exception as e:
                        st.error(f"Error issuing challan: {e}")
                else:
                    st.error("Please enter a vehicle number.")
        
    elif menu == "Search Vehicle":
        st.title("Vehicle Database Search")
        search_query = st.text_input("Enter Vehicle Number Plate (e.g., MH01AB1234)")
        if st.button("Search"):
            try:
                result = database.get_vehicle_by_number(search_query)
                if result:
                    st.success("Vehicle Found!")
                    st.json(result)
                else:
                    st.error("Vehicle not found in database.")
            except Exception as e:
                st.error(f"Error searching database: {e}")
