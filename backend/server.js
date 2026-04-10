const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dns = require('dns');
require('dotenv').config();

// Force Node DNS to use public resolvers for Atlas SRV lookups
dns.setServers(['8.8.8.8', '1.1.1.1']);

const app = express();
const PORT = process.env.PORT || 3000;

const path = require('path');

// Middlewares
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/auth', require('./routes/auth'));
app.use('/api/chats', require('./routes/chats'));
app.use('/api/admin', require('./routes/admin'));

// Serve Static Frontend Files
app.use(express.static(path.join(__dirname, '../')));



// Start Server & Connect to DB
mongoose.connect(process.env.MONGODB_URI)
  .then(async () => {
    console.log('MongoDB: Conexão bem sucedida ao Atlas!');

    // Semear conta de administrador se não existir
    try {
      const User = require('./models/User');
      const bcrypt = require('bcryptjs');
      const adminEmail = 'adm@iara.com';
      const adminExists = await User.findOne({ email: adminEmail });
      
      if (!adminExists) {
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash('iara123', salt);
        const adminUser = new User({
          name: 'Administradores',
          email: adminEmail,
          password: hashedPassword,
          role: 'admin'
        });
        await adminUser.save();
        console.log('Conta de administrador criada com sucesso!');
      }
    } catch (seedErr) {
      console.error('Erro ao semear conta de admin:', seedErr);
    }

    app.listen(PORT, () => {
      console.log(`Servidor rodando na porta ${PORT}`);
    });
  })
  .catch(err => {
    console.error('Falha ao conectar no MongoDB Atlas:', err);
  });
