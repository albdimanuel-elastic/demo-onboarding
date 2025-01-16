const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Frontend service is running!');
});

app.get('/call-backend', async (req, res) => {
  try {
    const backendResponse = await axios.get('http://backend-service:5000/');
    res.send(`Backend says: ${backendResponse.data}`);
  } catch (error) {
    res.status(500).send(`Error calling backend: ${error.message}`);
  }
});

app.listen(port, () => {
  console.log(`Frontend listening at http://localhost:${port}`);
});
