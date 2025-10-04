const fs = require('fs');
const path = require('path');

module.exports = {
  branches: [
    'develop',                                 // full semantic-release rules
    { name: 'dev-release', prerelease: false },  // patch-only
    { name: 'prod-release', prerelease: false }  // stable production
  ],
  plugins: [
    [
      '@semantic-release/commit-analyzer',
      {
        preset: 'angular',
        releaseRules: [
          { type: 'fix', release: 'patch' },
          { type: 'feat', release: 'minor' },
          { type: 'docs', release: false },
          { type: 'style', release: false },
          { type: 'refactor', release: 'patch' },
          { type: 'perf', release: 'patch' },
          { type: 'test', release: false },
          { type: 'chore', release: false },
          { type: 'ci', release: false }
        ],
        parserOpts: {
          noteKeywords: ['BREAKING CHANGE', 'BREAKING CHANGES']
        }
      }
    ],
    '@semantic-release/release-notes-generator',
    [
      '@semantic-release/changelog',
      {
        changelogFile: 'CHANGELOG.md'
      }
    ],
    [
      '@semantic-release/git',
      {
        assets: ['wms/__init__.py', 'CHANGELOG.md'],
        message: 'chore(release): ${nextRelease.version} [skip ci]'
      }
    ],
    [
      {
        verifyConditions: () => {},
        prepare: (pluginConfig, context) => {
          const { nextRelease, options, logger } = context;
          const branchName = options.branch?.name; // safely get branch name

          if (!nextRelease) {
            logger.log('No nextRelease detected, skipping version update.');
            return;
          }

          // Only allow patch bumps on dev-release
          if (branchName === 'dev-release' && nextRelease.type !== 'patch') {
            throw new Error(
              'Only patch releases allowed on dev-release. Commit types must be fixes.'
            );
          }

          // Update __version__ in wms/__init__.py
          const initFile = path.resolve(__dirname, 'wms/__init__.py');
          let content = fs.readFileSync(initFile, 'utf8');

          content = content.replace(
            /^__version__\s*=\s*['"].*['"]/m,
            `__version__ = "${nextRelease.version}"`
          );

          fs.writeFileSync(initFile, content, { encoding: 'utf8' });

          logger.log(`Updated ${initFile} to version ${nextRelease.version}`);
        }
      }
    ]
  ]
};
