import { useEffect, useMemo, useState } from "react";
const API = import.meta.env.VITE_API_BASE_URL;

export default function App() {
  const [q, setQ] = useState("black storage rack under 50");
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState({});
  const [cvCat, setCvCat] = useState("All");

  const chips = useMemo(() => {
    const s = new Set();
    for (const it of items) {
      const lbl = it?.product?.cv_label;
      if (lbl && String(lbl).trim()) s.add(String(lbl));
    }
    return ["All", ...Array.from(s).sort()];
  }, [items]);

  const search = async () => {
    setLoading(true); setErr("");
    try {
      const r = await fetch(`${API}/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: q,
          k: 8,
          cv_category: cvCat && cvCat !== "All" ? cvCat : null
        })
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = await r.json();
      setItems(Array.isArray(data.items) ? data.items : []);
    } catch (e) {
      setErr(String(e?.message || e)); setItems([]);
    } finally {
      setLoading(false);
    }
  };

  const genDesc = async (idx) => {
    const it = items[idx]; if (!it?.product) return;
    setBusy(s => ({ ...s, [idx]: true }));
    try {
      const r = await fetch(`${API}/recommend/gen-desc`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: it.product.title || "",
          brand: it.product.brand || "",
          categories: it.product.categories || [],
          color: it.product.color || "",
          material: it.product.material || "",
          package_dimensions: it.product.package_dimensions || "",
          price: it.product.price ?? null
        })
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = await r.json();
      const copy = items.slice();
      copy[idx] = { ...it, product: { ...it.product, gen_description: data.gen_description } };
      setItems(copy);
    } catch (e) {
      alert(`Please wait and try again: ${String(e?.message || e)}`);
    } finally {
      setBusy(s => { const n = { ...s }; delete n[idx]; return n; });
    }
  };

  useEffect(() => { search(); }, []);

  return (
    <div style={{ padding: 16 }}>
      <h2>Ikarus Recommendations</h2>

      <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <input
          value={q}
          onChange={e => setQ(e.target.value)}
          onKeyDown={e => { if (e.key === "Enter") search(); }}
          style={{ width: 480 }}
          placeholder="Describe what you want"
        />
        <button onClick={search} disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
        {chips.map((c) => (
          <button
            key={c}
            onClick={() => { setCvCat(c); setTimeout(search, 0); }}
            style={{
              padding: "6px 10px",
              borderRadius: 16,
              border: "1px solid #ccc",
              background: c === cvCat ? "#222" : "#fff",
              color: c === cvCat ? "#fff" : "#222",
              cursor: "pointer"
            }}
          >
            {c}
          </button>
        ))}
      </div>

      {err && <div style={{ color: "crimson", marginBottom: 12 }}>Error: {err}</div>}
      {!loading && !err && items.length === 0 && <div>No items found for this query.</div>}

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12 }}>
        {items.map((it, i) => {
          const p = it.product || {};
          return (
            <div key={i} style={{ border: "1px solid #ddd", padding: 12, borderRadius: 6 }}>
              <div style={{ fontWeight: 700, marginBottom: 6 }}>{p.title}</div>
              <div style={{ color: "#555", marginBottom: 6 }}>{p.brand}</div>
              {p.cv_label && (
                <div style={{
                  display: "inline-block",
                  padding: "2px 8px",
                  borderRadius: 12,
                  background: "#eef",
                  color: "#225",
                  fontSize: 12,
                  marginBottom: 6
                }}>
                  Predicted: {p.cv_label}{typeof p.cv_conf === "number" ? ` (${p.cv_conf.toFixed(2)})` : ""}
                </div>
              )}
              <div style={{ color: "#666", fontSize: 13, marginBottom: 8 }}>
                Score: {typeof it.score === "number" ? it.score.toFixed(3) : it.score}
              </div>
              {p.images?.[0] && (
                <img
                  src={p.images[0]}
                  alt=""
                  style={{ width: "100%", height: 220, objectFit: "cover", borderRadius: 4, marginBottom: 8 }}
                />
              )}
              <div style={{ fontSize: 14, lineHeight: 1.4, marginBottom: 8 }}>
                {p.gen_description || "No description yet."}
              </div>
              <button onClick={() => genDesc(i)} disabled={!!busy[i]}>
                {busy[i] ? "Generating…" : "Generate description"}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}