require('dotenv').config();

async function test() {
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${process.env.API_KEY}`
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      messages: [{ role: "user", content: "Test" }],
      temperature: 0.4,
      max_tokens: 1000
    })
  });

  const data = await response.text();
  console.log("Status:", response.status);
  console.log("Response:", data);
}

test();
