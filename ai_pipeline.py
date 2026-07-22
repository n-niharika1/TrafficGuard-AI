try:
    import cv2
except Exception:  # pragma: no cover
    class _CV2Stub:
        FONT_HERSHEY_SIMPLEX = None
        @staticmethod
        def rectangle(img, pt1, pt2, color, thickness):
            return img
        @staticmethod
        def putText(img, text, org, font, fontScale, color, thickness):
            return img
    cv2 = _CV2Stub()
import numpy as np
try:
    import easyocr
except Exception:
    class _EasyOCRStub:
        class Reader:
            def __init__(self, *args, **kwargs):
                pass
            def readtext(self, image):
                return []
    easyocr = _EasyOCRStub
from ultralytics import YOLO

class TrafficGuardAI:
    def __init__(self):
        print("Initializing TrafficGuard AI Models...")
        # For production, you would use custom trained YOLO models for helmets and license plates.
        # Here we use the base yolov8n for general object detection (vehicles).
        try:
            self.vehicle_model = YOLO("yolov8n.pt") 
            # self.plate_model = YOLO("plate_model.pt") # Placeholder for custom plate model
            # self.helmet_model = YOLO("helmet_model.pt") # Placeholder for custom helmet model
            
            # Initialize EasyOCR (using English)
            # gpu=True if CUDA is available, else False
            self.reader = easyocr.Reader(['en'], gpu=False) 
            print("Models loaded successfully.")
        except Exception as e:
            print(f"Error loading models: {e}")

    def process_frame(self, frame):
        """
        Process a single image frame to detect vehicles, helmets, and number plates.
        Returns the annotated frame and a list of structured detections.
        """
        annotated_frame = frame.copy()
        detections_list = []

        try:
            # 1. Detect vehicles
            results = self.vehicle_model(frame, stream=False, verbose=False)
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get class ID
                    cls_id = int(box.cls[0])
                    class_name = self.vehicle_model.names[cls_id]
                    
                    # We are interested in vehicles (car, motorcycle, bus, truck)
                    if class_name in ['car', 'motorcycle', 'bus', 'truck']:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = float(box.conf[0])
                        
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
                        # In a real app, you'd use a plate detector first. 
                        # Here, we run OCR on the lower half of the vehicle as a heuristic fallback.
                        h = y2 - y1
                        lower_half_crop = frame[y1 + h//2 : y2, x1:x2]
                        
                        if lower_half_crop.size > 0:
                            # Run EasyOCR
                            ocr_results = self.reader.readtext(lower_half_crop)
                            plate_text = ""
                            for (bbox, text, prob) in ocr_results:
                                if prob > 0.5: # Confidence threshold
                                    plate_text += text + " "
                            
                            plate_text = plate_text.strip().upper()
                            if plate_text:
                                vehicle_info["plate_text"] = plate_text
                                cv2.putText(annotated_frame, f"Plate: {plate_text}", (x1, y2 + 20), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                        # --- HELMET DETECTION ---
                        # In a real app, you'd run a helmet detector model on motorcycles.
                        if class_name == 'motorcycle':
                            # Placeholder logic: randomly assign helmet status for demo if no custom model
                            # vehicle_info["helmet_missing"] = True
                            pass
                            
                        detections_list.append(vehicle_info)

        except Exception as e:
            print(f"Error during AI processing: {e}")

        return annotated_frame, detections_list

# Singleton instance
ai_system = TrafficGuardAI()
