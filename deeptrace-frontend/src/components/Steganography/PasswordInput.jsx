import React from "react";

function PasswordInput({ password, setPassword }) {
  return (
    <>
      <label>Password (optional)</label>
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Enter password"
      />
    </>
  );
}

export default PasswordInput;