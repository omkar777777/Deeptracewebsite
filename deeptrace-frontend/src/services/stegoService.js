import api from "./api";

/* ================= IMAGE STEGANOGRAPHY ================= */

export const embedImageStego = (
  imageFile,
  secret,
  algorithm = "lsb",
  password = ""
) => {
  const formData = new FormData();
  formData.append("file", imageFile);
  formData.append("secret", secret);
  formData.append("algorithm", algorithm);

  if (algorithm === "lsb-keyed") {
    formData.append("password", password);
  }

  return api.post("/stego/image/embed", formData, {
    responseType: "arraybuffer"
  });
};


export const extractImageStego = (
  imageFile,
  algorithm = "lsb",
  password = ""
) => {
  const formData = new FormData();
  formData.append("file", imageFile);
  formData.append("algorithm", algorithm);

  if (algorithm === "lsb-keyed") {
    formData.append("password", password);
  }

  return api.post("/stego/image/extract", formData);
};