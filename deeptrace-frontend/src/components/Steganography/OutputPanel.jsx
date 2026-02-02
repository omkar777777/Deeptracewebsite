import React from "react";

function OutputPanel({ result, error }) {
  return (
    <>
      <label>Result</label>
      <div className="crypto-output">
        {result || "No output yet"}
      </div>

      {error && <div className="crypto-error">{error}</div>}
    </>
  );
}

export default OutputPanel;