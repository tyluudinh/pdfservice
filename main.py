# main.py
import io
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from weasyprint import HTML, CSS
import uvicorn

from models import PdfData


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def generate_pdf(data: PdfData):
    # Đọc nội dung HTML từ file template.html và thực hiện thay thế các biến
    with open('templates/template.html', 'r') as template_file:
        html_template = template_file.read()

    html_string = html_template.format(
        title=data.title,
        content=data.content,
        watermark=data.watermark,
        type=data.type,
        date=data.date,
        downloaded_by=data.downloaded_by,
        logo=data.logo,
    )

    # Tạo một đối tượng HTML từ HTML string
    html = HTML(string=html_string)

    main_doc = html.render(stylesheets=[CSS('templates/styles.css')])

    # Render HTML thành PDF sử dụng weasyprint
    pdf_bytes = main_doc.write_pdf()

    return pdf_bytes

@app.get("/")
def read_root():
    return {
        "success": True,
        "version": "1.0.2",
        "message": "Welcome to PdfService",
        "link": "https://github.com/tyluudinh/pdfservice"
    } 

@app.post("/generate_pdf/")
async def create_pdf(request: Request):
    data = await request.json()
    pdf_bytes = generate_pdf(PdfData(**data))

    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=output.pdf"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")
