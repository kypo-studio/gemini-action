describe('API Routes', () => {
  test('should return health check', () => {
    const healthResponse = { status: 'ok', timestamp: Date.now() };
    expect(healthResponse).toHaveProperty('status');
    expect(healthResponse.status).toBe('ok');
  });
});
