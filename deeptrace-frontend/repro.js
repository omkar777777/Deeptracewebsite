import script from 'crypto-js';
console.log("Type of script:", typeof script);
console.log("Has SHA256:", !!script.SHA256);
console.log("Keys:", Object.keys(script).slice(0, 10));
