from app.rag.interface.doc_process import AbstractDocumentLoader
from langchain_community.document_loaders import PyMuPDFLoader


class PDFLoader(AbstractDocumentLoader):
    def __init__(self):
        pass

    @property
    def supported_extensions(self) -> set[str]:
        return {".pdf"}

    async def load(self, file_path):
        pdf_loader = PyMuPDFLoader(str(file_path))
        return await pdf_loader.aload()
