import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import App from './App.jsx';
import Analytics from './Analytics.jsx';

function Nav() {
  return (
    <div style={{ display:'flex', gap:12, padding:12, borderBottom:'1px solid #eee', marginBottom:12 }}>
      <Link to='/' style={{ textDecoration:'none' }}>Home</Link>
      <Link to='/analytics' style={{ textDecoration:'none' }}>Analytics</Link>
    </div>
  );
}

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Nav />
      <Routes>
        <Route path='/' element={<App />} />
        <Route path='/analytics' element={<Analytics />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);