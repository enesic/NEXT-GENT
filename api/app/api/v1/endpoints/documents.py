"""
Document management API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_tenant
from app.core.logger import get_logger
from app.models.tenant import Tenant
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentUploadResponse
from app.services.document_service import DocumentService

router = APIRouter()
logger = get_logger(__name__)


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Upload a document file.
    For now, we're mocking the actual file storage.
    """
    try:
        if not current_tenant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Giriş yapmanız gerekiyor"
            )

        # Validate file type
        if not DocumentService.validate_file_type(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Desteklenmeyen dosya türü"
            )

        # Read file content to get size
        content = await file.read()
        file_size = len(content)

        # Validate file size
        if not DocumentService.validate_file_size(file_size):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dosya boyutu çok büyük (maksimum 50MB)"
            )

        # In production, upload to S3/cloud storage here
        # file_url = await storage_service.upload_file(content, file.filename, current_tenant.id)
        
        # For now, create a mock URL
        file_url = f"mock://storage/{current_tenant.id}/{file.filename}"

        # Create document record
        document_data = DocumentCreate(
            filename=file.filename,
            file_type=file.content_type or "application/octet-stream",
            size=file_size,
            file_url=file_url
        )

        document = await DocumentService.create_document(
            db=db,
            tenant_id=current_tenant.id,
            document_data=document_data
        )

        return DocumentUploadResponse(
            id=document.id,
            filename=document.filename,
            file_type=document.file_type,
            size=document.size,
            message="Dosya başarıyla yüklendi"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("document_upload_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Dosya yüklenirken bir hata oluştu"
        )


@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    limit: int = 100,
    offset: int = 0,
    file_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    List all documents for the authenticated tenant.
    """
    try:
        if not current_tenant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Giriş yapmanız gerekiyor"
            )

        documents = await DocumentService.list_documents(
            db=db,
            tenant_id=current_tenant.id,
            limit=limit,
            offset=offset,
            file_type=file_type
        )

        return [
            DocumentResponse(
                id=doc.id,
                tenant_id=doc.tenant_id,
                filename=doc.filename,
                file_url=doc.file_url,
                file_type=doc.file_type,
                size=doc.size,
                created_at=doc.created_at,
                updated_at=doc.updated_at
            )
            for doc in documents
        ]

    except HTTPException:
        raise
    except Exception as e:
        logger.error("document_list_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Belgeler alınamadı"
        )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Get a specific document by ID.
    """
    try:
        if not current_tenant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Giriş yapmanız gerekiyor"
            )

        document = await DocumentService.get_document(
            db=db,
            document_id=document_id,
            tenant_id=current_tenant.id
        )

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Belge bulunamadı"
            )

        return DocumentResponse(
            id=document.id,
            tenant_id=document.tenant_id,
            filename=document.filename,
            file_url=document.file_url,
            file_type=document.file_type,
            size=document.size,
            created_at=document.created_at,
            updated_at=document.updated_at
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("document_get_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Belge alınamadı"
        )


@router.delete("/{document_id}")
async def delete_document(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant)
):
    """
    Delete a document.
    """
    try:
        if not current_tenant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Giriş yapmanız gerekiyor"
            )

        success = await DocumentService.delete_document(
            db=db,
            document_id=document_id,
            tenant_id=current_tenant.id
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Belge bulunamadı"
            )

        return {"message": "Belge başarıyla silindi"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error("document_delete_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Belge silinirken bir hata oluştu"
        )
