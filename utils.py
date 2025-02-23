from fpdf import FPDF
import yagmail
import os
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_booking_pdf(booking_data):
    try:
        # Use the current working directory for the receipts folder
        receipts_dir = os.path.join(os.getcwd(), 'booking_receipts')
        os.makedirs(receipts_dir, exist_ok=True)
        logger.info(f"Using receipts directory: {receipts_dir}")

        pdf = FPDF()
        pdf.add_page()

        # Set title font
        pdf.set_font("Arial", "B", 20)
        pdf.cell(190, 10, " MovieFlix Booking Confirmation ", 0, 1, "C")
        pdf.ln(5)

        # Add horizontal line
        pdf.set_line_width(0.5)
        pdf.line(10, 25, 200, 25)
        pdf.ln(5)

        # Booking Details Section
        pdf.set_font("Arial", "B", 14)
        pdf.cell(190, 10, "Booking Details", 0, 1, "L")
        pdf.set_font("Arial", "", 12)
        pdf.cell(190, 8, f" Booking ID: {booking_data['_id']}", 0, 1)
        pdf.cell(190, 8, f" Movie: {booking_data['title']}", 0, 1)
        pdf.cell(190, 8, f" Showtime: {booking_data['showtime']}", 0, 1)
        pdf.cell(190, 8, f" Seat No.: {', '.join(booking_data['seats'])}", 0, 1)
        pdf.cell(190, 8, f" Payment Status: Confirmed", 0, 1)
        pdf.ln(5)

        # Customer Details Section
        pdf.set_font("Arial", "B", 14)
        pdf.cell(190, 10, "Customer Details", 0, 1, "L")
        pdf.set_font("Arial", "", 12)
        pdf.cell(190, 8, f" Name: {booking_data['name']}", 0, 1)
        pdf.cell(190, 8, f" Email: {booking_data['email']}", 0, 1)
        pdf.cell(190, 8, f" Booking Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
        pdf.ln(5)

        # Pricing Table Section
        pdf.set_font("Arial", "B", 14)
        pdf.cell(190, 10, "Payment Summary", 0, 1, "L")
        pdf.set_font("Arial", "B", 12)

        pdf.cell(95, 8, "Description", 1, 0, "C")
        pdf.cell(95, 8, "Amount (Rs.)", 1, 1, "C")

        pdf.set_font("Arial", "", 12)
        pdf.cell(95, 8, f" Tickets ({len(booking_data['seats'])} seats)", 1, 0, "C")
        pdf.cell(95, 8, f"Rs. {booking_data['total_price']}", 1, 1, "C")

        pdf.cell(95, 8, " Discount Applied", 1, 0, "C")
        pdf.cell(95, 8, "Rs. 0.00", 1, 1, "C")

        pdf.set_font("Arial", "B", 12)
        pdf.cell(95, 8, " Grand Total", 1, 0, "C")
        pdf.cell(95, 8, f"Rs. {booking_data['total_price']}", 1, 1, "C")
        pdf.ln(10)

        # Booking Terms
        pdf.set_font("Arial", "B", 14)
        pdf.cell(190, 10, "Booking Terms & Conditions", 0, 1, "L")
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(190, 6, " This ticket is non-refundable once confirmed.\n"
                               " Please arrive at least 15 minutes before the showtime.\n"
                               " MovieFlix reserves the right to change schedules due to unforeseen circumstances.\n"
                               " For any queries, contact movieflix2202@gmail.com", 0, "L")

        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(190, 10, " Thank you for booking with MovieFlix! Enjoy your movie! ", 0, 1, "C")

        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(receipts_dir, f"ticket_{booking_data['_id']}_{timestamp}.pdf")

        # Save PDF
        pdf.output(filename)
        logger.info(f"Generated PDF: {filename}")

        return filename
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise

def send_booking_confirmation(email, booking_data):
    try:
        pdf_file = generate_booking_pdf(booking_data)
        logger.info(f"PDF generated successfully: {pdf_file}")

        subject = f"MovieFlix - Booking Confirmation - {booking_data['title']}"
        contents = [
            f"Dear {booking_data['name']},",
            "Thank you for booking with MovieFlix!",
            "",
            "Booking Details:",
            f"Movie: {booking_data['title']}",
            f"Showtime: {booking_data['showtime']}",
            f"Seats: {', '.join(booking_data['seats'])}",
            f"Total Amount: Rs.{booking_data['total_price']}",
            "",
            "Please find your booking confirmation attached.",
            "",
            "Best regards,",
            "MovieFlix Team"
        ]

        # Use yag from email_config.py or pass credentials directly
        yag_instance = yagmail.SMTP(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
        yag_instance.send(
            to=email,
            subject=subject,
            contents=contents,
            attachments=pdf_file
        )
        logger.info(f"Email sent successfully to {email}")
        return True
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return False