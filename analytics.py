from fastapi import APIRouter
from pathlib import Path
import pandas as pd
import re

router = APIRouter(prefix="/analytics", tags=["analytics"])

def _read_df() -> pd.DataFrame:
    base = Path(__file__).resolve().parents[2] / "data"
    for name in ["intern_data_ikarus.csv", "products.csv"]:
        p = base / name
        if p.exists():
            try:
                return pd.read_csv(p)
            except Exception:
                pass
    return pd.DataFrame()

def _coerce_price_series(df: pd.DataFrame) -> pd.Series:
    # Try common price column names
    cand_cols = [c for c in ["price","sale_price","mrp","list_price"] if c in df.columns]
    if not cand_cols or df.empty:
        return pd.Series(dtype="float64")
    s = df[cand_cols[0]].astype(str)

    # Convert ranges like "₹1,299–₹1,499" or "1299-1499" to their mean
    def _range_to_mean(x: str) -> str:
        x = x.replace("–","-").replace("—","-")
        nums = re.findall(r"[0-9]+(?:[.,][0-9]+)?", x)
        if len(nums) >= 2:
            try:
                a = float(nums[0].replace(",",""))
                b = float(nums[1].replace(",",""))
                return str((a + b) / 2.0)
            except Exception:
                return x
        return x

    s = s.map(_range_to_mean)
    # Strip currency and symbols, keep digits and dot, drop commas
    s = s.str.replace(r"[^0-9.,]", "", regex=True).str.replace(",", "", regex=False)
    return pd.to_numeric(s, errors="coerce")

@router.get("/summary")
def summary():
    df = _read_df()
    total = int(len(df))

    price = {}
    clean = _coerce_price_series(df).dropna()
    if not clean.empty:
        price = {
            "avg": float(clean.mean()),
            "median": float(clean.median()),
            "p10": float(clean.quantile(0.10)),
            "p90": float(clean.quantile(0.90)),
        }

    # categories histogram
    categories = []
    if "categories" in df.columns and len(df):
        split = df["categories"].fillna("").astype(str).str.split("[|,;/]")
        flat = pd.Series([c.strip().lower() for row in split for c in row if c.strip()])
        if not flat.empty:
            vc = flat.value_counts().head(20)
            categories = [{"name": k, "count": int(v)} for k, v in vc.items()]

    # cv_label histogram
    cv_labels = []
    if "cv_label" in df.columns and len(df):
        vc = df["cv_label"].dropna().astype(str).str.strip().str.lower().value_counts().head(20)
        cv_labels = [{"name": k, "count": int(v)} for k, v in vc.items()]

    # top brands
    top_brands = []
    for col in ["brand", "Brand", "manufacturer"]:
        if col in df.columns and len(df):
            vc = df[col].dropna().astype(str).str.strip().str.lower().value_counts().head(10)
            top_brands = [{"name": k, "count": int(v)} for k, v in vc.items()]
            break

    # images coverage
    images_with = 0
    for col in ["images", "image_url", "image"]:
        if col in df.columns:
            images_with = int(df[col].notna().sum())
            break

    return {
        "total_products": total,
        "categories": categories,
        "cv_labels": cv_labels,
        "price": price,
        "top_brands": top_brands,
        "images_with": images_with
    }