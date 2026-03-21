const express = require('express');
const router = express.Router();
const Chat = require('../models/Chat');

// Get all chats for a specific user
router.get('/:userId', async (req, res) => {
  try {
    const chats = await Chat.find({ userId: req.params.userId }).sort({ updatedAt: -1 });
    res.status(200).json(chats);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Create a new chat
router.post('/', async (req, res) => {
  try {
    const { userId, title, messages } = req.body;
    const newChat = new Chat({
      userId,
      title: title || "Nova Conversa",
      messages: messages || []
    });
    const savedChat = await newChat.save();
    res.status(201).json(savedChat);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Push a new message to a chat & update title if provided
router.put('/:id', async (req, res) => {
  try {
    const { title, message } = req.body;
    
    let updateDoc = { $set: {} };
    if (title) updateDoc.$set.title = title;
    
    // Add msg if payload has it
    if (message) {
        updateDoc.$push = { messages: message };
    }

    const updatedChat = await Chat.findByIdAndUpdate(
      req.params.id,
      updateDoc,
      { new: true }
    );
    res.status(200).json(updatedChat);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Delete a chat
router.delete('/:id', async (req, res) => {
  try {
    await Chat.findByIdAndDelete(req.params.id);
    res.status(200).json({ message: "Conversa excluída com sucesso." });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Rename a chat 
router.put('/:id/rename', async (req, res) => {
  try {
    const { title } = req.body;
    const updatedChat = await Chat.findByIdAndUpdate(
      req.params.id,
      { $set: { title } },
      { new: true }
    );
    res.status(200).json(updatedChat);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
