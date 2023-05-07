module.exports = {
  presets: [
    [
      '@babel/preset-env',
      {
        // https://babeljs.io/docs/en/babel-preset-env#modules
        modules: false, // Enable transformation of ES module syntax to another module type. Note that cjs is just an alias for commonjs
        // https://babeljs.io/docs/en/babel-preset-env#targets
        targets: {
          browsers: [
            '>= 0.25%',
            'ie >= 11',
          ]
        },
        "useBuiltIns": "entry", // https://stackoverflow.com/a/62337595/617559
        // https://babeljs.io/docs/en/babel-preset-env#corejs
        // "corejs": { version: "3.12", proposals: true },
        // FIXME: 2023-02-05: Use more recent version
        "corejs": { version: "3.27", proposals: true },
        // https://babeljs.io/docs/en/babel-preset-env#forcealltransforms
        "forceAllTransforms": true,
      }
    ]
  ],
  plugins: [
      '@babel/plugin-transform-runtime',
  ],
};
