from flask_restful import Resource ,reqparse
from flask import jsonify
from flask_login import current_user
from application.data.models import *


#flask_restful
# class ---> method(function) ---> functionality ---> define routes
parser = reqparse.RequestParser()
parser.add_argument('Song_Title')
parser.add_argument('Release_Date')
parser.add_argument('Created_by')
parser.add_argument('Lyrics')
parser.add_argument('Genre')
parser.add_argument('Language')
parser.add_argument('Song_pic')
parser.add_argument('Song_url')
parser.add_argument('Creator_id')

class AllSongsApi(Resource):
    def get(self):
        all_songs = Songs.query.filter_by(is_flag=0).all()
        if all_songs:
            songs= {}
            genres = set()
            i=1
            for song in all_songs :
                s={}
                s['Id'] =  song.id
                s['Song_Title'] = song.song_title
                s['Release_Date']=song.release_date
                s['Created_by']=song.created_by
                s['Lyrics'] =song.lyrics
                s['Genre'] = song.genre
                s['Language'] = song.language
                s['Song_url'] =song.song_url
                s['Song_pic'] = song.song_pic
                s['Creator_id']=song.creator_id
                s['Is_Flag']  =song.is_flag
                
                
                genres.add(song.genre) 
                songs[f'song_{i}'] = s
                i+=1
                genres_list = list(genres)  # Convert set to list for JSON serialization
                response = {'songs': songs, 'genres': genres_list}
            return jsonify(response)
        else:
            # Handle the case where there are no songs in the database
            return jsonify({'message': 'No songs found' , 'songs':{} , 'genres':[]})

    
    def post(self):
        args = parser.parse_args()
        if args:
            song = Songs(song_title =args['Song_Title'] , release_date=args['Release_Date'],
                        created_by=args['Created_by'],lyrics=args['Lyrics'],
                        genre=args['Genre'], language=args['Language'],song_url=args['Song_url'],
                        song_pic=args['Song_pic'],creator_id=args['Creator_id'])
            
            db.session.add(song)
            db.session.commit()
            return jsonify({'message':'Song Added Successfully','status':'success' })
        return jsonify({'message':'Cannot add song , Please try again', 'status':'error'})                                                             
        
class SongsApi(Resource):
    def get(self,id):
        all_songs = all_songs= Songs.query.filter_by(id=id , is_flag=0).all()
        
        s= {}
        if all_songs:
        
            for song in all_songs:
                s['Id'] =  song.id
                s['Song_Title'] = song.song_title
                s['Release_Date']=song.release_date
                s['Created_by']=song.created_by
                s['Lyrics'] =song.lyrics
                s['Genre'] = song.genre
                s['Language'] = song.language
                s['Song_url'] =song.song_url
                s['Song_pic'] = song.song_pic
                s['Creator_id']=song.creator_id  
                s['Is_Flag']  =song.is_flag
            return jsonify({'songs':s})
        return jsonify({'songs':{}})
    
            
class AllSongs(Resource):
    def get(self):
        all_songs = Songs.query.filter_by().all()
        if all_songs:
            songs= {}
            genres = set()
            i=1
            for song in all_songs :
                s={}
                s['Id'] =  song.id
                s['Song_Title'] = song.song_title
                s['Release_Date']=song.release_date
                s['Created_by']=song.created_by
                s['Lyrics'] =song.lyrics
                s['Genre'] = song.genre
                s['Language'] = song.language
                s['Song_url'] =song.song_url
                s['Song_pic'] = song.song_pic
                s['Creator_id']=song.creator_id
                s['Is_Flag']  =song.is_flag
                
                genres.add(song.genre) 
                songs[f'song_{i}'] = s
                i+=1
                genres_list = list(genres)  # Convert set to list for JSON serialization
                response = {'songs': songs, 'genres': genres_list}
            return jsonify(response)
        else:
            # Handle the case where there are no songs in the database
            return jsonify({'message': 'No songs found' , 'songs':{} , 'genres':[]})


# {
#       "Creator_id": 1,
#       "Genre": "Romantic",
#       "Id": 1,
#       "Language": "Hindi",
#       "Lyrics": "Kyon Aaj Kal neend kam Khwab zaada hai Lagta Khuda ka koi neek iraada hai Kal tha Fakeer aaj dil shezada hai Lagta Khuda ka koi neek iraada hai  Kya Mujhe Pyaar hai ya Kaisa Khumar hai ya Kya Mujhe Pyaar hai ya Kaisa Khumar hai ya  Pathar ke in raston pe Phoolon ke ek chaadar hai Jabse mile ho humko Badla har ek manzar hai  Dekho jahaan main neele neele asmaan thale Rang naye naye hai jaise ghulte huwe Sohye se khwab mere jaage tere waaste Tere khayalon se hai bheege mere raaste  Kya Mujhe Pyaar hai ya Kaisa Khumar hai ya Kya Mujhe Pyaar hai ya Kaisa Khumar hai ya  Tum kyon chale aate ho Har raaz hain in khwaabon main Chupke se aa bhi jaao ek din meri bahoon main  Tere he saapnein andheron mein ujaalon mein Koi naasha hain tere aankhon ke pyalo mein Tu mere khwabon mein jawabon mein sawaalon mein Har din churaa tumhe mein laaton hoon kyaalon mein  Kya Mujhe Pyaar hai ya Kaisa Khumar hai ya Kya Mujhe Pyaar hai ya Kaisa Khumar hai ya",
#       "Release_Date": "2015",
#       "Song_Title": "Yeh Tune Kya Kia",
#       "Song_pic": "./static/song_pic/yeh_tune_kya_kia.jpg",
#       "Song_url": "./static/songs/Ye_Tune_Kya_Kiya.mp3"
#     }