# from flask import Flask,redirect
# import os
# from src.auth import auth
# from src.bookmarks import bookmarks
# from src.database import db, Bookmark
# from flask_jwt_extended import JWTManager


# def create_app(test_config=None):
#    app = Flask(__name__, instance_relative_config=True)

#    if test_config is None:
#       app.config.from_mapping(
#          SECRET_KEY=os.environ.get("SECRET_KEY "), #'dev',
#          SQLALCHEMY_DB_URI= 'sqlite:///bookmarks.db',#os.environ.get('SQLALCHEMY_DB_URL'),
#          JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
#       )
#    else:
#       app.config.from_mapping(test_config) 

#    # connect to database
#    db.app=app
#    db.init_app(app)

#    JWTManager(app)

#    @app.get('/<short_url>')
#    def redirect_to_url(short_url):
#       bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

#       if bookmark:
#          bookmark.visits = bookmark.visits+1
#          db.session.commit()

#          return redirect(bookmark.url)

#    # register blueprints
#    app.register_blueprint(auth)
#    app.register_blueprint(bookmarks)
   
#    return app
