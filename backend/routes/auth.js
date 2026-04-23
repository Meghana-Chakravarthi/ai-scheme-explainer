import express from "express";
import { getDB } from "../db.js";

const router = express.Router();

// Register
router.post("/register", async (req, res) => {
  const { username, password } = req.body;
  const db = await getDB();

  await db.exec(`
    CREATE TABLE IF NOT EXISTS users(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE,
      password TEXT
    )
  `);

  try {
    await db.run(
      "INSERT INTO users (username, password) VALUES (?, ?)",
      [username, password]
    );
    res.json({ message: "Registered successfully" });
  } catch {
    res.status(400).json({ error: "User already exists" });
  }
});

// Login
router.post("/login", async (req, res) => {
  const { username, password } = req.body;
  const db = await getDB();

  const user = await db.get(
    "SELECT * FROM users WHERE username=? AND password=?",
    [username, password]
  );

  if (user) {
    res.json({ message: "Login success" });
  } else {
    res.status(401).json({ error: "Invalid credentials" });
  }
});

export default router;
