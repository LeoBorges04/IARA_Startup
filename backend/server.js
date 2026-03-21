const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

const path = require('path');

// Middlewares
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/auth', require('./routes/auth'));
app.use('/api/chats', require('./routes/chats'));

// Serve Static Frontend Files
app.use(express.static(path.join(__dirname, '../')));



// Start Server & Connect to DB
mongoose.connect(process.env.MONGODB_URI)
  .then(() => {
    console.log('MongoDB: Conexão bem sucedida ao Atlas!');
    app.listen(PORT, () => {
      console.log(`Servidor rodando na porta ${PORT}`);
    });
  })
  .catch(err => {
    console.error('Falha ao conectar no MongoDB Atlas:', err);
  });
