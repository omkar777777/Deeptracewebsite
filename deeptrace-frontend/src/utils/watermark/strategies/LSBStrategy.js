import CryptoJS from 'crypto-js';
const { SHA256 } = CryptoJS;

/**
 * Linear Congruential Generator (LCG) for pseudo-random number generation.
 * Seeded by the secret key.
 */
class PMRNG {
    constructor(seed) {
        this.m = 0x80000000;
        this.a = 1103515245;
        this.c = 12345;
        this.state = seed ? this.stringToSeed(seed) : Math.floor(Math.random() * (this.m - 1));
    }

    stringToSeed(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = (hash << 5) - hash + char;
            hash = hash & hash; // Convert to 32bit integer
        }
        return Math.abs(hash);
    }

    nextInt() {
        this.state = (this.a * this.state + this.c) % this.m;
        return this.state;
    }

    // Fisher-Yates shuffle using our seeded PRNG
    shuffle(array) {
        let currentIndex = array.length, temporaryValue, randomIndex;
        while (0 !== currentIndex) {
            randomIndex = this.nextInt() % currentIndex;
            currentIndex -= 1;
            temporaryValue = array[currentIndex];
            array[currentIndex] = array[randomIndex];
            array[randomIndex] = temporaryValue;
        }
        return array;
    }
}

export const embedLSB = async (imageFile, options) => {
    const { secretKey, text } = options;
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

                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const data = imageData.data;

                // 1. Prepare Watermark Data
                const timestamp = Date.now();
                const rawData = JSON.stringify({
                    id: "user_" + Math.floor(Math.random() * 10000), // Simulate User ID
                    ts: timestamp,
                    hash: SHA256(secretKey + timestamp).toString(),
                    text: text || "" // Include user text
                });

                // Convert string to binary string
                let binaryWatermark = "";
                for (let i = 0; i < rawData.length; i++) {
                    const bin = rawData.charCodeAt(i).toString(2).padStart(8, "0");
                    binaryWatermark += bin;
                }

                // Add null terminator (8 zeros)
                binaryWatermark += "00000000";

                const totalPixels = data.length / 4;
                if (binaryWatermark.length > totalPixels) {
                    reject("Image too small to hold watermark data.");
                    return;
                }

                // 2. Randomized Embedding Positions
                // Create an array of indices [0, 1, 2, ... totalPixels-1]
                const indices = new Uint32Array(totalPixels);
                for (let i = 0; i < totalPixels; i++) indices[i] = i;

                // Shuffle indices using secret key
                const rng = new PMRNG(secretKey);
                rng.shuffle(indices);

                // 3. Embed Data
                for (let i = 0; i < binaryWatermark.length; i++) {
                    const pixelIndex = indices[i];
                    const dataIndex = pixelIndex * 4; // R channel of the random pixel
                    const bit = parseInt(binaryWatermark[i]);

                    // Clear LSB and set new bit
                    data[dataIndex] = (data[dataIndex] & ~1) | bit;
                }

                ctx.putImageData(imageData, 0, 0);
                resolve({
                    dataUrl: canvas.toDataURL("image/png"),
                    watermarkData: rawData
                });
            };
            img.onerror = reject;
            img.src = event.target.result;
        };
        reader.onerror = reject;
        reader.readAsDataURL(imageFile);
    });
};

export const extractLSB = async (imageFile, options) => {
    const { secretKey } = options;
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

                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const data = imageData.data;
                const totalPixels = data.length / 4;

                // 1. Recreate Randomized Indices
                const indices = new Uint32Array(totalPixels);
                for (let i = 0; i < totalPixels; i++) indices[i] = i;

                const rng = new PMRNG(secretKey);
                rng.shuffle(indices);

                // 2. Extract Bits
                let binaryString = "";
                let nullCharCount = 0;

                // We assume the data won't fill the entire image, but we need a limit to prevent crash
                const maxBits = Math.min(totalPixels, 100000); // Limit to ~12KB of data for safety

                for (let i = 0; i < maxBits; i++) {
                    const pixelIndex = indices[i];
                    const dataIndex = pixelIndex * 4;
                    const bit = data[dataIndex] & 1; // Read LSB of R channel
                    binaryString += bit;

                    // Check for null terminator (8 zeros) every 8 bits
                    if (binaryString.length % 8 === 0) {
                        const lastByte = binaryString.slice(-8);
                        if (lastByte === "00000000") {
                            // Found terminator
                            binaryString = binaryString.slice(0, -8);
                            break;
                        }
                    }
                }

                // 3. Convert Binary to Text
                try {
                    let text = "";
                    for (let i = 0; i < binaryString.length; i += 8) {
                        const byte = binaryString.slice(i, i + 8);
                        text += String.fromCharCode(parseInt(byte, 2));
                    }

                    // Try parsing JSON if possible, otherwise return raw text
                    try {
                        const json = JSON.parse(text);

                        // Added: Verification Logic
                        const reHash = SHA256(secretKey + json.ts).toString();
                        const isSignatureValid = reHash === json.hash;

                        resolve({
                            isValid: isSignatureValid,
                            decoded: json,
                            raw: text,
                            timestamp: new Date(json.ts).toLocaleString(),
                            userId: json.id,
                            text: json.text || "" // Added text field
                        });
                    } catch {
                        resolve({
                            isValid: false,
                            isRaw: true,
                            decoded: null,
                            raw: text
                        });
                    }

                } catch (err) {
                    reject("Failed to decode watermark data. Possible key mismatch.");
                }
            };
            img.onerror = reject;
            img.src = event.target.result;
        };
        reader.onerror = reject;
        reader.readAsDataURL(imageFile);
    });
};
