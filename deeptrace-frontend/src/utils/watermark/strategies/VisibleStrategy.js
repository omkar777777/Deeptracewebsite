import { embedLSB } from "./LSBStrategy";

export const embedVisible = async (imageFile, text, options = {}) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);

                // Options
                const fontSize = options.fontSize || Math.max(20, img.width * 0.05); // Responsive font size
                const opacity = options.opacity || 0.5;
                const color = options.color || "white";
                const position = options.position || "center"; // center, bottomRight, etc.

                ctx.font = `bold ${fontSize}px sans-serif`;
                ctx.globalAlpha = opacity;
                ctx.fillStyle = color;
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";

                let x, y;
                if (position === "center") {
                    x = canvas.width / 2;
                    y = canvas.height / 2;
                } else if (position === "topLeft") {
                    x = (ctx.measureText(text).width / 2) + 20;
                    y = fontSize + 20;
                } else if (position === "topRight") {
                    x = canvas.width - (ctx.measureText(text).width / 2) - 20;
                    y = fontSize + 20;
                } else if (position === "bottomLeft") {
                    x = (ctx.measureText(text).width / 2) + 20;
                    y = canvas.height - fontSize - 20;
                } else if (position === "bottomRight") {
                    x = canvas.width - (ctx.measureText(text).width / 2) - 20;
                    y = canvas.height - fontSize - 20;
                } else {
                    x = canvas.width / 2;
                    y = canvas.height / 2;
                }

                // Draw Shadow for better visibility
                ctx.shadowColor = "rgba(0,0,0,0.5)";
                ctx.shadowBlur = 4;
                ctx.shadowOffsetX = 2;
                ctx.shadowOffsetY = 2;

                ctx.fillText(text, x, y);

                canvas.toBlob(async (blob) => {
                    if (!blob) {
                        reject("Failed to create blob from canvas");
                        return;
                    }
                    try {
                        // Embed metadata so it can be extracted later
                        const result = await embedLSB(blob, {
                            secretKey: "VISIBLE_DEFAULT_KEY",
                            text: text
                        });
                        resolve(result);
                    } catch (err) {
                        reject(err);
                    }
                }, imageFile.type);
            };
            img.onerror = reject;
            img.src = event.target.result;
        };
        reader.onerror = reject;
        reader.readAsDataURL(imageFile);
    });
};
