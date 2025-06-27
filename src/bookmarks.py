from flask import Blueprint, request, jsonify
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from constants.status_codes import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from database import db, Bookmark


bookmarks = Blueprint('bookmarks', __name__, url_prefix="/api/v1/bookmarks")

@bookmarks.route('/', methods=['POST', "GET"])
@jwt_required()
def bookmarker():
   current_user = get_jwt_identity()

   if request.method == 'POST':
      body = request.json.get('body', '')
      url = request.json.get('url', '')

      if not validators.url(url):
         return jsonify({
            'error': "Enter a valid url"
         }), HTTP_400_BAD_REQUEST
      
      if Bookmark.query.filter_by(url=url).first():   
         return jsonify({
            "error": "url already bookmarked"
         }), HTTP_409_CONFLICT
      
      bookmark=Bookmark(body=body, url=url, user_id=current_user)
      db.session.add(bookmark)
      db.session.commit()

      return jsonify({
         'bookmark': bookmark.serialize()
      }), HTTP_201_CREATED
   
   else:
      page = request.args.get('page', 1, type=int)
      per_page=request.args.get('per_page', 5, type=int)

      bookmarks = Bookmark.query.filter_by(
         user_id=current_user).paginate(page=page, per_page=per_page)
      
      meta={
         "page": bookmarks.page,
         "pages": bookmarks.pages,
         "total_count": bookmarks.total,
         "prev_page": bookmarks.prev_num,
         "next_page": bookmarks.next_num,
         "has_next": bookmarks.has_next,
         "has_prev": bookmarks.has_prev,
      }

      return jsonify({
         "meta": meta,
         "bookmarks": [bookmark.serialize() for bookmark in bookmarks]
      })


@bookmarks.get('/<int:id>')
@jwt_required()
def get_bookmark(id):
   current_user = get_jwt_identity()

   bookmark = Bookmark.query.filter_by(user_id=current_user,id=id).first()

   if not bookmark:
      return jsonify({"message": "bookmark not found"}), HTTP_404_NOT_FOUND
   
   return jsonify({
      "bookmark": bookmark.serialize()
   }), HTTP_200_OK


@bookmarks.put('/<int:id>')
@bookmarks.patch('/<int:id>')
@jwt_required()
def edit_bookmark(id):
   current_user = get_jwt_identity()   
   body = request.json.get('body', '')
   url = request.json.get('url', '')

   if url:
      if not validators.url(url):
         return jsonify({
            'error': "Enter a valid url"
         }), HTTP_400_BAD_REQUEST

   bookmark = Bookmark.query.filter_by(user_id=current_user,id=id).first()

   if not bookmark:
      return jsonify({"message": "bookmark not found"}), HTTP_404_NOT_FOUND
   
   if body:
      bookmark.body = body
   if url:
      bookmark.url = url

   db.session.commit()

   return jsonify({"message": "Bookmark updated", "data": bookmark.serialize()}), HTTP_200_OK
   
@bookmarks.delete('/<int:id>')
@jwt_required()
def delete_bookmark(id):
   current_user = get_jwt_identity()

   bookmark = Bookmark.query.filter_by(user_id=current_user,id=id).first()

   if not bookmark:
      return jsonify({"message": "bookmark not found"}), HTTP_404_NOT_FOUND
   
   db.session.delete(bookmark)
   db.session.commit()

   return jsonify({
      "message": "bookmark deleted"
   }), HTTP_200_OK

@bookmarks.get('/stats')
@jwt_required()
def get_stats():
   current_user = get_jwt_identity()
   data=[]

   items=Bookmark.query.filter_by(user_id=current_user).all()

   for item in items:
      new_link={
         "visits": item.visits,
         "url": item.url,
         "id": item.id,
         "short_url": item.short_url
      }
      data.append(new_link)

   return jsonify({'data': data}), HTTP_200_OK