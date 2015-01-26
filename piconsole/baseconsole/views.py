import importlib
from flask import render_template
from piconsole import app, settings

apps = []
for modname in settings.INSTALLED_APPS:
    m = importlib.import_module('piconsole.{}'.format(modname))
    url = ''
    for rule in app.url_map.iter_rules():
        if rule.endpoint == m.ENDPOINT:
            url = rule.rule
    apps.append((m.NAME, url, m.DISPLAY_NAME))

@app.route('/')
def index():
    context = {
        'apps': apps,
    }
    return render_template('main.html', **context)
