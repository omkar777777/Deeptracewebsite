import { embedLSB, extractLSB } from "./strategies/LSBStrategy";
import { embedDCT, extractDCT } from "./strategies/DCTStrategy";
import { embedDWT, extractDWT } from "./strategies/DWTStrategy";
import { embedVisible } from "./strategies/VisibleStrategy";

class WatermarkEngine {
    static async applyWatermark(type, imageFile, options = {}) {
        if (!imageFile) throw new Error("No image data provided.");

        switch (type) {
            case "visible":
                if (!options.text) throw new Error("Watermark text is required for visible watermarking.");
                return await embedVisible(imageFile, options.text, options);

            case "invisible_lsb":
                if (!options.secretKey) throw new Error("Secret Key is required for LSB watermarking.");
                return await embedLSB(imageFile, options);

            case "invisible_dct":
                return await embedDCT(imageFile, options);

            case "invisible_dwt":
                return await embedDWT(imageFile, options);

            default:
                throw new Error(`Unknown watermark type: ${type}`);
        }
    }

    static async recoverWatermark(type, imageFile, options = {}) {
        if (!imageFile) throw new Error("No image data provided.");

        switch (type) {
            case "visible":
                return await extractLSB(imageFile, { secretKey: "VISIBLE_DEFAULT_KEY" });

            case "invisible_lsb":
                if (!options.secretKey) throw new Error("Secret Key is required for LSB extraction.");
                return await extractLSB(imageFile, options);

            case "invisible_dct":
                return await extractDCT(imageFile, options);

            case "invisible_dwt":
                return await extractDWT(imageFile, options);

            default:
                throw new Error(`Recovery not supported for type: ${type}`);
        }
    }
}

export default WatermarkEngine;
