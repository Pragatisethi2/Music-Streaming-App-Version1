from flask_restful import Resource , Api ,reqparse
from flask import jsonify
from flask_login import current_user
from application.data.models import *



class Creator_song(Resource):
    
    def get(self,id):
        # user = User.query.filter_by(id=id).first()
        # if user.is_blacklist==False:
    
        all_songs= Songs.query.filter_by(creator_id=id , is_flag=0).all()
        if all_songs:
            songs= {}
            i=1
            
            for song in all_songs:
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
                s['Creator_id']=id
                
                songs[f'song_{i}'] = s
                i+=1
            return jsonify({'songs':songs , 'total_songs':i-1})
        return jsonify({'songs':{},'total_songs':0})
    
    def delete(self,id):
        songs = Songs.query.filter_by(id=id).all()  
        print(songs)
        if songs:
            for song in songs:
                db.session.delete(song)
                db.session.commit()      
            return jsonify({'status':"success",'message' : 'Song has been deleted!'})
        return jsonify({'status':"failed",'message' : 'Song does not exist'})
    
    
    def put(self, Id):
        parser = reqparse.RequestParser()
        parser.add_argument('Song_Title', type=str)
        parser.add_argument('Release_Date', type=str)
        parser.add_argument('Genre', type=str)
        parser.add_argument('Language', type=str)
        parser.add_argument('Lyrics', type=str)
        
        args = parser.parse_args()

        # Find the song by ID
        song = Songs.query.filter_by(id=Id).first()
        if song:
            # Update the song attributes if provided in the request
            Song_title = args['Song_Title']
            Release_date=args['Release_Date']
            Genre = args['Genre']
            Language=args['Language']
            Lyrics = args['Lyrics']
            song.song_title = Song_title
            song.release_date=Release_date
            song.genre = Genre
            song.language =Language
            song.lyrics=Lyrics
            db.session.commit()

            return jsonify({'message': 'Song updated successfully', 'status':'success'})
        
        return jsonify({'message': 'Song not found' ,'status':'danger'})
                
    

# {
#       "Genre": "Romantic",
#       "Language": "Hindi",
#       "Lyrics": "Kyon Aaj Kal neend kam Khwab zaada hai Lagta Khuda ka koi neek iraada hai Kal tha Fakeer aaj dil shezada hai Lagta Khuda ka koi neek iraada hai  Kya Mujhe Pyaar hai ya Kaisa Khumar hai ya Kya Mujhe Pyaar hai ya Kaisa Khumar hai ya  Pathar ke in raston pe Phoolon ke ek chaadar hai Jabse mile ho humko Badla har ek manzar hai  Dekho jahaan main neele neele asmaan thale Rang naye naye hai jaise ghulte huwe Sohye se khwab mere jaage tere waaste Tere khayalon se hai bheege mere raaste  Kya Mujhe Pyaar hai ya Kaisa Khumar hai ya Kya Mujhe Pyaar hai ya Kaisa Khumar hai ya  Tum kyon chale aate ho Har raaz hain in khwaabon main Chupke se aa bhi jaao ek din meri bahoon main  Tere he saapnein andheron mein ujaalon mein Koi naasha hain tere aankhon ke pyalo mein Tu mere khwabon mein jawabon mein sawaalon mein Har din churaa tumhe mein laaton hoon kyaalon mein  Kya Mujhe Pyaar hai ya Kaisa Khumar hai ya Kya Mujhe Pyaar hai ya Kaisa Khumar hai ya",
#       "Release_Date": "2015",
#       "Song_Title": "Yeh Tune Kya Kia",
#     }
            
