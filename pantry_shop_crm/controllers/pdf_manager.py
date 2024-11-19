import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

class PDFManager:

    def __init__(self):
        self.shop_name = "Uv Pantry Shop"

    def generate_receipt(self, order_data, order_id):
        # Get the current timestamp to append to the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Define the folder path where you want to save the PDF
        data_folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "Data")
        
        # Ensure the "Data" folder exists
        os.makedirs(data_folder_path, exist_ok=True)
        
        # Create the PDF file with Order ID and timestamp in the filename
        file_name = os.path.join(data_folder_path, f"Order_{order_id}_{timestamp}_receipt.pdf")
        
        # Create the PDF document
        pdf = SimpleDocTemplate(file_name, pagesize=letter)

        # Content for the PDF
        elements = []

        # Adding the Shop Name as a Paragraph, center-aligned
        styles = getSampleStyleSheet()
        shop_name_style = styles['Heading1']
        shop_name_style.alignment = 1  # Align text to center (1 = center)
        shop_name_paragraph = Paragraph(self.shop_name, shop_name_style)
        elements.append(shop_name_paragraph)

        # Adding the Printed Date and Time, center-aligned, below Shop Name
        printed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        printed_date_paragraph = Paragraph(f"Printed on: {printed_date}", styles['Normal'])
        printed_date_paragraph.alignment = 1  # Align text to center (1 = center)
        elements.append(printed_date_paragraph)

        # Adding a small spacer between the printed timestamp and the order info table
        elements.append(Spacer(1, 12))  # Adds vertical space of 12 units

        # Extracting Order Status (assuming it's in the first item of order_data)
        order_status = order_data[0][2]  # Assuming the 3rd element in each item is the order status

        # Adding Order ID, Pickup Date, and Order Status as a table row, center-aligned
        order_info = [
            ["Order ID", "Pickup Date", "Order Status"],  # Table headers
            [str(order_id), printed_date, order_status]  # Values for the order
        ]

        # Create a table for the order info and apply styling
        order_table = Table(order_info, colWidths=[100, 150, 100])  # Adjust column widths as needed
        order_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align everything in this table
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ]))
        elements.append(order_table)

        # Adding a small spacer between the order info table and the material details table
        elements.append(Spacer(1, 12))  # Adds vertical space of 12 units

        # Adding the main table with material details
        order_details_data = [
            ["Material Name", "Quantity"]  # Table headers
        ]

        # Append the order details (excluding order status)
        for item in order_data:
            material_name = item[3]  # Material Name
            quantity = item[4]  # Quantity
            order_details_data.append([material_name, quantity])

        # Create the main order details table and apply styling
        details_table = Table(order_details_data, colWidths=[200, 80])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells in this table
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ]))
        elements.append(details_table)

        # Build the PDF
        pdf.build(elements)

        return file_name  # Return the generated PDF filename


