async function run() {
  try {
    // 1. Create a chat
    const createRes = await fetch('http://localhost:3000/api/chats', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId: 'admin@admin.com', title: 'Nova Conversa' })
    });
    const chat = await createRes.json();
    console.log('Created chat:', chat._id);

    // 2. Send a message
    const msgRes = await fetch(`http://localhost:3000/api/chats/${chat._id}/message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: { role: 'user', content: 'Hello' } })
    });

    const msgData = await msgRes.text();
    console.log('Message response:', msgRes.status, msgData);
  } catch (err) {
    console.error(err);
  }
}
run();
