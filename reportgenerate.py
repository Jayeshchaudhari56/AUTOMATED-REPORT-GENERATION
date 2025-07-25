import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.utils import ImageReader

#Read CSV File
df = pd.read_csv("sales_data.csv")
#Analyze Sales Data
total_sales = df['Monthly Sales'].sum()
average_sales = df['Monthly Sales'].mean()
top_salesperson = df.loc[df['Monthly Sales'].idxmax()]

#Generate Bar Chart and Save
plt.figure(figsize=(8, 5))
plt.bar(df["Salesperson"], df["Monthly Sales"], color='skyblue')
plt.title("Monthly Sales Report")
plt.xlabel("Salesperson")
plt.ylabel("Monthly Sales")
plt.tight_layout()
chart_file = "monthly_sales_chart.png"
plt.savefig(chart_file)
plt.close()

#Create PDF Report with Chart + Table
def generate_sales_report(dataframe, total, average, top, filename="sales_report.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 50, " Monthly Sales Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, f"Total Sales: ₹{total:,.2f}")
    c.drawString(50, height - 110, f"Average Sales: ₹{average:,.2f}")
    c.drawString(50, height - 130, f"Top Salesperson: {top['Salesperson']} (₹{top['Monthly Sales']:,})")
    chart = ImageReader(chart_file)
    c.drawImage(chart, 50, height - 400, width=500, preserveAspectRatio=True)
    table_data = [list(dataframe.columns)] + dataframe.values.tolist()
    table = Table(table_data, colWidths=[200, 150, 180])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey])
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, 50, 100)  # Adjust Y based on chart height
    c.save()
#Generate Report
generate_sales_report(df, total_sales, average_sales, top_salesperson)
print("One-page sales report generated: sales_report.pdf")
