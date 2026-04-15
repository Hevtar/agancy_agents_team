"""
Knowledge Base system using ChromaDB for long-term memory storage.
"""
import chromadb
from chromadb.config import Settings
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os
from core.config import settings


class KnowledgeBase:
    """
    Knowledge Base for storing and retrieving information using vector embeddings.
    Uses ChromaDB for efficient similarity search.
    """
    
    def __init__(self, collection_name: str = "agency_knowledge", persist_directory: Optional[str] = None):
        """Initialize Knowledge Base with ChromaDB."""
        if persist_directory is None:
            persist_directory = settings.KNOWLEDGE_BASE_PATH
        
        # Create persist directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Agency knowledge base for long-term memory"}
        )
    
    def add_document(
        self, 
        document: str, 
        metadata: Optional[Dict] = None, 
        document_id: Optional[str] = None
    ) -> str:
        """
        Add a document to the knowledge base.
        
        Args:
            document: The text content to store
            metadata: Additional metadata (project_id, agent, category, etc.)
            document_id: Optional custom ID for the document
            
        Returns:
            The ID of the added document
        """
        if document_id is None:
            document_id = f"doc_{datetime.now().timestamp()}"
        
        if metadata is None:
            metadata = {}
        
        # Add timestamp and system info
        metadata["created_at"] = datetime.now().isoformat()
        metadata["system"] = "agency_agents_team"
        
        # Add to ChromaDB
        self.collection.add(
            documents=[document],
            metadatas=[metadata],
            ids=[document_id]
        )
        
        return document_id
    
    def add_documents(self, documents: List[Dict]) -> List[str]:
        """
        Add multiple documents to the knowledge base.
        
        Args:
            documents: List of dicts with 'content', 'metadata', and optional 'id'
            
        Returns:
            List of document IDs
        """
        ids = []
        contents = []
        metadatas = []
        
        for doc in documents:
            doc_id = doc.get('id', f"doc_{datetime.now().timestamp()}_{len(ids)}")
            ids.append(doc_id)
            contents.append(doc['content'])
            
            metadata = doc.get('metadata', {})
            metadata["created_at"] = datetime.now().isoformat()
            metadata["system"] = "agency_agents_team"
            metadatas.append(metadata)
        
        self.collection.add(
            documents=contents,
            metadatas=metadatas,
            ids=ids
        )
        
        return ids
    
    def search(
        self, 
        query: str, 
        n_results: int = 5, 
        where: Optional[Dict] = None,
        include: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Search the knowledge base for relevant documents.
        
        Args:
            query: Search query
            n_results: Number of results to return
            where: Optional filter criteria
            include: What to include in results (documents, metadatas, distances)
            
        Returns:
            Search results with documents, metadata, and similarity scores
        """
        if include is None:
            include = ["documents", "metadatas", "distances"]
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where,
            include=include
        )
        
        return {
            "documents": results["documents"][0],
            "metadatas": results["metadatas"][0],
            "distances": results["distances"][0] if "distances" in results else None
        }
    
    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific document by ID.
        
        Args:
            document_id: The ID of the document to retrieve
            
        Returns:
            Document content and metadata, or None if not found
        """
        results = self.collection.get(ids=[document_id], include=["documents", "metadatas"])
        
        if results["documents"]:
            return {
                "id": document_id,
                "content": results["documents"][0],
                "metadata": results["metadatas"][0]
            }
        return None
    
    def update_document(self, document_id: str, document: str, metadata: Optional[Dict] = None) -> bool:
        """
        Update an existing document.
        
        Args:
            document_id: ID of document to update
            document: New document content
            metadata: Updated metadata
            
        Returns:
            True if updated successfully
        """
        if metadata is None:
            metadata = {}
        
        metadata["updated_at"] = datetime.now().isoformat()
        
        self.collection.update(
            ids=[document_id],
            documents=[document],
            metadatas=[metadata]
        )
        
        return True
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document from the knowledge base.
        
        Args:
            document_id: ID of document to delete
            
        Returns:
            True if deleted successfully
        """
        self.collection.delete(ids=[document_id])
        return True
    
    def list_documents(self, where: Optional[Dict] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List documents with optional filtering.
        
        Args:
            where: Optional filter criteria
            limit: Maximum number of documents to return
            
        Returns:
            List of documents with metadata
        """
        results = self.collection.get(
            where=where,
            limit=limit,
            include=["documents", "metadatas"]
        )
        
        return [
            {
                "id": doc_id,
                "content": content,
                "metadata": metadata
            }
            for doc_id, content, metadata in zip(
                results["ids"], 
                results["documents"], 
                results["metadatas"]
            )
        ]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get knowledge base statistics.
        
        Returns:
            Statistics about the knowledge base
        """
        count = self.collection.count()
        
        return {
            "total_documents": count,
            "collection_name": self.collection.name,
            "persist_path": settings.KNOWLEDGE_BASE_PATH
        }
    
    def clear(self) -> bool:
        """
        Clear all documents from the knowledge base.
        
        Returns:
            True if cleared successfully
        """
        # Delete and recreate collection
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            metadata={"description": "Agency knowledge base for long-term memory"}
        )
        return True


# Singleton instance
_knowledge_base_instance = None

def get_knowledge_base(collection_name: str = "agency_knowledge") -> KnowledgeBase:
    """Get or create the Knowledge Base instance."""
    global _knowledge_base_instance
    if _knowledge_base_instance is None:
        _knowledge_base_instance = KnowledgeBase(collection_name=collection_name)
    return _knowledge_base_instance