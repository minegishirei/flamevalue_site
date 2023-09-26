// vue.config.js
module.exports = {
  runtimeCompiler: true,
  publicPath: '/flamevalue_site/code/vue-notus/dist/',
  devServer: {
    public: '0.0.0.0:8080'
  }
};

/*
  transpileDependencies: true,
  outputDir: 'docs',
  publicPath: '/github-pages.beaver/',
  configureWebpack: {
    entry: "./src/main.js",
    devServer: {
      hot: true,
    },
    watch: true,
    watchOptions: {
      ignored: /node_modules/,
      poll: 1000,
    },
  },
}
*/