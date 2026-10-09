from app.rag_dd.interface.doc_process import (
    AbstractDocumentLoader,
    AbstractTextSplitter,
)
from app.rag_dd.loaders import PDFLoader
from app.rag_dd.splitters import RecursiveCharacterSplitter
from app.rag_dd.doc_loader import DocumentLoader
from app.core.config import settings
from app.rag_dd.interface.vector_store import AbstractVectorStore
from app.rag_dd.vector_stores.faiss_store import FaissStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.infrastructure.file_repository import FileStorageRepository
from app.domain.repositories.file_repository import AbstractFileStorageRepository
from app.application.file_ingestion_service import FileIngestionService
from app.domain.unit_of_work import AbstractUnitOfWork
from app.application.vector_store_service import VectorStoreService
from app.application.auth_service import AuthService


def get_loader() -> AbstractDocumentLoader:
    return PDFLoader()


def get_splitter() -> AbstractTextSplitter:
    return RecursiveCharacterSplitter(settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)


def get_doc_loader() -> DocumentLoader:
    return DocumentLoader(
        {
            ".pdf": get_loader(),
        },
        get_splitter(),
    )


def get_embedding_model():
    return GoogleGenerativeAIEmbeddings(
        model=settings.EMBED_MODEL,
        output_dimensionality=settings.EMBED_MODEL_SIZE,
        api_key=settings.GOOGLE_API_KEY,
    )


def get_vector_store() -> AbstractVectorStore:
    if (settings.VECTOR_FOLDER / "index.faiss").exists():
        return FaissStore.load(
            vector_dir=settings.VECTOR_FOLDER, embedding_client=get_embedding_model()
        )

    return FaissStore.create(
        vector_dir=settings.VECTOR_FOLDER,
        embedding_client=get_embedding_model(),
        dimensions=settings.EMBED_MODEL_SIZE,
    )


def get_file_storage_repository() -> AbstractFileStorageRepository:
    return FileStorageRepository()


def get_vector_store_service(vector_store: AbstractVectorStore) -> VectorStoreService:
    return VectorStoreService(vector_store=vector_store)


def get_file_ingestion_service(
    uow: AbstractUnitOfWork, vector_service: VectorStoreService
) -> FileIngestionService:
    return FileIngestionService(
        uow=uow,
        file_storage=get_file_storage_repository(),
        doc_loader=get_doc_loader(),
        vector_service=vector_service,
        root_dir=settings.FILE_UPLOAD_PATH,
    )


def get_auth_service(uow: AbstractUnitOfWork) -> AuthService:
    return AuthService(uow=uow)
