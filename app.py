from flask import Flask, render_template, request, send_file, redirect, url_for
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'csv_file' not in request.files:
        return "Aucun fichier CSV fourni.", 400

    csv_file = request.files['csv_file']
    pdf_filename = request.form.get('pdf_filename', 'output') + '.pdf'

    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        return f"Erreur lors de la lecture du CSV : {e}", 400

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x = 50
    y = height - 50
    line_height = 15

    for col in df.columns:
        p.drawString(x, y, str(col))
        x += 100
    y -= line_height
    x = 50

    for index, row in df.iterrows():
        for item in row:
            p.drawString(x, y, str(item))
            x += 100
        y -= line_height
        x = 50
        if y < 50:
            p.showPage()
            y = height - 50

    p.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=pdf_filename,
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)

