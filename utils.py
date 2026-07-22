import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import datetime

def generate_challan_pdf(violation_data, output_dir="challans"):
    """
    Generates a PDF challan for a given violation.
    Returns the file path of the generated PDF.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Unique filename based on timestamp
    timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Challan_{violation_data.get('vehicle_number', 'UNKNOWN')}_{timestamp_str}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2.0, height - 50, "TRAFFIC POLICE DEPARTMENT")
    
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.red)
    c.drawCentredString(width / 2.0, height - 80, "TRAFFIC VIOLATION E-CHALLAN")
    
    # Line separator
    c.setStrokeColor(colors.black)
    c.line(50, height - 100, width - 50, height - 100)
    
    # Challan Details
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    
    y_pos = height - 140
    line_height = 25
    
    details = [
        f"Challan No: CHL-{timestamp_str}",
        f"Date & Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Vehicle Number: {violation_data.get('vehicle_number', 'N/A')}",
        f"Offender Name: {violation_data.get('owner_name', 'Unknown')}",
        f"Violation Type: {violation_data.get('violation_type', 'Traffic Offence')}",
        f"Fine Amount: ₹ {violation_data.get('fine_amount', '0.00')}",
        f"Status: {violation_data.get('status', 'PENDING')}"
    ]
    
    for detail in details:
        c.drawString(70, y_pos, detail)
        y_pos -= line_height
        
    # Footer
    c.line(50, y_pos - 20, width - 50, y_pos - 20)
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.gray)
    c.drawCentredString(width / 2.0, y_pos - 40, "This is an automatically generated AI challan.")
    c.drawCentredString(width / 2.0, y_pos - 55, "Please pay the fine within 15 days to avoid additional penalties.")
    
    c.save()
    return filepath
