module.exports = {
    env: {
      browser: true,
      es2021: true,
      node: true,
      jest: true, // For test files
    },
    extends: [
      'eslint:recommended',
      'plugin:react/recommended',
      'plugin:react-hooks/recommended',
      'plugin:jsx-a11y/recommended',
      'plugin:import/errors',
      'plugin:import/warnings',
      'plugin:jest/recommended',
    ],
    parserOptions: {
      ecmaFeatures: {
        jsx: true,
      },
      ecmaVersion: 'latest',
      sourceType: 'module',
    },
    plugins: [
      'react',
      'react-hooks',
      'jsx-a11y',
      'import',
      'jest',
    ],
    settings: {
      react: {
        version: 'detect', // Automatically detect React version
      },
      'import/resolver': {
        node: {
          extensions: ['.js', '.jsx', '.ts', '.tsx'],
        },
      },
    },
    rules: {
      // React rules
      'react/react-in-jsx-scope': 'off', // Not needed in React 17+
      'react/prop-types': 'warn', // Warn about missing prop validations
      'react/jsx-uses-react': 'off', // Not needed in React 17+
      'react/jsx-filename-extension': ['warn', { extensions: ['.jsx', '.tsx'] }],
      'react/jsx-props-no-spreading': 'off', // Allow JSX prop spreading
      'react/jsx-pascal-case': 'warn', // Components should use PascalCase
      
      // React Hooks
      'react-hooks/rules-of-hooks': 'error', // Enforce Rules of Hooks
      'react-hooks/exhaustive-deps': 'warn', // Check effect dependencies
      
      // General JavaScript
      'no-console': 'warn', // Warning for console.log, etc.
      'no-unused-vars': ['warn', { 
        argsIgnorePattern: '^_', 
        varsIgnorePattern: '^_' 
      }], // Warn for unused variables except those starting with _
      'no-debugger': 'warn', // Warn for debugger statements
      'no-alert': 'warn', // Warn for alert, prompt, confirm
      'prefer-const': 'warn', // Use const instead of let when possible
      'arrow-body-style': ['warn', 'as-needed'], // Short arrow functions when possible
      
      // Import rules
      'import/no-unresolved': 'error', // Error for unresolved imports
      'import/order': ['warn', {
        groups: [
          'builtin', // Built-in imports (come from NodeJS)
          'external', // External imports
          'internal', // Absolute imports
          ['sibling', 'parent'], // Relative imports
          'index', // index imports
          'object', // Object imports
        ],
        'newlines-between': 'always',
      }],
  
      // Accessibility
      'jsx-a11y/anchor-is-valid': ['warn', {
        components: ['Link'],
        specialLink: ['to'],
      }],
      'jsx-a11y/click-events-have-key-events': 'warn',
      'jsx-a11y/no-static-element-interactions': 'warn',
    },
    overrides: [
        {
          files: [
            '**/*.test.js',
            '**/*.test.jsx',
            '**/*.spec.js',
            '**/*.spec.jsx',
            '**/tests/**',
            '**/__tests__/**'  // Add this pattern for Jest's __tests__ directory
          ],
          env: {
            jest: true,
          },
          rules: {
            'no-undef': 'off',
          },
          // You can also explicitly set globals
          globals: {
            test: 'readonly',
            expect: 'readonly',
            describe: 'readonly',
            beforeEach: 'readonly',
            afterEach: 'readonly',
            jest: 'readonly',
          }
        }
      ],
  };