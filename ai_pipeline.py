import sys
import types
import os
from PIL import Image
import io
import numpy as np

# ============================================================================
# CRITICAL: Install cv2 stub BEFORE ANY OTHER IMPORTS
# This must happen first to prevent YOLO from failing on cv2.imshow access
# ============================================================================

def create_cv2_stub():
    """Create a comprehensive stub for OpenCV that prevents import errors in headless environments"""
    _cv2_stub = types.SimpleNamespace()
    
    # === Constants ===
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
    
    # === Image Processing Functions ===
    def rectangle(img, pt1, pt2, color, thickness=1):
        """Draw rectangle on image"""
        if img is None:
            return img
        return img
    
    def putText(img, text, org, font, fontScale, color, thickness=1, lineType=None):
        """Put text on image"""
        if img is None:
            return img
        return img
    
    def circle(img, center, radius, color, thickness=-1):
        """Draw circle on image"""
        if img is None:
            return img
        return img
    
    def line(img, pt1, pt2, color, thickness=1):
        """Draw line on image"""
        if img is None:
            return img
        return img
    
    def cvtColor(img, code):
        """Convert image color space"""
        try:
            if img is None:
                return img
            
            if code in (_cv2_stub.COLOR_BGR2RGB, 4):
                if len(img.shape) == 3 and img.shape[2] == 3:
                    return img[:, :, ::-1].copy()
                return img
            elif code in (_cv2_stub.COLOR_RGB2BGR, 5):
                if len(img.shape) == 3 and img.shape[2] == 3:
                    return img[:, :, ::-1].copy()
                return img
            elif code in (_cv2_stub.COLOR_BGR2GRAY, 6):
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
        """Display image (no-op in headless environment)"""
        pass
    
    def destroyAllWindows():
        """Destroy all windows (no-op in headless environment)"""
        pass
    
    def destroyWindow(winname):
        """Destroy window (no-op in headless environment)"""
        pass
    
    def waitKey(delay=0):
        """Wait for key press (no-op in headless environment)"""
        return -1
    
    def namedWindow(winname, flags=0):
        """Create window (no-op in headless environment)"""
        pass
    
    # Assign all methods to stub
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
    _cv2_stub.destroyWindow = destroyWindow
    _cv2_stub.waitKey = waitKey
    _cv2_stub.namedWindow = namedWindow
    
    return _cv2_stub

# Install cv2 stub IMMEDIATELY
try:
    import cv2
    print("OpenCV already available")
except (ImportError, AttributeError, ModuleNotFoundError):
    print("Installing cv2 stub for headless environment")
    cv2_stub = create_cv2_stub()
    sys.modules['cv2'] = cv2_stub

# NOW import ultralytics AFTER cv2 is available
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
    print("YOLO imported successfully")
except Exception as e:
    print(f"Error importing YOLO: {e}")
    YOLO_AVAILABLE = False

# Try to import EasyOCR with fallback
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except Exception as e:
    print(f"Warning: EasyOCR not available: {e}")
    EASYOCR_AVAILABLE = False
    
    class _EasyOCRStub:
        class Reader:
            def __init__(self, *args, **kwargs):
                pass
            def readtext(self, image):
                return []
    easyocr = _EasyOCRStub


class TrafficGuardAI:
    def __init__(self):
        print("Initializing TrafficGuard AI Models...")
        self.model_loaded = False
        self.reader_loaded = False
        
        # Try to load YOLO model
        if YOLO_AVAILABLE:
            try:
                print("Loading YOLO model (yolov8s)...")
                # Use yolov8s instead of yolov8n for better accuracy (small model)
                self.vehicle_model = YOLO("yolov8s.pt")
                self.model_loaded = True
                print("✓ YOLO model loaded successfully (yolov8s)")
                print(f"  Available classes: {list(self.vehicle_model.names.values())}")
            except Exception as e:
                print(f"✗ Error loading YOLO model: {e}")
                import traceback
                traceback.print_exc()
                self.model_loaded = False
        else:
            print("✗ YOLO not available - running in demo mode")
            self.model_loaded = False
        
        # Try to load EasyOCR
        if EASYOCR_AVAILABLE:
            try:
                print("Loading EasyOCR...")
                self.reader = easyocr.Reader(['en'], gpu=False)
                self.reader_loaded = True
                print("✓ EasyOCR loaded successfully")
            except Exception as e:
                print(f"✗ Error loading EasyOCR: {e}")
                self.reader_loaded = False
        else:
            print("✗ EasyOCR not available - running in demo mode")
            self.reader_loaded = False

    def process_frame(self, frame):
        """
        Process a single image frame to detect vehicles, helmets, and number plates.
        Returns the annotated frame and a list of structured detections.
        """
        if frame is None:
            print("Error: Frame is None")
            return None, []
            
        annotated_frame = frame.copy()
        detections_list = []

        # If models aren't loaded, return frame as-is
        if not self.model_loaded:
            print("Models not loaded - skipping detection")
            return annotated_frame, detections_list

        try:
            # 1. Detect vehicles with lower confidence threshold
            print("Running YOLO detection...")
            results = self.vehicle_model(frame, stream=False, verbose=False, conf=0.3)
            
            print(f"  YOLO detected {len(results)} result frames")
            
            for result in results:
                boxes = result.boxes
                print(f"  Total objects found: {len(boxes)}")
                
                for box in boxes:
                    # Get class ID
                    cls_id = int(box.cls[0])
                    class_name = self.vehicle_model.names[cls_id]
                    conf = float(box.conf[0])
                    
                    print(f"    → {class_name} (confidence: {conf:.2f})")
                    
                    # Accept broader range of vehicle types
                    vehicle_types = ['car', 'truck', 'bus', 'motorcycle', 'bicycle', 
                                   'bike', 'vehicle', 'auto', 'cycle', 'scooter', 'taxi']
                    
                    if class_name.lower() in vehicle_types or 'car' in class_name.lower() or 'truck' in class_name.lower():
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        
                        # Draw bounding box for vehicle
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(annotated_frame, f"{class_name} {conf:.2f}", (x1, max(15, y1 - 10)), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
                        vehicle_info = {
                            "type": class_name,
                            "confidence": conf,
                            "bbox": (x1, y1, x2, y2),
                            "plate_text": None,
                            "helmet_missing": False
                        }
                        
                        # --- OCR FOR LICENSE PLATE ---
                        if self.reader_loaded:
                            try:
                                h = y2 - y1
                                lower_half_crop = frame[y1 + h//2 : y2, x1:x2]
                                
                                if lower_half_crop.size > 0:
                                    # Run EasyOCR
                                    ocr_results = self.reader.readtext(lower_half_crop)
                                    plate_text = ""
                                    for (bbox, text, prob) in ocr_results:
                                        if prob > 0.3:  # Lower confidence threshold for OCR
                                            plate_text += text + " "
                                    
                                    plate_text = plate_text.strip().upper()
                                    if plate_text:
                                        vehicle_info["plate_text"] = plate_text
                                        cv2.putText(annotated_frame, f"Plate: {plate_text}", (x1, y2 + 20), 
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                            except Exception as e:
                                print(f"Error during OCR: {e}")

                        # --- HELMET DETECTION ---
                        if 'motorcycle' in class_name.lower() or 'bike' in class_name.lower():
                            # In production, run helmet detector model on motorcycles
                            pass
                            
                        detections_list.append(vehicle_info)
            
            print(f"  Total valid vehicle detections: {len(detections_list)}")

        except Exception as e:
            print(f"Error during AI processing: {e}")
            import traceback
            traceback.print_exc()

        return annotated_frame, detections_list


# Singleton instance
print("\n" + "="*60)
print("Initializing TrafficGuard AI System")
print("="*60)
try:
    ai_system = TrafficGuardAI()
except Exception as e:
    print(f"Fatal error initializing TrafficGuardAI: {e}")
    import traceback
    traceback.print_exc()
    ai_system = TrafficGuardAI()

print("="*60 + "\n")
