from django.contrib.staticfiles.apps import StaticFilesConfig


class CustomStaticFilesConfig(StaticFilesConfig):
    ignore_patterns = [
        "node_modules",
        "src",
        ".babelrc",
        "package.json",
        "server.js",
        "webpack.base.config.js",
        "webpack.dev.config.js",
        "webpack.prod.config.js",
        "webpack-stats-dev.json",
        "webpack-stats-prod.json",
        "yarn.lock",
    ]