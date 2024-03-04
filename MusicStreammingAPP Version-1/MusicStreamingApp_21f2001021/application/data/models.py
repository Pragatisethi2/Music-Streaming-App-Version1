from sqlalchemy.sql import func
from .database import db
from flask_security import UserMixin, RoleMixin

UserRoles = db.Table('UserRoles',
                    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255)) 

class User(db.Model , UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String() , nullable=False)
    password = db.Column(db.String() , nullable=False)
    email_id = db.Column(db.String() , nullable=False)
    date_created = db.Column(db.DateTime(timezone=True) , default=func.now())   
    iscreator = db.Column(db.Boolean(), default=False)
    isadmin = db.Column(db.Boolean(), default=False)
    roles = db.Column(db.String(), default="user")     
    songs=db.relationship("Songs",backref="user")
    is_blacklist = db.Column(db.Integer(),default=0)
    user_playlist=db.relationship("Playlist" ,backref="user")
    user_album = db.relationship("Album",backref = "user")
    songs_rating = db.relationship("SongRatings" , backref="user")
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    roles = db.relationship('Role', secondary=UserRoles,
                            backref=db.backref('users', lazy='dynamic'))
    
    def is_active(self):
        return True

    def get_id(self):
        return(self.id)


class Songs(db.Model):
    __tablename__ = 'songs'
    id=db.Column(db.Integer(),autoincrement=True,primary_key=True)
    song_title=db.Column(db.String(),nullable=False)
    release_date=db.Column(db.String(),nullable=False)
    created_by=db.Column(db.String())
    lyrics = db.Column(db.String(),nullable=False)
    genre = db.Column(db.String(),nullable=False)
    language = db.Column(db.String(),nullable=False)
    song_url=db.Column(db.String(),nullable=False)
    song_pic=db.Column(db.String())
    is_flag = db.Column(db.Integer(),default=0)
    creator_id=db.Column(db.Integer(),db.ForeignKey("user.id"),nullable=False)
    playlist_id = db.relationship("SongInPlaylist",backref="songs",cascade="all, delete-orphan")
    songs_rating = db.relationship("SongRatings" , backref="songs",cascade="all, delete-orphan")
    album_id = db.relationship("SongInAlbum", backref = "songs",cascade="all, delete-orphan")
    
    def __init__(self, song_title , release_date,created_by,lyrics,genre,language,song_url,song_pic,creator_id):
        
        self.song_title=song_title
        self.release_date=release_date
        self.created_by= created_by
        self.lyrics=lyrics
        self.genre=genre
        self.language=language
        self.song_url=song_url
        self.song_pic=song_pic
        self.creator_id=creator_id
        
class Playlist(db.Model):
    __tablename__ = 'playlist'
    playlist_id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    playlist_name = db.Column(db.String(),nullable=False)
    song_in_playlist=db.relationship("SongInPlaylist",backref="playlist",cascade="all, delete-orphan")
    created_by = db.Column(db.Integer(),db.ForeignKey("user.id"),nullable=False)

class SongInPlaylist(db.Model):
    __tablename__ = 'song_in_playlist'
    
    playlist_id = db.Column(db.Integer(), db.ForeignKey("playlist.playlist_id"), nullable=False, primary_key = True)
    song_id = db.Column(db.Integer(), db.ForeignKey("songs.id") ,primary_key=True)
        
class SongRatings(db.Model):
    __tablename__ = "song_rating"
    song_id = db.Column(db.Integer() , db.ForeignKey("songs.id"),primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"),primary_key=True)
    ratings = db.Column(db.Integer())
    
class Album(db.Model):
    __tablename__="album"
    album_id = db.Column(db.Integer(), primary_key=True , autoincrement=True)    
    album_name = db.Column(db.String())
    is_flag = db.Column(db.Integer(),default=0)
    song_in_album=db.relationship("SongInAlbum",backref="album", cascade="all, delete-orphan")
    created_by = db.Column(db.Integer(),db.ForeignKey("user.id"),nullable=False)
    
class SongInAlbum(db.Model):
    __tablename__ = 'song_in_album'
    album_id = db.Column(db.Integer(), db.ForeignKey("album.album_id"), nullable=False, primary_key = True)
    song_id = db.Column(db.Integer(), db.ForeignKey("songs.id"), primary_key = True)


