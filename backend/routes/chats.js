const express = require('express');
const router = express.Router();
const Chat = require('../models/Chat');

// Get all chats for a specific user
router.get('/:userId', async (req, res) => {
  try {
    const chats = await Chat.find({ userId: req.params.userId, isDeleted: false }).sort({ updatedAt: -1 });
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

// Delete a chat (Soft Delete)
router.delete('/:id', async (req, res) => {
  try {
    await Chat.findByIdAndUpdate(req.params.id, { isDeleted: true });
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

// Process a new message and communicate with OpenAI securely
router.post('/:id/message', async (req, res) => {
  try {
    const { message } = req.body;
    
    // 1. Add user message locally
    const chat = await Chat.findByIdAndUpdate(
      req.params.id,
      { $push: { messages: message } },
      { new: true }
    );
    if (!chat) return res.status(404).json({ error: "Conversa não encontrada." });

    // 2. Comunicar com a OpenAI internamente
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${process.env.API_KEY}`
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: chat.messages.map(m => ({ role: m.role, content: m.content })),
        temperature: 0.6,
        max_tokens: 1000
      })
    });

    if (!response.ok) throw new Error("Erro na comunicação com OpenAI");

    const data = await response.json();
    const botReply = data.choices?.[0]?.message?.content?.trim() || "Não consegui gerar resposta.";
    const botMsgObj = { role: "assistant", content: botReply };

    // 3. Atualizar DB com a resposta do Bot
    await Chat.findByIdAndUpdate(
      req.params.id,
      { $push: { messages: botMsgObj } }
    );

    // 4. Gerar título se for a primeira mensagem do usuário (RF14)
    let newTitle = null;
    const userMessages = chat.messages.filter(m => m.role === 'user');
    if (userMessages.length === 1 && chat.title === "Nova Conversa") {
        try {
            const titleResponse = await fetch("https://api.openai.com/v1/chat/completions", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${process.env.API_KEY}`
                },
                body: JSON.stringify({
                    model: "gpt-4o-mini",
                    messages: [
                        { role: "system", content: "Gere um título forte, curto e explicativo para este chat baseado na mensagem do usuário. Retorne apenas o título, sem aspas, com no máximo 30 caracteres." },
                        { role: "user", content: userMessages[0].content }
                    ],
                    temperature: 0.7,
                    max_tokens: 50
                })
            });
            if (titleResponse.ok) {
                const titleData = await titleResponse.json();
                newTitle = titleData.choices?.[0]?.message?.content?.trim().replace(/['"]/g, '');
                if (newTitle) {
                    await Chat.findByIdAndUpdate(req.params.id, { title: newTitle });
                }
            }
        } catch (titleErr) {
            console.error("Erro ao gerar título:", titleErr);
        }
    }

    // 5. Retornar resposta ao frontend
    res.status(200).json({ botMsgObj, newTitle });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
