import { useState } from "react";
import { useSigninMutation } from "../../features/auth/authApi";

const Signin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [signin, { isLoading, error }] = useSigninMutation();

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
        <button type="submit" disabled={isLoading}>Signin</button>
        {error && <p style={{ color: "red" }}>Signin failed</p>}
      </form>
    </div>
  );
};

export default Signin;
