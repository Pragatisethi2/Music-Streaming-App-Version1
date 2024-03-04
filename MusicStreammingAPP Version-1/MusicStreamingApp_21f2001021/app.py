from flask import Flask 
from flask_restful import Api
from application.data.database import db
from application.apis.api import *
from application.apis.creator_api import *
from application.apis.playlist.create_playlist import *
from application.apis.album.create_album import *
from flask_jwt_extended import JWTManager
from application.security import user_datastore, security
from flask_cors import CORS


from application.apis.auth.registerAPI import RegisterAPI


def create_app():
    app = Flask(__name__)
    api = Api(app)
    # __name__ is the special function which gives the name of the current local python file 
    # This is needed so that Flask knows where to look for resources such as templates and static file
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY']='28ef91619bab9f89d5689b25'
    
    api.init_app(app)
    db.init_app(app)
    app.app_context().push()
    
    return app,api


app,api = create_app()  # Create the Flask app instance

# Flask CORS----------------------------------------
CORS(app, supports_credentials=True)


# Add CORS headers to every response-----------------
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'

    return response

@app.after_request
def after_request(response):
    response = add_cors_headers(response)
    return response


# JWT initialization-----------------------------------
# JWTManager(app)

# Flask Security--------------------------------------
security.init_app(app, user_datastore)

from application.routes import *

with app.app_context():
    db.create_all()
    
api.add_resource(AllAlbum , "/api/album")
api.add_resource(AllSongs , "/api/songs")
api.add_resource(AllSongsApi , "/api/all_songs" , "/api/create")
api.add_resource(Creator_song , "/api/creator_song/<int:id>" , "/api/delete_song/<int:id>", '/api/update_song/<int:Id>')
api.add_resource(SongsApi , "/api/songs/<int:id>")
api.add_resource(ApiPlaylist,"/api/playlist/create" , "/api/all_playlist/<int:id>" , '/api/delete_playlist/<int:id>' ,"/api/update_playlist/<int:id>" )
api.add_resource(ApiAll_Albums,"/api/all_album")
api.add_resource(ApiAlbum,"/api/album/create" , "/api/all_album/<int:id>" , '/api/delete_album/<int:id>')
api.add_resource(ApiAlbumId,"/api/album/<int:id>")
api.add_resource(ApiSong_In_Playlist,"/api/song_in_playlist/<int:id>")
api.add_resource(ApiSong_In_Album,"/api/song_in_album/<int:id>")
api.add_resource(ApiAvailable_Songs , "/api/available_song/<int:id>" )
if __name__ == '__main__':
    app.run(debug=True,port=5000)