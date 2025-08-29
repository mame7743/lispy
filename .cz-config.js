module.exports = {
  types: [
    { value: '✨ feat', name: '✨ feat:     新機能の追加' },
    { value: '🐛 fix', name: '🐛 fix:      バグ修正' },
    { value: '📝 docs', name: '📝 docs:     ドキュメントのみの変更' },
    { value: '🎨 style', name: '🎨 style:    コードの整形' },
    { value: '♻️ refactor', name: '♻️ refactor: リファクタリング' },
    { value: '🚀 perf', name: '🚀 perf:     パフォーマンス改善' },
    { value: '🧪 test', name: '🧪 test:     テストの追加・修正' },
    { value: '🔨 chore', name: '🔨 chore:    ビルド・開発環境' },
    { value: '🔧 ci', name: '🔧 ci:       CI/CD設定' },
    { value: '🎉 init', name: '🎉 init:     プロジェクト初期化' }
  ],

  scopes: ['interpreter', 'test', 'config', 'commitizen', 'setup'],
  allowCustomScopes: true,
  allowBreakingChanges: ['feat', 'fix'],
  subjectLimit: 100
};