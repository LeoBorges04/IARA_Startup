const express = require('express');
const router = express.Router();
const User = require('../models/User');
const bcrypt = require('bcryptjs');

// Register
router.post('/register', async (req, res) => {
  try {
    const { name, email, password } = req.body;
    
    // Check if user exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ error: 'Este e-mail já está cadastrado.' });
    }

    // Hash password
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    // Create user
    const newUser = new User({
      name,
      email,
      password: hashedPassword
    });

    const savedUser = await newUser.save();
    res.status(201).json({ message: 'Cadastro realizado com sucesso!', user: { name: savedUser.name, email: savedUser.email } });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Login
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    // Acesso admin hardcoded fallback
    if (email === "admin@admin.com" && password === "admin") {
        return res.status(200).json({ name: "Admin", email });
    }

    // Check if user exists
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(400).json({ error: 'E-mail ou senha inválidos.' });
    }

    // Check pass
    const validPass = await bcrypt.compare(password, user.password);
    if (!validPass) {
      return res.status(400).json({ error: 'E-mail ou senha inválidos.' });
    }

    res.status(200).json({ name: user.name, email: user.email });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
