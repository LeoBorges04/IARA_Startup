const mongoose = require('mongoose');

const MessageSchema = new mongoose.Schema({
  role: { type: String, enum: ['system', 'user', 'assistant'], required: true },
  content: { type: String, required: true }
});

const ChatSchema = new mongoose.Schema({
  userId: { type: String, required: true }, // we can use email or a proper ObjectId depending on setup
  title: { type: String, default: "Nova Conversa" },
  messages: [MessageSchema],
  isDeleted: { type: Boolean, default: false },
}, { timestamps: true }); 

module.exports = mongoose.model('Chat', ChatSchema);
