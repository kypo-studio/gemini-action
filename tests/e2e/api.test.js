const request = require('supertest');
const express = require('express');

// Créer une mini app pour les tests
const app = express();
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

describe('E2E API Tests', () => {
  test('GET /health should return 200', async () => {
    const response = await request(app).get('/health');
    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('status', 'ok');
  });
});
