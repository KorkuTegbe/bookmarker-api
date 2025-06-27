import os
from flask_jwt_extended import JWTManager
from flask import Flask, redirect, jsonify, send_file
from database import db, Bookmark
from auth import auth
from bookmarks import bookmarks
from datetime import timedelta
from constants.status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookmarks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_SECRET_KEY"] = 'secret'

docs_file_location=os.path.abspath(os.path.join(os.path.dirname(__file__), '..','spec','api.yaml'))
print(docs_file_location)
# SWAGGER
swaggerui_blueprint = get_swaggerui_blueprint('/docs', '/spec/api.yaml', config={
   'app_name': "Bookmarker API"
})


db.init_app(app)

with app.app_context():
   db.create_all()

JWTManager(app)

@app.get('/<short_url>')
def redirect_to_url(short_url):
   bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

   if bookmark:
      bookmark.visits = bookmark.visits+1
      db.session.commit()

      return redirect(bookmark.url)


# blueprints
app.register_blueprint(swaggerui_blueprint, url_prefix='/docs')
app.register_blueprint(auth)
app.register_blueprint(bookmarks)


# #### Serve YAML file
@app.route('/static/api.yaml')
def send_yaml():
   return send_file(docs_file_location, mimetype='text/yaml')



@app.errorhandler(HTTP_404_NOT_FOUND)
def handle_404(e):
   return jsonify({'error': "Not Found"}), HTTP_404_NOT_FOUND

@app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
def handle_500(e):
   return jsonify({'error': "Internal Server Error"}), HTTP_500_INTERNAL_SERVER_ERROR


if __name__ == "__main__":
   app.run() 