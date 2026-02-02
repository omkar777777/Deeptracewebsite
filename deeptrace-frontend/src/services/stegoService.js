import api from "./api";

/* ================= TEXT STEGANOGRAPHY ================= */

// EMBED → must use ARRAYBUFFER (not blob)
export const embedTextStego = (coverText, secret, algorithm) => {
  return api.post(
    "/stego/text/embed",
    {
      cover_text: coverText,
      secret,
      algorithm
    },
    {
      responseType: "arraybuffer"   // 🔥 CRITICAL FIX
    }
  );
};

// EXTRACT → multipart form (already correct)
export const extractTextStego = (file, algorithm) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("algorithm", algorithm);

  return api.post("/stego/text/extract", formData);
};