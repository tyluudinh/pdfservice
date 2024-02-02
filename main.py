# main.py
import io
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from weasyprint import HTML, CSS
import uvicorn

from models import PdfData

app = FastAPI()

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

@app.post("/generate_pdf/")
async def create_pdf(request: Request):
    data = await request.json()
    pdf_bytes = generate_pdf(PdfData(**data))

    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=output.pdf"})


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
