describe('Example E2E Test', () => {
  test('should pass', () => {
    expect(true).toBe(true);
  });

  test('should handle async operations', async () => {
    const result = await Promise.resolve('success');
    expect(result).toBe('success');
  });
});
