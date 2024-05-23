
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import io
import tempfile

app = FastAPI()

@app.post("/sign-pdf/")
async def sign_pdf(pdf: UploadFile = File(...), signature: UploadFile = File(...)):
    try:
        # Load PDF and Signature files
        pdf_reader = PdfReader(pdf.file)
        pdf_writer = PdfWriter()

        # Read signature image
        signature_image = Image.open(signature.file)

        # Create a temporary canvas to hold the signature
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)

        # Convert signature image to bytes
        temp_signature = io.BytesIO()
        signature_image.save(temp_signature, format='PNG')
        temp_signature.seek(0)

        # Create a temporary file for the signature image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(temp_signature.read())
            temp_file.seek(0)

            # Get dimensions of the PDF page
            page_width, page_height = letter

            # Set the position for the signature on the right side
            signature_width = 80
            signature_height = 40
            x_position = page_width - signature_width - 50  # 50 units margin from the right edge
            y_position = 50  # 50 units from the bottom

            # Draw the signature on the canvas
            can.drawImage(temp_file.name, x_position, y_position, width=signature_width, height=signature_height)  # Adjust position and size
            can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)

        # Add the "watermark" (which is the signature) on the existing page
        for i in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[i]
            page.merge_page(new_pdf.pages[0])
            pdf_writer.add_page(page)

        # Save the new PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as output_temp_file:
            pdf_writer.write(output_temp_file)
            output_temp_file_path = output_temp_file.name

        return FileResponse(output_temp_file_path, media_type='application/pdf', filename='signed_document.pdf')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
