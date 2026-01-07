/**
 * Configuration globale pour les tests Jest
 */

// Mock de l'API Chrome
global.chrome = {
  runtime: {
    sendMessage: jest.fn(),
    onMessage: {
      addListener: jest.fn(),
      removeListener: jest.fn()
    }
  },
  storage: {
    local: {
      get: jest.fn((keys, callback) => {
        if (callback) callback({});
      }),
      set: jest.fn((data, callback) => {
        if (callback) callback();
      }),
      remove: jest.fn((keys, callback) => {
        if (callback) callback();
      })
    }
  },
  tabs: {
    query: jest.fn((queryInfo, callback) => {
      if (callback) callback([{ id: 1, url: 'https://example.com' }]);
    })
  }
};

// Mock de fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    status: 200,
    json: () => Promise.resolve({}),
    text: () => Promise.resolve('')
  })
);

// Nettoyer les mocks avant chaque test
beforeEach(() => {
  jest.clearAllMocks();
});

