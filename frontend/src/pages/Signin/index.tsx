import { useState } from "react";
import { useSigninMutation } from "features/auth/authApi";
import { ErrorResponse } from "features/auth/types";
import { normalizeApiError } from "utils/normalizeApiError";

const Signin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [signin, { isLoading, error, isError }] = useSigninMutation();
  const errors = normalizeApiError<ErrorResponse>(error)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await signin({ email, password });
  };

  return (
    <div>
      <h2>Sign in</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit" disabled={isLoading}>{isLoading ? "Signin..." : "Signin"}</button>
        {isError && (
          <div>
            <p>{errors?.data.email}</p>
            <p>{errors?.data.password}</p>
            <p>{errors?.data.detail}</p>
            <p>{errors?.data.non_field_errors}</p>
          </div>
        )}
      </form>
    </div>
  );
};

export default Signin;
