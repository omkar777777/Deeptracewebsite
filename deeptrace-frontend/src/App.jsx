import { BrowserRouter, Routes, Route } from "react-router-dom";
import { lazy, Suspense } from "react";

import Navbar from "./components/Navbar";

// Core pages (safe, eager load)
import Home from "./pages/Home";
import ModuleSelect from "./pages/ModuleSelect";
import Crypto from "./pages/Crypto";
import Watermark from "./pages/Watermark";
import Analysis from "./pages/Analysis";

// ⚠️ Steganography is lazy-loaded to prevent global crash
const Stego = lazy(() => import("./pages/Stego"));

function App() {
  return (
    <BrowserRouter>
      <div className="app-layout">
        <Navbar />

        <div className="routes-container">
          <Routes>
            {/* Core pages */}
            <Route path="/" element={<Home />} />
            <Route path="/modules" element={<ModuleSelect />} />

            {/* DeepTrace Modules */}
            <Route path="/crypto" element={<Crypto />} />

            <Route
              path="/stego"
              element={
                <Suspense fallback={<div style={{ padding: 40 }}>Loading Steganography…</div>}>
                  <Stego />
                </Suspense>
              }
            />

            <Route path="/watermark" element={<Watermark />} />
            <Route path="/analysis" element={<Analysis />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;