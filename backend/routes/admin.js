const express = require('express');
const router = express.Router();
const User = require('../models/User');
const Chat = require('../models/Chat');

router.get('/users-chats', async (req, res) => {
  try {
    const users = await User.find({}, '-password').lean(); // all users without password
    const chats = await Chat.find({}).lean(); // all chats
    
    // Group chats by email (userId in Chat)
    const chatsByUser = {};
    chats.forEach(chat => {
      if (!chatsByUser[chat.userId]) {
         chatsByUser[chat.userId] = [];
      }
      chatsByUser[chat.userId].push(chat);
    });

    const enrichedUsers = users.map(user => {
      return {
        ...user,
        chats: chatsByUser[user.email] || []
      };
    });

    res.status(200).json(enrichedUsers);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
