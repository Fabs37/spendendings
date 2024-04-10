import os

from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, 'spendendings.sqlite'),
    )
    
    if test_config is None:
        if not os.path.exists(os.path.join(app.instance_path, "config.py")):
            import spendendings._defaultconfig
            app.config.from_object(spendendings._defaultconfig)
        else:
            app.config.from_pyfile("config.py")
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    
    from . import db
    db.init_app(app)
    
    from . import projectlist
    app.register_blueprint(projectlist.bp)
    
    from . import form
    app.register_blueprint(form.bp)
    
    @app.errorhandler(404)
    @app.errorhandler(400)
    def err4xx(message):
        return render_template("error.html", name=message.name, code=message.code, msg=message.description, supressgh=True), message.code
    
    return app

# import werkzeug.exceptions as we

# we.NotFound().

