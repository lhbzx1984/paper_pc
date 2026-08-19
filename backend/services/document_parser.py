import io
from typing import Union
import PyPDF2
from docx import Document


class DocumentParser:
    """文档解析器，支持多种格式"""
    
    def parse(self, content: bytes, file_ext: str) -> str:
        """解析文档内容"""
        if file_ext in [".docx", ".doc", ".wps"]:
            return self._parse_docx(content)
        elif file_ext == ".pdf":
            return self._parse_pdf(content)
        else:
            raise ValueError(f"不支持的文件格式: {file_ext}")
    
    def _parse_docx(self, content: bytes) -> str:
        """解析Word/WPS文档"""
        try:
            doc = Document(io.BytesIO(content))
            text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            return text
        except Exception as e:
            raise Exception(f"Word文档解析失败: {str(e)}")
    
    def _parse_pdf(self, content: bytes) -> str:
        """解析PDF文档"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"PDF文档解析失败: {str(e)}")
