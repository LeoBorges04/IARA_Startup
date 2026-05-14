const mongoose = require('mongoose');
require('dotenv').config();
mongoose.connect(process.env.MONGODB_URI).then(async () => {
  const Chat = require('./models/Chat');
  const chats = await Chat.find().sort({ updatedAt: -1 }).limit(1);
  console.log(JSON.stringify(chats, null, 2));
  process.exit(0);
});
