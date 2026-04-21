const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();

// Fix 1 — use environment variable instead of hardcoded localhost
const API_URL = process.env.API_URL || "http://api:8000";

app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));

app.post('/submit', async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/jobs`);
    res.json(response.data);
  } catch (err) {
    // Fix 2 — return actual error message instead of hiding it
    res.status(500).json({ error: err.message });
  }
});

app.get('/status/:id', async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/jobs/${req.params.id}`);
    res.json(response.data);
  } catch (err) {
    // Fix 2 — return actual error message instead of hiding it
    res.status(500).json({ error: err.message });
  }
});

// Fix 3 — add /health endpoint for Docker HEALTHCHECK
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.listen(3000, () => {
  console.log('Frontend running on port 3000');
});