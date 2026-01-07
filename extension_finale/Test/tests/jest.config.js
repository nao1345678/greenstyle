module.exports = {
  testEnvironment: 'jsdom',
  testMatch: [
    '**/Test/tests/extension/**/*.test.js',
    '**/Test/tests/extension/**/*.js'
  ],
  collectCoverageFrom: [
    'extensions/**/*.js',
    '!extensions/**/*.min.js'
  ],
  coverageDirectory: 'coverage',
  setupFilesAfterEnv: ['<rootDir>/tests/setupTests.js'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/../$1'
  }
};

