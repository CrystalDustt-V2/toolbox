import os
from pathlib import Path
from typing import List, Dict, Any

try:
    import numpy as np
except ModuleNotFoundError:
    np = None

try:
    from sentence_transformers import SentenceTransformer
except ModuleNotFoundError:
    SentenceTransformer = None

try:
    import faiss
except ModuleNotFoundError:
    faiss = None
from toolbox.core.engine import console

class DocumentIndexer:
    """Simple RAG engine for local document intelligence."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        if SentenceTransformer is None or faiss is None or np is None:
            raise RuntimeError(
                "Semantic indexing dependencies are missing. Install with: pip install 'toolbox-universal[ai]'"
            )
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        
    def add_documents(self, file_paths: List[str]):
        """Index local files (txt, pdf, md)."""
        texts = []
        for path in file_paths:
            p = Path(path)
            if not p.exists(): continue
            
            content = ""
            if p.suffix == ".txt" or p.suffix == ".md":
                with open(p, "r", encoding="utf-8") as f:
                    content = f.read()
            elif p.suffix == ".pdf":
                # Basic PDF extraction (already have pypdf)
                from pypdf import PdfReader
                reader = PdfReader(p)
                content = "\n".join([page.extract_text() for page in reader.pages])
            
            if content:
                # Chunking (simple overlap)
                chunks = self._chunk_text(content)
                for i, chunk in enumerate(chunks):
                    texts.append(chunk)
                    self.documents.append({"source": str(p), "chunk": i, "text": chunk})

        if not texts:
            return

        embeddings = self.model.encode(texts)
        dimension = embeddings.shape[1]
        
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        console.print(f"[green]✓ Indexed {len(self.documents)} document chunks.[/green]")

    def _chunk_text(self, text: str, size: int = 500, overlap: int = 50) -> List[str]:
        chunks = []
        for i in range(0, len(text), size - overlap):
            chunks.append(text[i:i + size])
        return chunks

    def search(self, query: str, top_k: int = 3) -> str:
        """Find relevant context for a query."""
        if self.index is None:
            return ""
            
        query_vector = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_vector).astype('float32'), top_k)
        
        context = []
        for idx in indices[0]:
            if idx < len(self.documents):
                context.append(self.documents[idx]["text"])
                
        return "\n---\n".join(context)
