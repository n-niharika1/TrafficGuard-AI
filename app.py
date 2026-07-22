import streamlit as st
import pandas as pd
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av

from ai_pipeline import ai_system
import database

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
        
    elif menu == "Manage Officers":
        st.title("Manage Traffic Officers")
        st.write("Add, update, or remove traffic officers from the system.")
        
    elif menu == "Violation Logs":
        st.title("System Violation Logs")
        st.write("Detailed view of all violations recorded by the AI and officers.")
        df = database.fetch_all_violations()
        st.dataframe(df, use_container_width=True)
        
    elif menu == "Settings":
        st.title("System Settings")
        st.write("Configure fine amounts and thresholds for repeat offenders.")

elif role == "Traffic Officer":
    st.sidebar.markdown("### Officer Menu")
    menu = st.sidebar.selectbox("Select Action", ["Live Camera Feed", "Upload Evidence", "Issue Challan", "Search Vehicle"])
    
    if menu == "Live Camera Feed":
        st.title("Live Camera Feed - AI Detection")
        st.write("Real-time traffic monitoring for helmet detection and number plate recognition.")
        
        # Callback function for processing WebRTC video frames
        def video_frame_callback(frame):
            img = frame.to_ndarray(format="bgr24")
            
            # Process the frame using our AI pipeline
            annotated_img, detections = ai_system.process_frame(img)
            
            return av.VideoFrame.from_ndarray(annotated_img, format="bgr24")

        webrtc_streamer(key="traffic_guard_live", video_frame_callback=video_frame_callback)
        
    elif menu == "Upload Evidence":
        st.title("Upload Evidence")
        uploaded_file = st.file_uploader("Upload an image of the violation", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            # Convert uploaded file to OpenCV format
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, 1)
            
            st.success("File uploaded successfully. AI processing...")
            
            with st.spinner("Running YOLOv8 and OCR..."):
                annotated_img, detections = ai_system.process_frame(img)
            
            # Display results
            col1, col2 = st.columns([2, 1])
            with col1:
                # Convert BGR back to RGB for Streamlit display
                st.image(cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB), caption="AI Detection Results", use_container_width=True)
            
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
                                plate = det.get('plate_text', 'UNKNOWN')
                                database.insert_violation(plate, 'AI Detected Offence', 1000.0)
                                st.success(f"Challan generated and saved to database for {plate}!")
            
    elif menu == "Issue Challan":
        st.title("Issue Manual Challan")
        st.write("Generate a challan for a specific vehicle.")
        
    elif menu == "Search Vehicle":
        st.title("Vehicle Database Search")
        search_query = st.text_input("Enter Vehicle Number Plate (e.g., MH01AB1234)")
        if st.button("Search"):
            result = database.get_vehicle_by_number(search_query)
            if result:
                st.success("Vehicle Found!")
                st.json(result)
            else:
                st.error("Vehicle not found in database.")
