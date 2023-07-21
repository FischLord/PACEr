from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import json

def generate_pdf_from_json(json_data, output_path):
    data = json.loads(json_data)

    # PDF erstellen
    c = canvas.Canvas(output_path, pagesize=A4)

    # PDF-Inhalt erstellen
    table_header = ['Länge', 'BZ', 'EZ', 'HZ']
    table_data = [table_header]

    for key, value in data.items():
        row = [str(key) + ' m']
        if 'bz_min' in value and 'bz_sec' in value:
            row.append(f"{value['bz_min']}:{'{:02}'.format(value['bz_sec'])}")
        row.append(f"{value['ez_min']}:{'{:02}'.format(value['ez_sec'])}")
        row.append(f"{value['hz_min']}:{'{:02}'.format(value['hz_sec'])}")

        table_data.append(row)

    # Tabelle im PDF zeichnen
    x_offset = 50
    y_offset = 700
    cell_width = (A4[0] - 2 * x_offset) / len(table_header)
    cell_height = 40

    background_colors = [colors.white, colors.green, colors.orange, colors.red]

    for index, row in enumerate(table_data):
        for i, cell in enumerate(row):
            if index == 0:  # Header
                c.setFont("Helvetica-Bold", 14)
                c.setFillColor(colors.black)
            else:  # Daten
                c.setFont("Helvetica-Bold", 22)  # Größere Schriftart
                c.setFillColor(colors.black)
                c.setFillColor(background_colors[i])
                c.rect(x_offset + (i * cell_width), y_offset - cell_height, cell_width, cell_height, fill=True, stroke=True)
                c.setFillColor(colors.black if i == 0 else colors.white)

            c.drawString(x_offset + (i * cell_width) + 10, y_offset - cell_height + 10, cell)
        y_offset -= 2 * cell_height  # Lassen Sie eine Zeile frei zwischen den Reihen

    c.save()

# Beispiel JSON-Daten
json_data = '''{
    "1000": {"bz_min": 3, "bz_sec": 23, "hz_min": 9, "hz_sec": 13, "ez_min": 4, "ez_sec": 0},
    "2000": {"bz_min": 6, "bz_sec": 46, "hz_min": 18, "hz_sec": 27, "ez_min": 8, "ez_sec": 0},
    "3000": {"bz_min": 10, "bz_sec": 10, "hz_min": 27, "hz_sec": 41, "ez_min": 12, "ez_sec": 0},
    "4000": {"bz_min": 13, "bz_sec": 33, "hz_min": 36, "hz_sec": 55, "ez_min": 16, "ez_sec": 0},
    "4900": {"bz_min": 16, "bz_sec": 37, "hz_min": 45, "hz_sec": 14, "ez_min": 19, "ez_sec": 37}
}'''

# Pfadeinstellungen
output_path = "output.pdf"

# Generiere das PDF
generate_pdf_from_json(json_data, output_path)
