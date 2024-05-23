Just tried to implement the e-sign on pdf with the help of python.
This FastAPI application provides an endpoint /sign-pdf/ for signing PDF documents. Here's a brief overview of what the code does:

It imports necessary modules including FastAPI, PyPDF2, reportlab, PIL, and tempfile.
Defines a FastAPI instance app.
Defines a POST endpoint /sign-pdf/ which accepts two file uploads: the PDF document to be signed (pdf) and the signature image (signature).
Inside the endpoint function:
It reads the PDF using PyPDF2's PdfReader.
Opens and reads the signature image using PIL.
Creates a temporary canvas using reportlab to draw the signature.
Converts the signature image to bytes and saves it temporarily.
Draws the signature on the canvas at a specific position on each page of the PDF.
Merges the signature onto each page of the PDF using PyPDF2's merge_page method.
Writes the modified PDF to a temporary file.
Returns the signed PDF file as a response.
The code is structured to handle errors gracefully and returns a 500 HTTP status code with the error details if an exception occurs during the signing process. Finally, it runs the FastAPI application using uvicorn server.
