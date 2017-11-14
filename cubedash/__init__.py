import sys

import flask


from . import _filters, _dataset, _platform, _product, _api

app = flask.Flask('cubedash')
app.register_blueprint(_filters.bp)
app.register_blueprint(_api.bp)
app.register_blueprint(_dataset.bp)
app.register_blueprint(_platform.bp)
app.register_blueprint(_product.bp)


@app.route('/')
def default_redirect():
    """Redirect to default starting page."""
    return flask.redirect(flask.url_for('product.spatial_page', product='ls7_level1_scene'))


if __name__ == '__main__':
    DEBUG_MODE = len(sys.argv) == 2 and sys.argv[1] == '--debug'
    app.jinja_env.auto_reload = DEBUG_MODE
    app.run(port=8080, debug=DEBUG_MODE)
