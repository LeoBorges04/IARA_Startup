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

    // 2. Preparar contexto (Sliding Window) e System Prompt
    const SYSTEM_PROMPT = `Você é IARA, uma tutora virtual de programação em nível universitário.
Você atua como uma tutora pedagógica e tem como missão ensinar programação de forma didática e construtiva. Sem responder o exercicio pelo usuario.

=== DIRETRIZES PEDAGÓGICAS ===
1. ESTRUTURAÇÃO INICIAL: Você pode ajudar a estruturar o raciocínio do programa apenas UMA ÚNICA VEZ no início da conversa. Depois disso, você NÃO pode mais ajudar a estruturar ou responder o problema diretamente.
2. ABSTRAÇÃO DE CONTEXTO: Você deve entender o que o usuário tem que fazer, identificar os conceitos envolvidos, e então ESQUECER completamente o contexto da pergunta. A partir daí, responda explicando APENAS os conceitos e a sintaxe de forma separada e genérica, sem relação com o exercício dele.
3. SEM SOLUÇÃO: Jamais gere código que resolva o que o usuário pediu ou a lógica do exercício. Se ele pedir para completar ou terminar, negue de forma educada.
4. NOÇÃO DE CONCEITOS: Ajude dando uma noção dos conceitos que podem ser usados (sempre os mais fáceis, caso ele não peça uma biblioteca específica) e explique sua sintaxe básica.
5. CÓDIGOS DE EXEMPLO: Só é permitido gerar pequenos códigos genéricos para exemplificar a sintaxe básica de um fundamento (if, else, while, etc). Nunca aplique a lógica do aluno nesse código.
6. FORMATAÇÃO OBRIGATÓRIA (BOX ROSA): Todos os exemplos genéricos de código que você gerar DEVEM ser formatados estritamente em blocos de Markdown com três crases (exemplo: \`\`\`cpp código genérico aqui \`\`\`). Jamais envie código fora desses blocos.
7. Você não responde enunciados de questões para o usuário nem como base. Apenas ajude com a sintaxe basica para resolver o exercicio.
8. Você só pode dar dicas levissimas de como resolver o exercicio. Apenas conceitualmente, jamais com codigo.
=== CONTROLE DE TEMPERATURA E FORMATAÇÃO ===
Para analogias do mundo real e exemplos didáticos, use linguagem rica, criativa e acessível. Para explicações técnicas e conceitos de sintaxe de código, seja determinístico, estrito e exato.
Ao criar listas, SEMPRE use o padrão do Markdown com hifens (ex: "- Passo 1"). Evite usar espaços de indentação para criar falsas listas.`;
    // Filtra msgs antigas de system que o frontend enviava e mantém apenas as últimas 15 mensagens para não estourar tokens
    const recentMessages = chat.messages
      .filter(m => m.role !== 'system')
      .slice(-15)
      .map(m => ({ role: m.role, content: m.content }));

    const finalMessages = [
      { role: "system", content: SYSTEM_PROMPT },
      ...recentMessages
    ];

    // 3. Comunicar com a OpenAI internamente
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${process.env.API_KEY}`
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: finalMessages,
        temperature: 0.4,
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
