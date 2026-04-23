import { useState } from "react";
import { loginUser } from "../services/auth";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await loginUser(form);
    alert(res.message || res.error);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form 
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-xl shadow-lg w-80"
      >
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>

        <input
          className="w-full p-2 mb-4 border rounded"
          placeholder="Username"
          onChange={e => setForm({...form, username: e.target.value})}
        />

        <input
          type="password"
          className="w-full p-2 mb-4 border rounded"
          placeholder="Password"
          onChange={e => setForm({...form, password: e.target.value})}
        />

        <button
          className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
        >
          Login
        </button>

        <p className="mt-4 text-sm text-center">
          New user? <a href="/register" className="text-blue-500">Register</a>
        </p>
      </form>
    </div>
  );
}
