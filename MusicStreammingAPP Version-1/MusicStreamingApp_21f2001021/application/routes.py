from flask import Flask , render_template , url_for , redirect , request , flash , session , jsonify , after_this_request
from application.forms import  *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager ,login_user,login_required , logout_user , current_user
from flask import current_app as app
from flask_login import LoginManager
from application.data.models import *
import requests , secrets
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os



login_manager = LoginManager()


login_manager.init_app(app)   
login_manager.login_view = "user_login"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register',methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if request.method=='GET':
        return render_template('register.html',title='Register',form=form)    
    
    if request.method == "POST" and form.validate_on_submit() :
        name = form.name.data
        password=form.password.data
        email_id=form.email_id.data
        hashed_password = generate_password_hash(password)
        user = User(name=name,password=hashed_password,email_id=email_id )
        user.fs_uniquifier = secrets.token_hex(16)
        db.session.add(user)
        db.session.commit()
        flash('Your Account is created! Please Login.' , 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route('/user_login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method=='GET':
        
        return render_template('login.html',title='User Login',form=form , login='User Login')
    
    if request.method=='POST':
        email_id=form.email_id.data
        password=form.password.data 
        user = User.query.filter_by(email_id=email_id).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect('user_dashboard')
            else:
                flash("Wrong Password")
                return redirect("/user_login")
        else:
            flash("You are not registerd" , 'danger')
            return redirect("/user_login")
        
#---------------------------------------------------------------Admin Controllers-------------------------------------------------------------------
    
@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    form = LoginForm()
    if request.method=='GET':
       
        return render_template('login.html', title='Admin_Login',form=form,login="Admin Login" )
    if request.method == "POST":
        email_id=form.email_id.data
        password=form.password.data
        if email_id =='admin123@gmail.com' and int(password)==123456789:
            
            session['email_id']=email_id
            flash("welcome to admin dashboard",'success')
            return redirect(url_for('admin_dashboard'))
        else:
        
            flash("Invalid admin_id and password. You are not allowed to access admin dashboard " , "danger")
    return render_template('login.html', title='Admin_Login',form=form,login="Admin Login")

@app.route('/admin_logout')
def admin_logout():
    if ('email_id' in session):
        session.pop('email_id')
        return redirect(url_for('home'))

@app.route('/admin_dashboard')
def admin_dashboard():
    
    if ('email_id' in session):
        
        total_songs  = len(Songs.query.all())
        total_albums = len(Album.query.all())
        songs=Songs.query.all()
        users = User.query.all()
        total_genre = set()
        for song in songs:
            total_genre.add(song.genre)
        total_genres = len(total_genre)
        total_users = len(users)
        total_creator=0    
    
        for user in users:
            if user.iscreator==True:
                total_creator+=1
        plt.clf()
        graphs()
        graph2()
        return render_template('admin_dashboard.html' , total_songs=total_songs , total_albums=total_albums , total_users=total_users, total_creator=total_creator , total_genres=total_genres)
    
    flash('You are not allowed to access this page','danger')
    return redirect('/')

@app.route("/all_albums")
def all_albums():
    delete_album = request.args.get('delete_album')
    flag_albums = request.args.get('flag_album')
    album_id = request.args.get('album_id')  
    if ('email_id' in session):
        url=f'http://127.0.0.1:5000/api/album'
        responses=requests.get(url)
        response=responses.json()
        albums=response['albums']
        
        
        if str(delete_album).lower() == 'true':
            url2=f"http://127.0.0.1:5000/api/delete_album/{int(album_id)}"
            response2= requests.delete(url2)
            response=response2.json()
            flash(response['message'],response['status'])
            return(redirect(url_for('all_albums')))
        if str(flag_albums).lower() == 'true':
            album = Album.query.filter_by(album_id = int(album_id)).first()
            album.is_flag=1
            db.session.commit()
            flash('Album is flag','success')
            return(redirect(url_for('all_albums')))
        if str(flag_albums).lower() == 'false':
            album = Album.query.filter_by(album_id = int(album_id)).first()
            album.is_flag=0
            db.session.commit()
            flash('Album is unflag','success')
            return(redirect(url_for('all_albums')))
        
        return render_template('all_albums.html',albums=albums)
    flash('You are not allowed to access this page','danger')
    return redirect('/')
        
@app.route("/all_creators")
def all_creators():
    blacklist_creator=request.args.get('Blacklist_creator')
    user_id = request.args.get('user_id')
        #print('email_id' in session)
    if ('email_id' in session):
        users = User.query.filter_by(iscreator=True).all()
        if str(blacklist_creator).lower() == 'true':
            blacklist(int(user_id))
            flash("Creator is blacklisted" , "success")
            return redirect('/all_creators')
        if str(blacklist_creator).lower() == 'false':
            blacklist(int(user_id))
            flash("Creator is Whitelisted" , "success")
            return redirect('/all_creators')

        return render_template('all_creators.html', users=users)
    flash('You are not allowed to access this page','danger')
    return redirect('/')
        
@app.route("/all_songs")
def all_songs():
    flag_songs=request.args.get('flag_song')
    song_id = request.args.get('song_id')
    print('email_id' in session)
    if ('email_id' in session):
        delete_song = request.args.get('delete_song')
        song_id = request.args.get('song_id')
        url="http://127.0.0.1:5000/api/songs"
        response = requests.get(url)
        data = response.json()
        songs= data['songs']
        genres= data['genres']  
        
            
        if str(delete_song).lower() == 'true':
            url2=f"http://127.0.0.1:5000/api/delete_song/{int(song_id)}"
            response2= requests.delete(url2)
            response=response2.json()
            flash(response['message'],response['status'])
            return(redirect('/all_songs'))
        if str(flag_songs).lower() == 'true':
            song = Songs.query.filter_by(id = int(song_id)).first()
            song.is_flag=1
            db.session.commit()
            flash('Song is flag','success')
            return(redirect('/all_songs'))
        if str(flag_songs).lower() == 'false':
            song = Songs.query.filter_by(id = int(song_id)).first()
            song.is_flag=0
            db.session.commit()
            flash('Song is unflag','success')
            return(redirect('/all_songs'))
        
        return render_template('all_songs.html' , genres=genres , songs=songs)  
    flash('You are not allowed to access this page','danger')
    return redirect('/')

#------------------------------------------------------------------------User Controllers ---------------------------------------------------------

@app.route("/profile" , methods=['GET', 'POST'])
def profile():
    form = RegistrationForm(submit_name='Update')
    user = User.query.filter_by(id=current_user.id).first()
    update_profile = request.args.get('update_profile')
    if str(update_profile).lower() == 'true':
        return render_template('profile.html' , update_profile=True ,user=user ,form=form)
    if request.method=='POST' and form.validate_on_submit:
        user.name = form.name.data
        user.email_id = form.email_id.data
        db.session.commit()
        flash('Your Profile is updated!' , 'success')
        return redirect(url_for("profile"))        
    return render_template('profile.html' , update_profile=False , user=user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/user_dashboard")
@login_required
def user_dashboard():

    url="http://127.0.0.1:5000/api/all_songs"
    response = requests.get(url)
    data = response.json()
    songs= data['songs']
    genres= data['genres']
    id = current_user.id
    # print(songs)
    url2=f"http://127.0.0.1:5000/api/all_album"
    responses2= requests.get(url2)
    response2=responses2.json()
    albums=response2['albums']
    url1=f"http://127.0.0.1:5000/api/all_playlist/{id}"
    responses1= requests.get(url1)
    response1=responses1.json()
    playlists=response1['playlists']
    enable_feature = request.args.get('enable_feature')
    playlist_id=request.args.get('playlist_id')
    if str(enable_feature).lower() == 'true':
         
         url2=f"http://127.0.0.1:5000/api/delete_playlist/{int(playlist_id)}"
         response2= requests.delete(url2)
         response=response2.json()
         flash(response['message'],response['status'])
         return(redirect(url_for('user_dashboard')))
        
    return render_template("base.html",songs=songs,genres=genres,playlists=playlists ,albums=albums)
  
  
#----------------------------------------------------------------- Creators Controllers -----------------------------------------------------------------

@app.route('/creator_dashboard', methods=['GET','POST','DELETE'])
@login_required
def creator_dashboard():
    if request.method=="GET":
        if  current_user.is_blacklist==False:
            if current_user.iscreator==True: 
                id = current_user.id
                ar= average_rating_creator(id)
                url=f'http://127.0.0.1:5000/api/creator_song/{id}'
                url1=f'http://127.0.0.1:5000/api/all_album/{id}'
                responses=requests.get(url)
                responses1=requests.get(url1)
                response = responses.json()
                response1=responses1.json()
                albums=response1['albums']
                total_albums = response1['total_albums']
                songs= response['songs']
                total_songs = response['total_songs']
                delete_album = request.args.get('delete_album')
                album_id=request.args.get('album_id')
                if str(delete_album).lower() == 'true':
            
                    url2=f"http://127.0.0.1:5000/api/delete_album/{int(album_id)}"
                    response2= requests.delete(url2)
                    response=response2.json()
                    flash(response['message'],response['status'])
                    return(redirect(url_for('creator_dashboard')))
                
                return render_template("creator.html",songs=songs,albums=albums,total_albums=total_albums,total_songs=total_songs , ar=ar)
            else: 
                return render_template("creator_registration.html")
        else:
            return render_template("creator_registration.html" , blacklisted='blacklisted')
        
    if request.method=="POST":
        creator=request_creator_role()
        if creator==True:
            flash("You have register as creator","success")
            return redirect('/creator_dashboard')
        

def request_creator_role():
    if current_user.iscreator == False:
        current_user.iscreator = True
        db.session.commit()
        return True  
    return False
    
@app.route('/upload_song', methods=['GET','POST'])
@login_required
def upload_song():
    if current_user.iscreator == True:
        form = Upload_Song()
        if request.method=="GET":
         return render_template("song.html", form=form)
        if request.method=="POST" and form.validate_on_submit() :
            creator=User.query.filter_by(id=current_user.id).first()
            # creator_name = creator.name
            song_file =form.song_file.data
            song_pic=form.song_pic.data
            song_file.save('static/songs/'+song_file.filename)
            file_path=str('./static/songs/'+song_file.filename)
            song_pic.save('static/song_pic/'+song_pic.filename)
            file=str('./static/song_pic/'+song_pic.filename)
            form_data={
            'Song_Title':form.song_title.data,
            'Release_Date':form.release_date.data,
            'Created_by':creator.name,
            'Genre':form.genre.data,
            'Language':form.language.data,
            'Lyrics' : form.lyrics.data,
            'Song_pic':file,
            'Song_url':file_path,
            'Creator_id':current_user.id
            }
            responses= requests.post('http://127.0.0.1:5000/api/create' , json=form_data)
            
            response=responses.json()
            

            flash(response['message'], response['status'])
            return redirect("/creator_dashboard")
        else:
            return render_template("song.html", form=form)
    
    return "You are not allowed"
@app.route('/update_song/<int:Id>' ,methods=['GET','POST' , 'PUT'])
@login_required
def update_song(Id):
    form=Upload_Song(submit_field="Update Song")
    url=f'http://127.0.0.1:5000/api/songs/{Id}'
    responses=requests.get(url)
    response=responses.json()
    update_song=response['songs']
    if request.method=="POST" and form.validate_on_submit:
            form_data={
            'Song_Title':form.song_title.data,
            'Release_Date':form.release_date.data,
            'Genre':form.genre.data,
            'Language':form.language.data,
            'Lyrics' : form.lyrics.data,
            }
            responses= requests.put(f'http://127.0.0.1:5000/api/update_song/{Id}' , json=form_data)
            response=responses.json()
            flash(response['message'], response['status'])
            return redirect('/creator_dashboard')
    return render_template('update_song.html',update_song=update_song, form=form)
   
@app.route('/song_details/<int:Id>', methods=['GET','POST'])
@login_required
def song_details(Id):
    song = Songs.query.get(Id)
    rating = SongRatings.query.filter_by(song_id=Id, user_id=current_user.id).first()
    if request.method == 'POST':
        new_rating = int(request.form['rating'])
        
        if rating:
            rating.ratings = new_rating
        else:
            rating = SongRatings(song_id=Id, user_id=current_user.id, ratings=new_rating)
            db.session.add(rating)
        db.session.commit()
    ar = average_rating(Id)
    print(ar)

    return render_template('song_details.html', song=song, rate=rating.ratings if rating else None , average_rating=ar)

@app.route('/playlist',methods=['GET','POST'])
@login_required
def playlist():
    if request.method=="GET":
        url="http://127.0.0.1:5000/api/all_songs"
        response = requests.get(url)
        data = response.json()
        songs= data['songs']
        return render_template('playlist.html' , songs=songs , title='Create Playlist')
    playlist_name=request.form['playlistName']
    selected_songs = request.form.getlist("songs")    
    if selected_songs !=[]:
        data = {
            'Playlist_name': playlist_name , 
            'Selected_songs': selected_songs,
            'User_id': current_user.id
        }
        responses= requests.post("http://127.0.0.1:5000/api/playlist/create" , json=data)    
        response=responses.json()
        flash(response['message'], response['status'])
        return redirect(url_for("user_dashboard"))
    
    flash('Cannot Create Empty Playlist','danger')
    return redirect('/playlist')

@app.route("/playlist_details/<int:id>")
@login_required
def playlist_details(id):
    url=f'http://127.0.0.1:5000/api/song_in_playlist/{id}'
    responses = requests.get(url)
    response = responses.json()
    songs = response['songs']
    
    return render_template('playlist_details.html',songs=songs,id=id)


@app.route('/album',methods=['GET','POST'])
@login_required
def album():
    if request.method=="GET":
        id = current_user.id
        url=f'http://127.0.0.1:5000/api/available_song/{id}'
        responses=requests.get(url)
        response = responses.json()
        songs= response['songs']
        
        return render_template('playlist.html' , songs=songs)
    album_name=request.form['AlbumName']
    selected_songs = request.form.getlist("songs")   
    if selected_songs!=[]: 
        data = {
            'Album_name': album_name , 
            'Selected_songs': selected_songs,
            'User_id': current_user.id
        }
        responses= requests.post("http://127.0.0.1:5000/api/album/create" , json=data)    
        response=responses.json()
        print(response)
        flash(response['message'], response['status'])
        return redirect('/creator_dashboard')
    
    flash('Cannot Create Empty Album','danger')
    return redirect('/album')


@app.route("/album_details/<int:id>")
@login_required 
def album_details(id):
    url=f'http://127.0.0.1:5000/api/song_in_album/{id}'
    responses = requests.get(url)
    response = responses.json()
    songs = response['songs']
    return render_template('album_details.html',songs=songs,id=id)    

@app.route("/edit_playlist/<int:id>" , methods=['GET','POST','PUT'])
@login_required   
def edit_playlist(id):
    play = Playlist.query.filter_by(playlist_id=id).first()
    if request.method=='GET':
        url="http://127.0.0.1:5000/api/all_songs"
        responses = requests.get(url)
        response = responses.json()
        songs = response['songs']
        #play = Playlist.query.filter_by(playlist_id=id).first()
        playlist_name=play.playlist_name.split('_')[0]
        playlist = SongInPlaylist.query.filter_by(playlist_id=id).all()
        songs_ids = [entry.song_id for entry in playlist]
        return render_template('edit_playlist.html' ,songs=songs , songs_ids=songs_ids ,playlist_name=playlist_name,id=id)
    playlist_name=request.form['playlistName']
    selected_songs = request.form.getlist("songs") 
    if playlist_name != play.playlist_name.split('_')[0]:
        unique_playlist_name = f'{playlist_name}_{current_user.id}'
        if not Playlist.query.filter_by(created_by=current_user.id, playlist_name =unique_playlist_name).first():
            play.playlist_name=unique_playlist_name
            db.session.commit()               
    song_in_playlist = SongInPlaylist.query.filter_by(playlist_id=id).all()
    for song in song_in_playlist:
        db.session.delete(song)
        db.session.commit()
    for songs in selected_songs:
        s = SongInPlaylist(playlist_id=id , song_id=songs)
        db.session.add(s)
    db.session.commit()

    flash('Playlist Updated','success')
    return redirect(url_for('user_dashboard'))

@app.route("/edit_album/<int:id>" , methods=['GET','POST','PUT'])
@login_required   
def edit_album(id):
    album = Album.query.filter_by(album_id=id).first()
    if request.method=='GET':
        url=f'http://127.0.0.1:5000/api/available_song/{current_user.id}'
        responses = requests.get(url)
        response = responses.json()
        songs = response['songs']
        url1=f'http://127.0.0.1:5000/api/song_in_album/{id}'
        responses1 = requests.get(url1)
        response1 = responses1.json()
        songs1 = response1['songs']
        album_name=album.album_name.split('_')[0]
        albums = SongInAlbum.query.filter_by(album_id=id).all()
        songs_ids = [entry.song_id for entry in albums]
        return render_template('edit_album.html' ,songs=songs , songs_ids=songs_ids ,album_name=album_name,id=id , songs1=songs1)
    album_name=request.form['Album Name']
    selected_songs = request.form.getlist("songs") 
    print(selected_songs)
    if album_name != album.album_name.split('_')[0]:
        unique_album_name = f'{album_name}_{current_user.id}'
        if not Album.query.filter_by(created_by=current_user.id, album_name =unique_album_name).first():
            album.album_name=unique_album_name
            db.session.commit()         
        else:
            flash("Album Name Already Exists" ,"danger")      
    song_in_album = SongInAlbum.query.filter_by(album_id=id).all()
    for song in song_in_album:
        db.session.delete(song)
        db.session.commit()
    for songs in selected_songs:
        s = SongInAlbum(album_id=id , song_id=songs)
        db.session.add(s)
    db.session.commit()
    flash('Album Updated','success')
    return redirect(url_for('creator_dashboard'))

@app.route("/search" , methods=['GET', 'POST'])
def search():
    song_id=request.args.get('song_id')
    song_feature=request.args.get('song')
    album_id=request.args.get('album_id')
    album_feature=request.args.get('album_feature')
    print(song_id ,song_feature , album_id,album_feature)
    if request.method=='POST':
        q=request.form.get('q')
        query = "%"+q+"%"
        songs = Songs.query.filter(Songs.song_title.like(query)).all()
        albums= Album.query.filter(Album.album_name.like(query)).all()
        songs_genre = Songs.query.filter(Songs.genre.like(query)).all()
        creator = User.query.filter(User.name.like(query)).all()
        songs_creator={}
        albums_creator ={}
        if creator:
            for create in creator:
                if create.songs!=[]:
                    songs_creator[create.name]=create.songs 
                if create.user_album!=[]:
                    albums_creator[create.name]=create.user_album    
        print(albums_creator)
        return render_template("search.html" , q=q , songs=songs , albums=albums , albums_creator=albums_creator,songs_genre=songs_genre , songs_creator=songs_creator  ,visible='search_query' )
       
    if str(song_feature).lower()=='true':
        url = f'http://127.0.0.1:5000/api/songs/{song_id}'
        responses=requests.get(url)
        response=responses.json()
        songs=response['songs']
        return render_template("search.html",songs=songs, visible='song')
    
    if str(album_feature).lower()=='true':
        url = f'http://127.0.0.1:5000/api/album/{album_id}'
        responses=requests.get(url)
        response=responses.json()
        albums=response['albums']
        items = list(albums.values())
        album_name=items[0]['album_name']
        album_id =items[0]['album_id']
        print(album_id)
        url1=f'http://127.0.0.1:5000/api/song_in_album/{album_id}'
        responses1 = requests.get(url1)
        response1 = responses1.json()
        songs = response1['songs']
        return render_template("search.html",album_name =album_name , album_id = album_id ,songs=songs, visible='album')
    return "hello"


#-------------------------------------------------------------------- Functions ------------------------------------------------------------------------

def blacklist(id):
    user = User.query.filter_by(id=id).first()
    if user.is_blacklist == 0:
        user.is_blacklist=1
        db.session.commit()
        
        songs = Songs.query.filter_by(creator_id=id).all()
        for song in songs:
            song.is_flag=1
            db.session.commit()
            
        albums = Album.query.filter_by(created_by=id).all()
        for album in albums:
            album.is_flag=1
            db.session.commit()
    else:
        user.is_blacklist=0
        db.session.commit()
        
        songs = Songs.query.filter_by(creator_id=id).all()
        for song in songs:
            song.is_flag=0
            db.session.commit()
            
        albums = Album.query.filter_by(created_by=id).all()
        for album in albums:
            album.is_flag=0
            db.session.commit()
            
def average_rating(id):
    ratings = SongRatings.query.filter_by(song_id=id).all()
    rate=0
    i=0
    for rating in ratings :
        rate+=rating.ratings 
        i+=1
    if rate!=0 and i!=0:
        average_rating = rate/i
    else:
        average_rating ='No rating is made yet' 
    return average_rating
    
def average_rating_creator(id):
    songs = Songs.query.filter_by(creator_id=id).all()
    average_rating = 0
    total_ratings = 0

    for song in songs:
        ratings = SongRatings.query.filter_by(song_id=song.id).all()
        
        if ratings:
            total_ratings += len(ratings)
            average_rating += sum(rating.ratings for rating in ratings)

    if total_ratings > 0:
        average_rating /= total_ratings
        average_rating=round(average_rating,2)
    else:
        average_rating = 'No ratings yet'

            
    return average_rating
    
def graphs():
    
    songs = Songs.query.all()
    songs_rating={}
    
    for song in songs:
        ratings = average_rating(song.id)
        print(ratings)
        if type(ratings)==float: 
            songs_rating[song.song_title]=ratings
        else:
            songs_rating[song.song_title]=0
            
    song_names = list(songs_rating.keys())
    ratings = list(songs_rating.values())
    print(song_names , ratings)
    
    plt.bar(song_names, ratings, color='blue')
    plt.xlabel('Song Names')
    plt.ylabel('Ratings')
    plt.title('Song Ratings')
    save_directory = './static/graph'
    save_path = os.path.join(save_directory, 'my_plot1.png')
    plt.savefig(save_path)
    plt.close()
    
    
def graph2():
    
    songs = Songs.query.all()
    song_ratings_genre={}
    for song in songs:
        ratings = average_rating(song.id)
        if type(ratings)==float: 
            genre = song.genre    
            if genre in song_ratings_genre.keys():
                avg_rating_genre +=ratings
                count+=1
            else:
                avg_rating_genre=ratings
                count=1
            song_ratings_genre[genre]=avg_rating_genre/count
        else:
            pass

    genre_name= list(song_ratings_genre.keys())
    genre_ratings =list(song_ratings_genre.values())
    print(genre_ratings , genre_name)
    plt.xlabel('Genre Names')
    plt.ylabel('Ratings')
    plt.title('Song Ratings Vs Genre')
    plt.bar(genre_name, genre_ratings , color='orange' )
    
    save_directory = './static/graph'
    save_path = os.path.join(save_directory, 'my_plot2.png')
    plt.savefig(save_path)      
    plt.close()
        

    