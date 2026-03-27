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
      "steganalysis/analyze",
      formData
      // ⚠ Do NOT manually set Content-Type.
      // Axios automatically sets correct multipart boundary.
    );

    return response.data;

  } catch (error) {
    console.error("Steganalysis API Error:", error);

    // If backend returned structured error
    if (error.response?.data) {
      const backendError =
        error.response.data.error ||
        error.response.data.details ||
        error.response.data.message;

      if (backendError) {
        throw new Error(backendError);
      }
    }

    // Network / CORS / unexpected failure
    throw new Error("Server error during analysis.");
  }
};