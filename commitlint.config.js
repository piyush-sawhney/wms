module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'subject-empty': [2, 'never'],
    'type-empty': [2, 'never'],
    'type-case': [2, 'always', 'lower-case'],
    'type-enum': [
      2,
      'always',
      [
        'feat',     // new feature
        'fix',      // bug fix
        'docs',     // documentation only changes
        'style',    // formatting, code style changes
        'refactor', // code change that neither fixes a bug nor adds a feature
        'perf',     // performance improvements
        'test',     // adding tests
        'chore',    // tooling, configs, build process changes
        'ci'        // CI/CD related changes
      ]
    ]
  }
};
