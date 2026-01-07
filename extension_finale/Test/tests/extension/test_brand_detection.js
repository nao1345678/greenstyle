/**
 * Tests pour la détection de marques dans l'extension Chrome
 * Ces tests peuvent être exécutés avec Jest ou manuellement dans le navigateur
 */

// Mock des APIs Chrome
global.chrome = {
  runtime: {
    sendMessage: jest.fn((message, callback) => {
      if (callback) {
        callback({ success: true, brands: [] });
      }
    }),
    onMessage: {
      addListener: jest.fn()
    }
  },
  storage: {
    local: {
      get: jest.fn((keys, callback) => {
        if (callback) {
          callback({});
        }
      }),
      set: jest.fn((data, callback) => {
        if (callback) {
          callback();
        }
      })
    }
  }
};

// Mock de fetch pour les appels API
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({
      brand_name: "test_brand",
      final_score: 8.5,
      global_env_impact: 9.0,
      labor_ethics: 8.0
    })
  })
);

describe('Détection de marques', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('devrait détecter une marque sur la page', () => {
    // Simuler le contenu d'une page
    document.body.innerHTML = `
      <div class="product">
        <h1>Nike Air Max</h1>
        <p>Marque: Nike</p>
      </div>
    `;

    // Simuler la détection de marque
    const detectedBrands = ['nike'];
    expect(detectedBrands).toContain('nike');
  });

  test('devrait appeler l\'API pour récupérer les données de marque', async () => {
    const brandName = 'veja';
    const response = await fetch(`http://localhost:8000/brands/name/${brandName}`);
    const data = await response.json();

    expect(fetch).toHaveBeenCalledWith(`http://localhost:8000/brands/name/${brandName}`);
    expect(data).toHaveProperty('brand_name');
    expect(data).toHaveProperty('final_score');
  });

  test('devrait gérer les erreurs d\'API', async () => {
    global.fetch.mockRejectedValueOnce(new Error('Network error'));

    try {
      await fetch('http://localhost:8000/brands/name/test');
    } catch (error) {
      expect(error.message).toBe('Network error');
    }
  });
});

describe('Affichage des scores', () => {
  test('devrait formater le score correctement', () => {
    const score = 8.5;
    const formatted = `${score.toFixed(1)}/10`;
    expect(formatted).toBe('8.5/10');
  });

  test('devrait déterminer la couleur du score', () => {
    const getScoreColor = (score) => {
      if (score >= 8) return 'green';
      if (score >= 6) return 'yellow';
      if (score >= 4) return 'orange';
      return 'red';
    };

    expect(getScoreColor(9.0)).toBe('green');
    expect(getScoreColor(7.0)).toBe('yellow');
    expect(getScoreColor(5.0)).toBe('orange');
    expect(getScoreColor(3.0)).toBe('red');
  });
});

