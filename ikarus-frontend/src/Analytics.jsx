import { useEffect, useState } from "react";
const API = import.meta.env.VITE_API_BASE_URL;

export default function Analytics() {
  const [data, setData] = useState(null);
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const r = await fetch(`${API}/analytics/summary`);
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const j = await r.json();
        setData(j);
      } catch (e) {
        setErr(String(e?.message || e));
      }
    })();
  }, []);

  if (err) return <div style={{padding:16, color:"crimson"}}>Error: {err}</div>;
  if (!data) return <div style={{padding:16}}>Loading…</div>;

  return (
    <div style={{ padding:16 }}>
      <h2>Dataset Analytics</h2>

      <div style={{ display:"flex", gap:12, flexWrap:"wrap", margin:"12px 0" }}>
        <Stat title="Total Products" value={data.total_products ?? 0} />
        <Stat title="Images with URL" value={data.images_with ?? 0} />
        <Stat title="Avg Price" value={data.price?.avg?.toFixed?.(2) ?? "-"} />
        <Stat title="Median Price" value={data.price?.median?.toFixed?.(2) ?? "-"} />
      </div>

      <Section title="Top Categories">
        <List data={data.categories} />
      </Section>

      <Section title="Top CV Labels">
        <List data={data.cv_labels} />
      </Section>

      <Section title="Top Brands">
        <List data={data.top_brands} />
      </Section>
    </div>
  );
}

function Stat({ title, value }) {
  return (
    <div style={{ border:"1px solid #ddd", borderRadius:8, padding:12, minWidth:180 }}>
      <div style={{ fontSize:12, color:"#666" }}>{title}</div>
      <div style={{ fontSize:22, fontWeight:700 }}>{String(value)}</div>
    </div>
  );
}

function Section({ title, children }) {
  return (
    <div style={{ margin:"16px 0" }}>
      <h3 style={{ margin:"8px 0" }}>{title}</h3>
      {children}
    </div>
  );
}

function List({ data }) {
  if (!Array.isArray(data) || data.length === 0) return <div>None</div>;
  return (
    <div style={{ display:"grid", gridTemplateColumns:"repeat(2, minmax(220px, 1fr))", gap:8 }}>
      {data.map((x, i) => (
        <div key={i} style={{ display:"flex", justifyContent:"space-between", border:"1px solid #eee", borderRadius:6, padding:"8px 10px" }}>
          <span style={{ color:"#333" }}>{x.name}</span>
          <span style={{ color:"#555" }}>{x.count}</span>
        </div>
      ))}
    </div>
  );
}