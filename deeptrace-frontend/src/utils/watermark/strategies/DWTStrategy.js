import api from "../../../services/api";
import CryptoJS from 'crypto-js';
const { SHA256 } = CryptoJS;

export const embedDWT = async (imageFile, options = {}) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = async (event) => {
            try {
                const dataUrl = event.target.result;
                const secretKey = options.secretKey;

                if (!secretKey) {
                    reject("Secret Key is required for DWT watermarking.");
                    return;
                }

                // Prepare Payload
                const timestamp = Date.now();
                const payload = JSON.stringify({
                    id: "user_" + Math.floor(Math.random() * 10000),
                    ts: timestamp,
                    hash: SHA256(secretKey + timestamp).toString(),
                    text: options.text || ""
                });

                // Send to Backend
                const response = await api.post("/watermark/embed", {
                    image: dataUrl,
                    type: "invisible_dwt",
                    secretKey: secretKey,
                    text: payload
                });

                resolve({
                    dataUrl: response.data.dataUrl,
                    watermarkData: payload
                });

            } catch (error) {
                console.error("DWT Embed Error:", error);
                reject(error.response?.data?.error || error.message);
            }
        };
        reader.onerror = reject;
        reader.readAsDataURL(imageFile);
    });
};

export const extractDWT = async (imageFile, options = {}) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = async (event) => {
            try {
                const dataUrl = event.target.result;
                const secretKey = options.secretKey;

                if (!secretKey) {
                    reject("Secret Key is required for DWT extraction.");
                    return;
                }

                const response = await api.post("/watermark/extract", {
                    image: dataUrl,
                    type: "invisible_dwt",
                    secretKey: secretKey
                });

                const text = response.data.data.message;

                // Verification Logic
                try {
                    const json = JSON.parse(text);
                    const reHash = SHA256(secretKey + json.ts).toString();
                    const isSignatureValid = reHash === json.hash;

                    resolve({
                        isValid: isSignatureValid,
                        decoded: json,
                        raw: text,
                        timestamp: new Date(json.ts).toLocaleString(),
                        userId: json.id,
                        text: json.text || ""
                    });
                } catch {
                    resolve({
                        isValid: false,
                        isRaw: true,
                        decoded: null,
                        raw: text
                    });
                }

            } catch (error) {
                console.error("DWT Extract Error:", error);
                reject(error.response?.data?.error || error.message);
            }
        };
        reader.onerror = reject;
        reader.readAsDataURL(imageFile);
    });
};
