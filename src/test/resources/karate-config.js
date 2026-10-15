function fn() {
  karate.configure('connectTimeout', 15000);
  karate.configure('readTimeout', 60000);
  karate.configure('headers', { Accept: 'application/json', 'Content-Type': 'application/json' });
  return {
    baseUrl: karate.properties['api.baseUrl'] || 'https://taller-de-tecnicas-de-prueba-de-caja.onrender.com/api'
  };
}
