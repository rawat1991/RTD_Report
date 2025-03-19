
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
import pandas as pd
from datetime import datetime

def calculate_total_cans(row):
    """Calculate total cans including all rejections and samples"""
    base_cans = row['TotalCase'] + row['LooseCans']
    rejection_fields = [
        'EmptyRejection', 'FilledRejection', 'BreakdownRejection',
        'ManpowerDentRejection', 'HighPressureRejection', 'WaterCanRejection',
        'MachineDentCans', 'FadeCans', 'UnprintedCans', 'ScratchedCans',
        'LidRejection', 'QASample', 'QAOtherSample'
    ]
    rejection_total = sum(row[field] for field in rejection_fields)
    return base_cans + rejection_total

def create_pdf_report(df, start_date, end_date):
    """Generate a PDF report from the dataframe"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=20,
        alignment=1  # Center alignment
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=10,
        spaceAfter=10,
        textColor=colors.HexColor('#1a472a')
    )

    # Title
    elements.append(Paragraph("Production Report", title_style))
    elements.append(Paragraph(f"Period: {start_date} to {end_date}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # Process each record
    for idx, row in df.iterrows():
        total_cans = calculate_total_cans(row)

        # Record header with better styling
        elements.append(Paragraph(
            f"Report: {row['Date']} - {row['VariantName']} ({row['BatchCode']})",
            header_style
        ))

        # Basic Information
        elements.append(Paragraph("Basic Information", styles["Heading3"]))
        basic_info = [
            ["Date", str(row["Date"])],
            ["Variant Name", row["VariantName"]],
            ["Batch Code", row["BatchCode"]],
            ["Total Cans", str(total_cans)],
            ["Total Case", str(row["TotalCase"])],
            ["Loose Cans", str(row["LooseCans"])],
            ["WIP Cans", str(row["WIPCans"])]
        ]
        
        basic_table = Table(basic_info, colWidths=[2.5*inch, 5*inch])
        basic_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(basic_table)
        elements.append(Spacer(1, 15))

        # Rejection Information with better layout
        elements.append(Paragraph("Rejection Details", styles["Heading3"]))
        rejection_info = [
            ["Empty Rejection", str(row["EmptyRejection"])],
            ["Filled Rejection", str(row["FilledRejection"])],
            ["Breakdown Rejection", str(row["BreakdownRejection"])],
            ["Manpower Dent Rejection", str(row["ManpowerDentRejection"])],
            ["High Pressure Rejection", str(row["HighPressureRejection"])],
            ["Water Can Rejection", str(row["WaterCanRejection"])],
            ["Machine Dent Cans", str(row["MachineDentCans"])],
            ["Fade Cans", str(row["FadeCans"])],
            ["Unprinted Cans", str(row["UnprintedCans"])],
            ["Scratched Cans", str(row["ScratchedCans"])],
            ["Lid Rejection", str(row["LidRejection"])],
            ["Reject Shipper", str(row["RejectShipper"])]
        ]
        
        rejection_table = Table(rejection_info, colWidths=[3*inch, 4.5*inch])
        rejection_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(rejection_table)
        elements.append(Spacer(1, 15))

        # QA Information
        elements.append(Paragraph("Quality Assurance", styles["Heading3"]))
        qa_info = [
            ["QA Sample", str(row["QASample"])],
            ["QA Other Sample", str(row["QAOtherSample"])],
            ["Empty Sample", str(row["EmptySample"])]
        ]
        
        qa_table = Table(qa_info, colWidths=[2.5*inch, 5*inch])
        qa_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(qa_table)
        
        # Add page break after each report except the last one
        if idx < len(df) - 1:
            elements.append(PageBreak())

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
