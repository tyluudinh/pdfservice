from pydantic import BaseModel

class PdfData(BaseModel):
    title: str
    content: str
    watermark: str
    type: str
    date: str
    downloaded_by: str
    logo: str