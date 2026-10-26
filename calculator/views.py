import io
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from .forms import WasteInputForm
from .models import WasteInput

# Simple Translation Dictionary for MVP
TRANSLATIONS = {
    'en': {
        'title': 'SDG 7 & 12: Bio-Waste Fermentation Calculator',
        'waste_type': 'Organic Waste Type',
        'qty': 'Quantity (kg)',
        'loc_label': 'Select Waste Source Location',
        'locate_me': '📍 Locate Me',
        'calc_btn': 'Calculate Potential Yield',
        'results': 'Calculation Results',
        'input_proc': 'Input Processed',
        'est_yield': 'Estimated Biogas Yield',
        'elec_eq': 'Electrical Equivalent',
        'loc_tracked': 'Location Tracked',
        'download_pdf': '📄 Download PDF Report',
        'pdf_title': 'Bio-Waste Fermentation Yield Report',
        'pdf_sub': 'Project Alignment: SDG 7 (Clean Energy) & SDG 12',
    },
    'de': {
        'title': 'SDG 7 & 12: Bio-Abfall Fermentationsrechner',
        'waste_type': 'Art des organischen Abfalls',
        'qty': 'Menge (kg)',
        'loc_label': 'Standort der Abfallquelle auswählen',
        'locate_me': '📍 Finde mich',
        'calc_btn': 'Potenziellen Ertrag berechnen',
        'results': 'Berechnungsergebnisse',
        'input_proc': 'Verarbeitete Eingabe',
        'est_yield': 'Geschätzter Biogasertrag',
        'elec_eq': 'Elektrisches Äquivalent',
        'loc_tracked': 'Erfasster Standort',
        'download_pdf': '📄 PDF-Bericht herunterladen',
        'pdf_title': 'Bio-Abfall Fermentationsertragsbericht',
        'pdf_sub': 'Projektausrichtung: SDG 7 (Saubere Energie) & SDG 12',
    }
}

# Translate the dropdown options for the PDF/Results
WASTE_TRANSLATIONS = {
    'food_waste': {'en': 'Mixed Food Waste', 'de': 'Gemischte Lebensmittelabfälle'},
    'swine_manure': {'en': 'Swine Manure', 'de': 'Schweinemist'},
    'cattle_manure': {'en': 'Cattle Manure', 'de': 'Rindermist'},
    'wheat_straw': {'en': 'Wheat Straw', 'de': 'Weizenstroh'},
    'corn_stover': {'en': 'Corn Stover', 'de': 'Maisstroh'},
    'spent_coffee': {'en': 'Spent Ground Coffee', 'de': 'Kaffeesatz'},
}

def calculator_view(request):
    # Handle language switching
    if 'lang' in request.GET:
        request.session['lang'] = request.GET['lang']
        return redirect('calculator')
    
    lang = request.session.get('lang', 'en')
    t = TRANSLATIONS[lang]
    
    # Dynamically build the dropdown choices based on the active language
    empty_label = '- Select an option -' if lang == 'en' else '- Option auswählen -'
    translated_choices = [('', empty_label)]
    for key, translations in WASTE_TRANSLATIONS.items():
        translated_choices.append((key, translations[lang]))
    
    result = None
    if request.method == 'POST':
        form = WasteInputForm(request.POST)
        # Override the form choices with our translated list BEFORE validation
        form.fields['waste_type'].choices = translated_choices
        
        if form.is_valid():
            result = form.save()
            result.translated_waste = WASTE_TRANSLATIONS[result.waste_type][lang]
    else:
        form = WasteInputForm()
        # Override the form choices for the empty form
        form.fields['waste_type'].choices = translated_choices

    return render(request, 'calculator/calculator.html', {'form': form, 'result': result, 't': t, 'lang': lang})

def download_pdf_report(request, result_id):
    lang = request.session.get('lang', 'en')
    t = TRANSLATIONS[lang]
    result = get_object_or_404(WasteInput, id=result_id)
    translated_waste = WASTE_TRANSLATIONS[result.waste_type][lang]
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Header Styling
    p.setFillColor(colors.HexColor("#198754")) 
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, 750, t['pdf_title'])
    
    p.setFillColor(colors.darkgray)
    p.setFont("Helvetica", 12)
    p.drawString(50, 725, t['pdf_sub'])
    
    # Colored Separator Line
    p.setStrokeColor(colors.HexColor("#198754"))
    p.line(50, 710, 550, 710)
    
    # Main Data
    p.setFillColor(colors.black)
    p.drawString(50, 680, f"{t['input_proc']}: {result.quantity_kg} kg - {translated_waste}")
    
    # Bold Results
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 640, f"{t['est_yield']}: {result.estimated_biogas_yield} m3")
    p.drawString(50, 620, f"{t['elec_eq']}: {result.estimated_electricity_kwh} kWh")
    
    # Location Tracking with Human-Readable Name
    if result.location_name:
        p.setFillColor(colors.HexColor("#0dcaf0"))
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, 580, f"📍 {t['loc_tracked']}: {result.location_name}")
        # Add the raw coordinates underneath in smaller text
        p.setFont("Helvetica", 10)
        p.drawString(50, 565, f"(Lat {result.latitude}, Lng {result.longitude})")
    elif result.latitude and result.longitude:
        p.setFillColor(colors.HexColor("#0dcaf0"))
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, 580, f"📍 {t['loc_tracked']}: Lat {result.latitude}, Lng {result.longitude}")
        
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Yield_Report_{lang.upper()}_{result.id}.pdf")