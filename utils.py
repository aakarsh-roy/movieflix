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
        
        # Add header
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 10, 'MovieFlix Booking Confirmation', 0, 1, 'C')
        
        # Add booking details
        pdf.set_font('Arial', '', 12)
        pdf.cell(190, 10, f"Booking ID: {booking_data['_id']}", 0, 1)
        pdf.cell(190, 10, f"Movie: {booking_data['title']}", 0, 1)
        pdf.cell(190, 10, f"Name: {booking_data['name']}", 0, 1)
        pdf.cell(190, 10, f"Email: {booking_data['email']}", 0, 1)
        pdf.cell(190, 10, f"Showtime: {booking_data['showtime']}", 0, 1)
        pdf.cell(190, 10, f"Seats: {', '.join(booking_data['seats'])}", 0, 1)
        pdf.cell(190, 10, f"Total Price: ₹{booking_data['total_price']}", 0, 1)
        pdf.cell(190, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
        
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
            f"Total Amount: ₹{booking_data['total_price']}",
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