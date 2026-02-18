import api from "./api";

/* =====================================================
   STEGANALYSIS SERVICE
   Handles file upload and analysis request
===================================================== */

export const analyzeFile = async (file) => {
  if (!file) {
    throw new Error("No file provided for analysis.");
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await api.post(
      "/steganalysis/analyze",   // ✅ removed extra /api
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    return response.data;

  } catch (error) {
    console.error("Steganalysis API Error:", error);

    if (error.response && error.response.data) {
      throw new Error(error.response.data.error || "Analysis failed");
    }

    throw new Error("Server error during analysis.");
  }
};