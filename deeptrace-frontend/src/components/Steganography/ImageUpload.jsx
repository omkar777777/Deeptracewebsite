import React from "react";

function ImageUpload({ setImageFile }) {
  return (
    <>
      <label>Cover Image</label>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setImageFile(e.target.files[0])}
      />
    </>
  );
}

export default ImageUpload;