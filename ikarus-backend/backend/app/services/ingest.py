import ast, pandas as pd, numpy as np
from typing import List, Dict
from .embed import TextEmbedder
from .vector_store import FaissStore

def parse_list(s):
    if pd.isna(s): return []
    s = str(s).strip()
    try:
        v = ast.literal_eval(s)
        return [x.strip() for x in v] if isinstance(v, (list, tuple)) else [s]
    except Exception:
        return [x.strip() for x in s.split(",") if x.strip()]

def load_products(csv_path: str) -> List[Dict]:
    df = pd.read_csv(csv_path)
    df["categories"] = df["categories"].apply(parse_list)
    df["images"] = df["images"].apply(parse_list)
    def parse_price(x):
        if pd.isna(x): return None
        if isinstance(x, str):
            x = x.replace("$","").replace(",","").strip()
        try: return float(x)
        except: return None
    df["price"] = df["price"].apply(parse_price)
    return df.to_dict(orient="records")

def build_indices(csv_path: str, idx_path: str):
    products = load_products(csv_path)
    emb = TextEmbedder()
    vecs, _ = emb.encode_products(products)
    store = FaissStore(dim=vecs.shape[1], path=idx_path)
    store.add(np.array(vecs), products)
    store.save()
