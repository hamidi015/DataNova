from reportlab.pdfgen import canvas


def generate_pdf_report(
    total_revenue,
    total_profit,
    profit_margin,
    best_product,
    score
):
    pdf_file = "business_report.pdf"

    pdf = canvas.Canvas(pdf_file)

    pdf.setTitle("DataNova Business Report")

    pdf.drawString(
        100,
        800,
        "DataNova Business Report"
    )

    pdf.drawString(
        100,
        760,
        f"Total Revenue: {total_revenue}"
    )

    pdf.drawString(
        100,
        740,
        f"Total Profit: {total_profit}"
    )

    pdf.drawString(
        100,
        720,
        f"Profit Margin: {profit_margin:.2f}%"
    )

    pdf.drawString(
        100,
        700,
        f"Best Product: {best_product}"
    )

    pdf.drawString(
        100,
        680,
        f"Business Health Score: {score}/100"
    )

    pdf.save()

    return pdf_file