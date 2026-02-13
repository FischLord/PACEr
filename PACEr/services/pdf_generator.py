import io
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class PacerPdfGenerator:
    """Generates A4 PDF with calculation results."""

    EMPTY_COL_WIDTH = 15 * mm

    def __init__(self, calculation):
        self.calc = calculation
        self.result_data = json.loads(calculation.result_json) if calculation.result_json else {}

    def generate(self):
        """Returns a BytesIO buffer containing the PDF."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A4,
            leftMargin=10 * mm, rightMargin=10 * mm,
            topMargin=10 * mm, bottomMargin=10 * mm,
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'PacerTitle', parent=styles['Title'],
            fontSize=20, textColor=colors.HexColor('#ea580c'),
            spaceAfter=4 * mm,
        )
        meta_style = ParagraphStyle(
            'PacerMeta', parent=styles['Normal'],
            fontSize=10, textColor=colors.HexColor('#9ca3af'),
            spaceAfter=2 * mm,
        )

        elements = []

        # Title
        elements.append(Paragraph('PACEr - Ergebnisse', title_style))

        # Meta info
        meta_parts = [f'Streckenlänge: {self.calc.laenge} m']
        if self.calc.art:
            meta_parts.append(f'Art: {self.calc.art.capitalize()}')
        if self.calc.kmh:
            meta_parts.append(f'Tempo: {self.calc.kmh} km/h')
        if self.calc.klasse:
            meta_parts.append(f'Klasse: {self.calc.klasse}')
        if self.calc.tournament:
            meta_parts.append(f'Turnier: {self.calc.tournament.name}')

        elements.append(Paragraph(' | '.join(meta_parts), meta_style))
        elements.append(Spacer(1, 6 * mm))

        # Build table
        has_bz = 'bz' in self.result_data

        # Header: Strecke, [leer], BZ?, [leer], EZ, [leer], HZ, [leer]
        header = ['Strecke (m)']
        if has_bz:
            header.extend(['', 'Bestzeit'])
        header.extend(['', 'Erlaubte Zeit', '', 'Höchstzeit', ''])

        table_data = [header]

        ez_data = self.result_data.get('ez', {})
        hz_data = self.result_data.get('hz', {})
        bz_data = self.result_data.get('bz', {})

        for key in ez_data:
            row = [str(key)]
            if has_bz:
                if key in bz_data:
                    bz = bz_data[key]
                    row.extend(['', f"{bz['min']}:{bz['sec']:02d}"])
                else:
                    row.extend(['', '-'])
            ez = ez_data[key]
            hz = hz_data.get(key, {})
            row.extend(['', f"{ez['min']}:{ez['sec']:02d}"])
            row.extend(['', f"{hz.get('min', 0)}:{hz.get('sec', 0):02d}", ''])
            table_data.append(row)

        # Calculate column widths
        # With BZ: Strecke(0) ''(1) BZ(2) ''(3) EZ(4) ''(5) HZ(6) ''(7) — 8 cols
        # Without:  Strecke(0) ''(1) EZ(2) ''(3) HZ(4) ''(5) — 6 cols
        page_width = A4[0] - 20 * mm  # total usable width (10mm margins each side)

        if has_bz:
            empty_count = 4  # indices 1, 3, 5, 7
            data_count = 4   # indices 0, 2, 4, 6
        else:
            empty_count = 3  # indices 1, 3, 5
            data_count = 3   # indices 0, 2, 4

        empty_total = empty_count * self.EMPTY_COL_WIDTH
        data_col_width = (page_width - empty_total) / data_count

        col_widths = []
        for i, h in enumerate(header):
            if h == '':
                col_widths.append(self.EMPTY_COL_WIDTH)
            else:
                col_widths.append(data_col_width)

        table = Table(table_data, colWidths=col_widths)

        # Colors
        bz_color = colors.HexColor('#22c55e')  # green
        ez_color = colors.HexColor('#f97316')  # orange
        hz_color = colors.HexColor('#ef4444')  # red
        header_bg = colors.HexColor('#374151')
        row_bg = colors.HexColor('#1f2937')
        alt_row_bg = colors.HexColor('#111827')

        style_commands = [
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), header_bg),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            # Data rows
            ('FONTSIZE', (0, 1), (-1, -1), 13),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (0, -1), 14),
            # Alignment
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # Increased padding for readability
            ('TOPPADDING', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            # Grid on data columns only
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#374151')),
        ]

        # Make empty columns have no background color distinction and no grid lines
        for i, h in enumerate(header):
            if h == '':
                # White-out the grid for empty columns by setting same bg
                for row_idx in range(len(table_data)):
                    style_commands.append(('BACKGROUND', (i, row_idx), (i, row_idx), colors.white))
                    style_commands.append(('TEXTCOLOR', (i, row_idx), (i, row_idx), colors.white))
                # Remove grid lines around empty columns
                style_commands.append(('LINEBELOW', (i, 0), (i, -1), 0, colors.white))
                style_commands.append(('LINEABOVE', (i, 0), (i, -1), 0, colors.white))
                style_commands.append(('LINEBEFORE', (i, 0), (i, -1), 0, colors.white))
                style_commands.append(('LINEAFTER', (i, 0), (i, -1), 0, colors.white))

        # Alternate row backgrounds (only on data columns)
        for i in range(1, len(table_data)):
            bg = row_bg if i % 2 == 1 else alt_row_bg
            for col_idx, h in enumerate(header):
                if h != '':
                    style_commands.append(('BACKGROUND', (col_idx, i), (col_idx, i), bg))

        # Color data cells by type
        if has_bz:
            # BZ at col 2, EZ at col 4, HZ at col 6
            bz_col, ez_col, hz_col = 2, 4, 6
        else:
            # EZ at col 2, HZ at col 4
            ez_col, hz_col = 2, 4
            bz_col = None

        for i in range(1, len(table_data)):
            if bz_col is not None:
                style_commands.append(('TEXTCOLOR', (bz_col, i), (bz_col, i), bz_color))
            style_commands.append(('TEXTCOLOR', (ez_col, i), (ez_col, i), ez_color))
            style_commands.append(('TEXTCOLOR', (hz_col, i), (hz_col, i), hz_color))

        # Distance column text color
        for i in range(1, len(table_data)):
            style_commands.append(('TEXTCOLOR', (0, i), (0, i), colors.HexColor('#d1d5db')))

        table.setStyle(TableStyle(style_commands))
        elements.append(table)

        # Footer
        elements.append(Spacer(1, 8 * mm))
        footer_style = ParagraphStyle(
            'Footer', parent=styles['Normal'],
            fontSize=8, textColor=colors.HexColor('#6b7280'),
        )
        timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
        elements.append(Paragraph(f'Erstellt mit PACEr am {timestamp}', footer_style))

        doc.build(elements)
        buffer.seek(0)
        return buffer
