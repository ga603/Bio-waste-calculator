import io
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .forms import WasteInputForm
from .models import WasteInput

def calculator_view(request):
    result = None
    if request.method == 'POST':
        form = WasteInputForm(request.POST)
        if form.is_valid():
            result = form.save()
    else:
        form = WasteInputForm()

    return render(request, 'calculator/calculator.html', {'form': form, 'result': result})

def download_pdf_report(request, result_id):
    # Fetch the specific calculation result
    result = get_object_or_404(WasteInput, id=result_id)
    
    # Create a file-like buffer for the PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Draw PDF Content
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "Bio-Waste Fermentation Yield Report")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 720, "Project Alignment: SDG 7 (Clean Energy) & SDG 12 (Responsible Consumption)")
    
    p.line(50, 710, 550, 710) # Horizontal line separator
    
    p.drawString(50, 680, f"Waste Type: {result.get_waste_type_display()}")
    p.drawString(50, 660, f"Quantity Processed: {result.quantity_kg} kg")
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 620, f"Estimated Biogas Yield: {result.estimated_biogas_yield} m3")
    p.drawString(50, 600, f"Electrical Equivalent: {result.estimated_electricity_kwh} kWh")
    
    if result.latitude and result.longitude:
        p.setFont("Helvetica", 12)
        p.drawString(50, 560, f"Source Coordinates: {result.latitude}, {result.longitude}")
        
    p.showPage()
    p.save()
    
    # Return the buffer as a downloadable response
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Yield_Report_{result.id}.pdf")