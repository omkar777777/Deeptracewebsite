import React from "react";

function MediaSelector({ mode, setMode }) {
  return (
    <div>
      <label>Mode</label>
      <select value={mode} onChange={(e) => setMode(e.target.value)}>
        <option value="image">Image</option>
        <option value="text">Text</option>
      </select>
    </div>
  );
}

export default MediaSelector;