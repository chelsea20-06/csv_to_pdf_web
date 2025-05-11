from flask import Flask, render_template, request, send_file, redirect, url_for
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from io import BytesIO

app = Flask(__name__)

# Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('home.html')

# Route vers le générateur de PDF (actuellement dashboard)
@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

# Route pour générer le PDF
@app.route('/generate', methods=['POST'])
def generate_pdf():
    if 'csv_file' not in request.files:
        return 'Aucun fichier CSV envoyé.'

    csv_file = request.files['csv_file']
    pdf_filename = request.form.get('pdf_filename', 'document.pdf')

    if not pdf_filename.endswith('.pdf'):
        pdf_filename += '.pdf'

    df = pd.read_csv(csv_file)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x = 50
    y = height - 50

    for col in df.columns:
        p.drawString(x, y, col)
        x += 100
    y -= 20
    x = 50

    for index, row in df.iterrows():
        for item in row:
            p.drawString(x, y, str(item))
            x += 100
        y -= 20
        x = 50
        if y < 50:
            p.showPage()
            y = height - 50

    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=pdf_filename, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)

