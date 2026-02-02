import React from "react";

function AlgorithmSelect({ algorithm, setAlgorithm }) {
  return (
    <div>
      <label>Algorithm</label>
      <select
        value={algorithm}
        onChange={(e) => setAlgorithm(e.target.value)}
      >
        <option value="whitespace">Whitespace</option>
        <option value="zerowidth">Zero Width</option>
      </select>
    </div>
  );
}

export default AlgorithmSelect;