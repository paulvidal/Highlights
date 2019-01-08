from django.contrib.staticfiles.apps import StaticFilesConfig


class CustomStaticFilesConfig(StaticFilesConfig):
    ignore_patterns = [
        "node_modules",
        "src",
        ".babelrc",
        "package.json",
        "server.js",
        "webpack.base.config",
        "webpack.dev.config",
        "webpack.prod.config",
        "webpack-stats-dev.json",
        "webpack-stats-prod.json",
        "yarn.lock",
    ]