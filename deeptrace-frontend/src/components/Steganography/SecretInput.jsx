import React from "react";

function SecretInput({ label = "Secret Message", value, setValue }) {
  return (
    <>
      <label>{label}</label>
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
    </>
  );
}

export default SecretInput;