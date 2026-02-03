"""
Document service for handling document business logic.
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from datetime import datetime

from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentResponse
from app.core.logger import get_logger

logger = get_logger(__name__)


class DocumentService:
    """Service for document management operations"""

    @staticmethod
    async def create_document(
        db: AsyncSession,
        tenant_id: UUID,
        document_data: DocumentCreate
    ) -> Document:
        """
        Create a new document record.
        For now, we're mocking the actual file storage.
        In production, this would upload to S3/cloud storage.
        """
        try:
            # Create document record
            document = Document(
                tenant_id=tenant_id,
                filename=document_data.filename,
                file_url=document_data.file_url or f"mock://storage/{tenant_id}/{document_data.filename}",
                file_type=document_data.file_type,
                size=document_data.size
            )
            
            db.add(document)
            await db.commit()
            await db.refresh(document)
            
            logger.info(
                "document_created",
                document_id=str(document.id),
                tenant_id=str(tenant_id),
                filename=document.filename
            )
            
            return document
            
        except Exception as e:
            await db.rollback()
            logger.error("document_creation_failed", error=str(e))
            raise

    @staticmethod
    async def list_documents(
        db: AsyncSession,
        tenant_id: UUID,
        limit: int = 100,
        offset: int = 0,
        file_type: Optional[str] = None
    ) -> List[Document]:
        """
        List all documents for a tenant with optional filtering.
        """
        try:
            query = select(Document).where(Document.tenant_id == tenant_id)
            
            if file_type:
                query = query.where(Document.file_type.like(f"{file_type}%"))
            
            query = query.order_by(desc(Document.created_at)).limit(limit).offset(offset)
            
            result = await db.execute(query)
            documents = result.scalars().all()
            
            return documents
            
        except Exception as e:
            logger.error("document_listing_failed", error=str(e))
            raise

    @staticmethod
    async def get_document(
        db: AsyncSession,
        document_id: UUID,
        tenant_id: UUID
    ) -> Optional[Document]:
        """
        Get a specific document by ID, ensuring it belongs to the tenant.
        """
        try:
            result = await db.execute(
                select(Document).where(
                    and_(
                        Document.id == document_id,
                        Document.tenant_id == tenant_id
                    )
                )
            )
            document = result.scalar_one_or_none()
            
            return document
            
        except Exception as e:
            logger.error("document_retrieval_failed", error=str(e))
            raise

    @staticmethod
    async def delete_document(
        db: AsyncSession,
        document_id: UUID,
        tenant_id: UUID
    ) -> bool:
        """
        Delete a document record and its associated file.
        For now, we're mocking the file deletion.
        """
        try:
            document = await DocumentService.get_document(db, document_id, tenant_id)
            
            if not document:
                return False
            
            # In production, delete the actual file from S3/storage here
            # await storage_service.delete_file(document.file_url)
            
            await db.delete(document)
            await db.commit()
            
            logger.info(
                "document_deleted",
                document_id=str(document_id),
                tenant_id=str(tenant_id)
            )
            
            return True
            
        except Exception as e:
            await db.rollback()
            logger.error("document_deletion_failed", error=str(e))
            raise

    @staticmethod
    def validate_file_type(filename: str, allowed_types: List[str] = None) -> bool:
        """
        Validate file type based on extension.
        """
        if allowed_types is None:
            # Default allowed types
            allowed_types = [
                'pdf', 'doc', 'docx', 'xls', 'xlsx', 
                'txt', 'jpg', 'jpeg', 'png', 'gif',
                'zip', 'rar', 'csv'
            ]
        
        extension = filename.lower().split('.')[-1] if '.' in filename else ''
        return extension in allowed_types

    @staticmethod
    def validate_file_size(size: int, max_size_mb: int = 50) -> bool:
        """
        Validate file size.
        """
        max_size_bytes = max_size_mb * 1024 * 1024
        return size <= max_size_bytes
