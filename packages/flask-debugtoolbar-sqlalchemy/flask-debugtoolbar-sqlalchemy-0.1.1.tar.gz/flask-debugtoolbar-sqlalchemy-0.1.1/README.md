Flaks debug toolbar SQLAlchemy panel
====================================

Similar to the
[builtin SQLAlchemy toolbar](https://flask-debugtoolbar.readthedocs.io/en/latest/panels.html#sqlalchemy)
but does not require the `Flask-SQLAlchemy` extension.

Displayed in toolbar:

![Toolbar view](http://bezdomni.net/pics/sqlalchemy_panel_1.png)

Panel details:

![Panel view](http://bezdomni.net/pics/sqlalchemy_panel_2.png)

Install
-------

From the cheese shop:

```
pip install flask-debugtoolbar-sqlalchemy
```

Setup
-----

Bootstrap the toolbar
[as usual](https://flask-debugtoolbar.readthedocs.io/en/latest/#usage) and add
SQLAlchemyPanel to the list of panels.

```py
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True

toolbar = DebugToolbarExtension(app)

app.config['DEBUG_TB_PANELS'] += (
    'flask_debugtoolbar_sqlalchemy.SQLAlchemyPanel',
)
```
