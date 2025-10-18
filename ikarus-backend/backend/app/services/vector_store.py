import faiss, numpy as np, json
from typing import List, Dict, Tuple

class FaissStore:
    def __init__(self, dim: int, path: str):
        self.dim = dim
        self.path = path
        self.index = faiss.IndexFlatIP(dim)
        self.meta: List[Dict] = []

    def add(self, vectors: np.ndarray, metas: List[Dict]):
        if vectors.dtype != np.float32:
            vectors = vectors.astype(np.float32)
        self.index.add(vectors)
        self.meta.extend(metas)

    def search(self, query_vec: np.ndarray, k: int) -> List[Tuple[int, float]]:
        if query_vec.dtype != np.float32:
            query_vec = query_vec.astype(np.float32)
        D, I = self.index.search(query_vec, k)
        return [(int(I[0, i]), float(D[0, i])) for i in range(min(k, I.shape[1]))]

    def save(self):
        faiss.write_index(self.index, self.path + ".index")
        with open(self.path + ".meta.json","w",encoding="utf-8") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)

    def load(self):
        self.index = faiss.read_index(self.path + ".index")
        with open(self.path + ".meta.json","r",encoding="utf-8") as f:
            self.meta = json.load(f)
