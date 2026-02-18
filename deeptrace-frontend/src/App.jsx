import { BrowserRouter, Routes, Route } from "react-router-dom";
import { lazy, Suspense, useState, useEffect } from "react";

import Navbar from "./components/Navbar";

// Core pages (safe, eager load)
import Home from "./pages/Home";
import ModuleSelect from "./pages/ModuleSelect";
import Crypto from "./pages/Crypto";
import WatermarkSelect from "./pages/WatermarkSelect";
import WatermarkEmbed from "./pages/WatermarkEmbed";
import WatermarkRecover from "./pages/WatermarkRecover";
import Analysis from "./pages/Analysis";
import About from "./pages/About";

// ⚠️ Steganography is lazy-loaded to prevent global crash
const Stego = lazy(() => import("./pages/Stego"));

function App() {
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  return (
    <BrowserRouter>
      <div className="app-layout">
        <Navbar theme={theme} toggleTheme={toggleTheme} />

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

            {/* Watermark Sub-modules */}
            <Route path="/watermark" element={<WatermarkSelect />} />
            <Route path="/watermark/embed" element={<WatermarkEmbed />} />
            <Route path="/watermark/recover" element={<WatermarkRecover />} />

            <Route path="/watermark" element={<WatermarkSelect />} />
            <Route path="/analysis" element={<Analysis />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;