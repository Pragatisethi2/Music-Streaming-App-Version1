from flask_restful import Resource ,reqparse
from flask import jsonify
from flask_login import current_user
from application.data.models import *
import requests

parser = reqparse.RequestParser()

parser.add_argument('Album_name')
parser.add_argument('Selected_songs', type=str, action='append', help='List of selected songs')
parser.add_argument('User_id')

class ApiAll_Albums(Resource):
    def get(self):
        # This functions query all the albums which is not flagged 
        all_albums=Album.query.filter_by(is_flag=0).all()
        albums={}
        i=1
        if all_albums:
            for album in all_albums:
               
                url=f'http://127.0.0.1:5000/api/song_in_album/{album.album_id}'
                responses = requests.get(url)
                response = responses.json()
                songs = response['songs']
                lists = {}
                lists['album_name'] = album.album_name.split('_')[0]
                lists['album_id'] = album.album_id
                lists['album_songs']=songs
                lists['is_flag']=album.is_flag
                albums[f'Album_{i}'] =lists
                print(lists)
                i+=1
            return jsonify({'albums':albums ,'total_albums':i-1})
        else:
            return jsonify({'message':'No album is created' , 'albums':{} , 'total_albums':0})
        
class ApiAlbum(Resource):
    def get(self,id):
        # all the album created by given creator id 
        all_album= Album.query.filter_by(created_by=id,is_flag=0).all()
        albums={}    
        i=1
        if all_album:
            for album in all_album:
                lists = {}
                lists['album_name'] = album.album_name.split('_')[0]
                lists['album_id'] = album.album_id
                lists['is_flag']=album.is_flag
                albums[f'Album_{i}'] =lists
                i+=1
            
            return jsonify({'albums':albums ,'total_albums':i-1})
        else:
            return jsonify({'message':'No album is created' , 'albums':{} , 'total_albums':0})
    
    def post(self):
        args = parser.parse_args()
        if args:
            unique_album_name = f"{args['Album_name']}_{args['User_id']}"
            
            if not Album.query.filter_by(created_by=args['User_id'], album_name=unique_album_name).first():
                # Playlist name is unique for this user, add it to the database
                new_album = Album(album_name=unique_album_name, created_by=args['User_id'])
                db.session.add(new_album)
                db.session.commit()
                album = Album.query.filter_by(album_name=unique_album_name).first()
                album_id = album.album_id
                selected_songs = args['Selected_songs']
                lists=[]
                for arg in selected_songs:
                    s = SongInAlbum(album_id=album_id, song_id=int(arg))
                    lists.append(s)
                for l in lists:
                    db.session.add(l)
                db.session.commit()
                return jsonify({ 'message' : 'Album Created' , 'status': 'success'})
            else:
                return jsonify({ 'message' : 'Album name should be unique' , 'status': 'danger'})
        return jsonify({ 'message' : 'No arguments given , cannot create the album' , 'status': 'danger'})
       
           
    def delete(self,id):
        album = Album.query.filter_by(album_id=id).first()
        if album:
            db.session.delete(album)
            db.session.commit()
            return jsonify({'status':"success",'message' : 'Album has been deleted!'})
        return jsonify({'status':"danger",'message' : 'Album does not exist'})
              
           
        
        
class ApiSong_In_Album(Resource):  
    
    def get(self,id):
        # all the songs present in an album whose id is given
        all_songs = SongInAlbum.query.filter_by(album_id=id).all()
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
        return jsonify({'songs':{}, 'message': "No Song Exist in the Album , Please add some"})
    

class ApiAvailable_Songs(Resource):
    def get(self, id):
    # Get all songs created by the specified user , and avilable for creating album 
    #  hence songs that is not a part of any album
        all_songs = Songs.query.filter_by(creator_id=id , is_flag=0).all()

        if all_songs:
            songs = {}
            i = 1

            for song in all_songs:
                # Check if the song is not already part of any album
                if not SongInAlbum.query.filter_by(song_id=song.id).first():
                    s = {}
                    s['Id'] = song.id
                    s['Song_Title'] = song.song_title
                    s['Release_Date'] = song.release_date
                    s['Created_by'] = song.created_by
                    s['Lyrics'] = song.lyrics
                    s['Genre'] = song.genre
                    s['Language'] = song.language
                    s['Song_url'] = song.song_url
                    s['Song_pic'] = song.song_pic
                    s['Creator_id'] = id
                    s['Is_Flag']  =song.is_flag
                    songs[f'song_{i}'] = s
                    i += 1

            return jsonify({'songs': songs})

        return jsonify({'songs': {}})
class ApiAlbumId(Resource):
    def get(self,id):
        # query album on the basis of given album id 
        all_album= Album.query.filter_by(album_id=id, is_flag=0).all()
        albums={}    
        i=1
        if all_album:
            for album in all_album:
                lists = {}
                lists['album_name'] = album.album_name.split('_')[0]
                lists['album_id'] = album.album_id
                lists['is_flag']=album.is_flag
                albums[f'Album_{i}'] =lists
                i+=1
            return jsonify({'albums':albums ,'total_albums':i-1})
        else:
            return jsonify({'message':'No album is created' , 'albums':{} , 'total_albums':0})
        
class AllAlbum(Resource):
    def get(self):
        # all the album whether flag or non-flag
        all_albums=Album.query.all()
        albums={}
        i=1
        if all_albums:
            for album in all_albums:               
                url=f'http://127.0.0.1:5000/api/song_in_album/{album.album_id}'
                responses = requests.get(url)
                response = responses.json()
                songs = response['songs']
                lists = {}
                lists['album_name'] = album.album_name.split('_')[0]
                lists['album_id'] = album.album_id
                lists['album_songs']=songs
                lists['is_flag']=album.is_flag
                albums[f'Album_{i}'] =lists
                print(lists)
                i+=1
            return jsonify({'albums':albums ,'total_albums':i-1})
        else:
            return jsonify({'message':'No album is created' , 'albums':{} , 'total_albums':0})

 # {
    #      'Album_name': "Playlists" , 
    #         'Selected_songs': ['1','2'],
    #         'User_id': 1
    #  }    