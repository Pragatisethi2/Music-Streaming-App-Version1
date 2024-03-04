from flask_restful import Resource ,reqparse
from flask import jsonify
from flask_login import current_user
from application.data.models import *
import requests

parser = reqparse.RequestParser()

parser.add_argument('Playlist_name')
parser.add_argument('Selected_songs', type=str, action='append', help='List of selected songs')
parser.add_argument('User_id')

class ApiPlaylist(Resource):
    def get(self,id):
    
        all_playlist= Playlist.query.filter_by(created_by=id).all()
        playlists={}    
        i=1
        if all_playlist:
            for playlist in all_playlist:
                lists = {}
                lists['playlist_name'] = playlist.playlist_name.split('_')[0]
                lists['playlist_id'] = playlist.playlist_id
                print(lists)
                playlists[f'Playlist_{i}'] =lists
                i+=1
            return jsonify({'playlists':playlists })
        else:
            return jsonify({'message':'No playlist is created' , 'playlists':{}})
    
    def post(self):
        args = parser.parse_args()
        if args:
           unique_playlist_name = f"{args['Playlist_name']}_{args['User_id']}"
           
           if not Playlist.query.filter_by(created_by=args['User_id'], playlist_name=unique_playlist_name).first():
            # Playlist name is unique for this user, add it to the database
                new_playlist = Playlist(playlist_name=unique_playlist_name, created_by=args['User_id'])
                db.session.add(new_playlist)
                db.session.commit()
                playlist = Playlist.query.filter_by(playlist_name=unique_playlist_name).first()
                playlist_id = playlist.playlist_id
                lists = args['Selected_songs']
                songs=[]
                for arg in lists:
                    
                    s = SongInPlaylist(playlist_id=playlist_id , song_id=int(arg))
                    songs.append(s)
                for s in songs:
                    db.session.add(s)
                db.session.commit()
                return jsonify({
                    'message': 'New Playlist Created' , 'status':'success'
                })
           else:
                return jsonify({ 'message' : 'Playlist name should be unique' , 'status': 'danger'})
        return jsonify({'message' : 'No arguments given , cannot create the playlist' , 'status': 'danger'})
       
           
    def delete(self,id):
        playlist = Playlist.query.filter_by(playlist_id=id).first()
        if playlist:
            db.session.delete(playlist)
            db.session.commit()
            return jsonify({'status':"success",'message' : 'Playlist has been deleted!'})
        return jsonify({'status':"danger",'message' : 'Playlist does not exist'})
        
    def put(self,id):
        args = parser.parse_args()
        playlist = Playlist.query.filter_by(playlist_id=id)
        print(playlist)
        
        if args:
           unique_playlist_name = f"{args['Playlist_name']}_{args['User_id']}"
           
           if not Playlist.query.filter_by(created_by=args['User_id'], playlist_name=unique_playlist_name).first():
                playlist.playlist_name=unique_playlist_name
                db.session.commit()
                songs_in_playlist = SongInPlaylist.query.filter_by(playlist_id=id).all()
                existing_song_ids = {song.song_id for song in songs_in_playlist}
                for song in songs_in_playlist:
                    if song.song_id not in args['Selected_songs']:
    
                        db.session.delete(song)
                        db.session.commit()

                # Check songs to add to the playlist    
                for song_id in args['Selected_songs']:
                    if song_id not in existing_song_ids:
                        # Add the song to the playlist
                        new_song = SongInPlaylist(playlist_id=id, song_id=song_id)
                        db.session.add(new_song)

                db.session.commit()
                return {'message': 'Playlist updated successfully', 'status': 'success'}
        else:
            return {'message': 'Playlist not found', 'status': 'error'}, 404
        
class ApiSong_In_Playlist(Resource):  
    
    def get(self,id):
    
        all_songs = SongInPlaylist.query.filter_by(playlist_id=id).all()
        songs={}
        i=1
        if all_songs:
            for song in all_songs:
                url=f'http://127.0.0.1:5000/api/songs/{song.song_id}'
                responses=requests.get(url)
                response=responses.json()
                song=response['songs']
                songs[f'song_{i}'] =song
                i+=1
            return jsonify({'songs':songs})
        return jsonify({'songs':{}, 'message': "No Song Exist in the Track , Please add some"})
            
    
    # {
    #      'Playlist_name': "Playlists" , 
    #         'Selected_songs': ['1','2'],
    #         'User_id': 1
    #  }    