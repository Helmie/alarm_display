# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas


def index(request):
    return render(request, 'ui/index.html')


def idle(request):
    return render(request, 'ui/idle.html')


def weather(request):
    return render(request, 'ui/weather.html')


def statistics(request):
    return render(request, 'ui/statistics.html')


def pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
