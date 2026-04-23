import { useState } from "react";
import { registerUser } from "../services/auth";

export default function Register() {
  const [form, setForm] = useState({ username: "", password: "" });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await registerUser(form);
    alert(res.message || res.error);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form 
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-xl shadow-lg w-80"
      >
        <h2 className="text-2xl font-bold mb-6 text-center">Register</h2>

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
          className="w-full bg-green-500 text-white p-2 rounded hover:bg-green-600"
        >
          Register
        </button>

        <p className="mt-4 text-sm text-center">
          Already have account? <a href="/" className="text-blue-500">Login</a>
        </p>
      </form>
    </div>
  );
}
