import React from "react";

function ActionButtons({
  mode,
  loading,
  onEmbedImage,
  onExtractImage,
  onEmbedText,
  onExtractText,
  disabled
}) {
  return (
    <>
      {mode === "image" && (
        <>
          <button onClick={onEmbedImage} disabled={loading || disabled}>
            Embed & Download
          </button>
          <button onClick={onExtractImage} disabled={loading || disabled}>
            Extract
          </button>
        </>
      )}

      {mode === "text" && (
        <>
          <button onClick={onEmbedText} disabled={loading}>
            Embed
          </button>
          <button onClick={onExtractText} disabled={loading}>
            Extract
          </button>
        </>
      )}
    </>
  );
}

export default ActionButtons;