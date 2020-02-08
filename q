warning: LF will be replaced by CRLF in app.py.
The file will have its original line endings in your working directory
warning: LF will be replaced by CRLF in forms.py.
The file will have its original line endings in your working directory
warning: LF will be replaced by CRLF in templates/forms/new_artist.html.
The file will have its original line endings in your working directory
warning: LF will be replaced by CRLF in templates/forms/new_venue.html.
The file will have its original line endings in your working directory
[1mdiff --git a/__pycache__/app.cpython-38.pyc b/__pycache__/app.cpython-38.pyc[m
[1mindex 471ba43..bc74b80 100644[m
Binary files a/__pycache__/app.cpython-38.pyc and b/__pycache__/app.cpython-38.pyc differ
[1mdiff --git a/__pycache__/forms.cpython-38.pyc b/__pycache__/forms.cpython-38.pyc[m
[1mindex 4cb2d5d..1702339 100644[m
Binary files a/__pycache__/forms.cpython-38.pyc and b/__pycache__/forms.cpython-38.pyc differ
[1mdiff --git a/app.py b/app.py[m
[1mindex d5d183d..4385f51 100644[m
[1m--- a/app.py[m
[1m+++ b/app.py[m
[36m@@ -66,17 +66,20 @@[m [mclass Venue(db.Model):[m
 [m
 class Artist(db.Model):[m
     __tablename__ = 'Artist'[m
[31m-[m
[32m+[m[41m    [m
     id = db.Column(db.Integer, primary_key=True)[m
     name = db.Column(db.String)[m
[32m+[m[32m    genres = db.Column(db.ARRAY(db.String(120)))[m
     city = db.Column(db.String(120))[m
     state = db.Column(db.String(120))[m
     phone = db.Column(db.String(120))[m
[31m-    #genres = db.Column(db.String(120))[m
[31m-    genres = db.Column(db.ARRAY(db.String(120)))[m
[31m-    image_link = db.Column(db.String(500))[m
[31m-    facebook_link = db.Column(db.String(120))[m
[32m+[m[32m    website = db.Column(db.String(500))[m
[32m+[m[32m    facebook_link = db.Column(db.String(120))[m[41m  [m
[32m+[m[32m    seeking_venue = db.Column(db.Boolean, default=False)[m
[32m+[m[32m    seeking_description = db.Column(db.String(500), default='')[m
     venues = db.relationship('Show', back_populates='artist')[m
[32m+[m[32m    image_link = db.Column(db.String(500))[m
[32m+[m[41m    [m
     def details(self):[m
       return{[m
         'id': self.id,[m
[36m@@ -85,10 +88,10 @@[m [mclass Artist(db.Model):[m
         'city': self.city,[m
         'state': self.state,[m
         'phone': self.phone,[m
[31m-        #'website': self.website,[m
[32m+[m[32m        'website': self.website,[m
         'facebook_link': self.facebook_link,[m
[31m-        #'seeking_venue': self.seeking_venue,[m
[31m-        #'seeking_description': self.seeking_description,[m
[32m+[m[32m        'seeking_venue': self.seeking_venue,[m
[32m+[m[32m        'seeking_description': self.seeking_description,[m
         'image_link': self.image_link[m
       }[m
 [m
[36m@@ -229,7 +232,8 @@[m [mdef create_venue_submission():[m
     # TODO: insert form data as a new Venue record in the db, instead[m
     # TODO: modify data to be the data object returned from db insertion[m
   form = VenueForm(request.form)[m
[31m-  #flash(form.errors)[m
[32m+[m[32m  flash(form.errors)[m
[32m+[m[32m  flash(request.form['seeking_talent'])[m
   if request.method == "POST" and form.validate():[m
     try: [m
       new_venue = Venue([m
[36m@@ -238,11 +242,12 @@[m [mdef create_venue_submission():[m
                 city=request.form['city'],[m
                 state=request.form['state'],[m
                 phone=request.form['phone'],[m
[31m-                image_link='',[m
[32m+[m[32m                image_link=request.form['image_link'],[m
                 facebook_link=request.form['facebook_link'],[m
[31m-                description='',[m
[32m+[m[32m                description=request.form['seeking_description'],[m
[32m+[m[32m                #TODO: To chnage it later to the real value[m
                 seeking_talent=False,[m
[31m-                website='',[m
[32m+[m[32m                website=request.form['website'],[m
                 genres=request.form.getlist('genres'),             [m
             )[m
       #Venue.insert(new_venue)[m
[36m@@ -398,16 +403,19 @@[m [mdef create_artist_submission():[m
   form = ArtistForm(request.form)[m
   #flash(form.errors)[m
   if form.validate():[m
[31m-    try: [m
[32m+[m[32m    try:[m[41m      [m
       new_artist = Artist([m
                 name=request.form['name'],[m
[31m-                #address=request.form['address'],[m
                 city=request.form['city'],[m
                 state=request.form['state'],[m
                 phone=request.form['phone'],[m
                 genres=request.form.getlist('genres'),     [m
[31m-                image_link='',[m
[32m+[m[32m                image_link=request.form['image_link'],[m
[32m+[m[32m                #TODO: To chnage it later to the real value[m
[32m+[m[32m                seeking_venue=False,[m
[32m+[m[32m                seeking_description=request.form['seeking_description'],[m
                 facebook_link=request.form['facebook_link'],[m
[32m+[m[32m                website=request.form['website'],[m
             )[m
       db.session.add(new_artist)[m
       db.session.commit()[m
[1mdiff --git a/forms.py b/forms.py[m
[1mindex f3a54ad..122371f 100644[m
[1m--- a/forms.py[m
[1m+++ b/forms.py[m
[36m@@ -85,9 +85,6 @@[m [mclass VenueForm(Form):[m
     phone = StringField([m
         'phone'[m
     )[m
[31m-    image_link = StringField([m
[31m-        'image_link'[m
[31m-    )[m
     genres = SelectMultipleField([m
         # TODO implement enum restriction[m
         'genres', validators=[DataRequired()],[m
[36m@@ -116,6 +113,18 @@[m [mclass VenueForm(Form):[m
     facebook_link = StringField([m
         'facebook_link', validators=[URL()][m
     )[m
[32m+[m[32m    website = StringField([m
[32m+[m[32m        'website', validators=[URL()][m
[32m+[m[32m    )[m
[32m+[m[32m    seeking_talent = StringField([m
[32m+[m[32m        'seeking_talent'[m
[32m+[m[32m    )[m
[32m+[m[32m    seeking_description = StringField([m
[32m+[m[32m        'seeking_description'[m
[32m+[m[32m    )[m
[32m+[m[32m    image_link = StringField([m
[32m+[m[32m        'image_link', validators=[URL()][m
[32m+[m[32m    )[m
 [m
 class ArtistForm(Form):[m
     name = StringField([m
[36m@@ -184,9 +193,6 @@[m [mclass ArtistForm(Form):[m
         # TODO implement validation logic for state[m
         'phone'[m
     )[m
[31m-    # image_link = StringField([m
[31m-    #     'image_link'[m
[31m-    # )[m
     genres = SelectMultipleField([m
         # TODO implement enum restriction[m
         'genres', validators=[DataRequired()],[m
[36m@@ -216,5 +222,17 @@[m [mclass ArtistForm(Form):[m
         # TODO implement enum restriction[m
         'facebook_link', validators=[URL()][m
     )[m
[32m+[m[32m    website = StringField([m
[32m+[m[32m        'website', validators=[URL()][m
[32m+[m[32m    )[m
[32m+[m[32m    seeking_venue = StringField([m
[32m+[m[32m        'seeking_talent'[m
[32m+[m[32m    )[m
[32m+[m[32m    seeking_description = StringField([m
[32m+[m[32m        'seeking_description'[m
[32m+[m[32m    )[m
[32m+[m[32m    image_link = StringField([m
[32m+[m[32m        'image_link', validators=[URL()][m
[32m+[m[32m    )[m
 [m
 # TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM[m
[1mdiff --git a/templates/forms/new_artist.html b/templates/forms/new_artist.html[m
[1mindex 250e438..219089f 100644[m
[1m--- a/templates/forms/new_artist.html[m
[1m+++ b/templates/forms/new_artist.html[m
[36m@@ -34,6 +34,27 @@[m
           <label for="genres">Facebook Link</label>[m
           {{ form.facebook_link(class_ = 'form-control', placeholder='http://', id=form.state, autofocus = true) }}[m
         </div>[m
[32m+[m[41m      [m
[32m+[m[32m      <!-- Add website seeking venue desicription and image link -->[m
[32m+[m[32m      <div class="form-group">[m
[32m+[m[32m          <label for="website">Website</label>[m
[32m+[m[32m          {{ form.website(class_ = 'form-control', placeholder='http://', id=form.state, autofocus = true) }}[m
[32m+[m[32m      </div>[m
[32m+[m[32m            <div class="form-group">[m
[32m+[m[32m          <label for="image_link">Image Link</label>[m
[32m+[m[32m          {{ form.image_link(class_ = 'form-control', placeholder='http://', id=form.state, autofocus = true) }}[m
[32m+[m[32m      </div>[m
[32m+[m[32m      <div class="form-group">[m
[32m+[m[32m          <label for="seeking_venue">Seeking Venue</label>[m
[32m+[m[32m          {{ form.seeking_venue(class_ = 'checkbox', type='checkbox',  id=form.state) }}[m
[32m+[m[32m      </div>[m[41m [m
[32m+[m[32m      <div class="form-group">[m
[32m+[m[32m          <label for="seeking_description">Seeking Description</label>[m
[32m+[m[32m          {{ form.seeking_description(class_ = 'form-control', placeholder='seeking description', id=form.state, autofocus = true) }}[m
[32m+[m[32m      </div>[m
[32m+[m
[32m+[m
[32m+[m
       <input type="submit" value="Create Venue" class="btn btn-primary btn-lg btn-block">[m
     </form>[m
   </div>[m
[1mdiff --git a/templates/forms/new_venue.html b/templates/forms/new_venue.html[m
[1mindex f363583..6549460 100644[m
[1m--- a/templates/forms/new_venue.html[m
[1m+++ b/templates/forms/new_venue.html[m
[36m@@ -35,9 +35,26 @@[m
         {{ form.genres(class_ = 'form-control', placeholder='Genres, separated by commas', id=form.state, autofocus = true) }}[m
       </div>[m
       <div class="form-group">[m
[31m-          <label for="genres">Facebook Link</label>[m
[32m+[m[32m          <label for="facebook_link">Facebook Link</label>[m
           {{ form.facebook_link(class_ = 'form-control', placeholder='http://', id=form.state, autofocus = true) }}[m
[31m-        </div>[m
[32m+[m[32m      </div>[m
[32m+[m[32m      <!-- Add website facebook link seeking venue desicription and image link -->[m
[32m+[m[32m      <div class="form-group">[m
[32m+[m[32m          <label for="website">Website</label>[m
[32m+[m[32m          {{ form.website(class_ = 'form-control', placeholder='http://', id=form.state, autofocus = true) }}[m
[32m+[m[32m      </div>[m
[32m+[m[32m      <div class="form-group">[m
[32m+[m[32m          <label for="seeking_talent">Seeking Talent</label>[m
[32m+[m[32m          {{ form.seeking_talent(class_ = 'checkbox', type='checkbox',  id=form.state) }}[m
[32m+[m[32m      </div>[m[41m [m
[32m+[m[32m      <div class="form-group">[m
[32m+[m[32m          <label for="seeking_description">Seeking Description</label>[m
[32m+[m[32m          {{ form.seeking_description(class_ = 'form-control', placeholder='seeking description', id=form.state, autofocus = true) }}[m
[32m+[m[32m      </div>[m
[32m+[m[32m      <div class="form-group">[m
[32m+[m[32m          <label for="image_link">Image Link</label>[m
[32m+[m[32m          {{ form.image_link(class_ = 'form-control', placeholder='http://', id=form.state, autofocus = true) }}[m
[32m+[m[32m      </div>[m
       <input type="submit" value="Create Venue" class="btn btn-primary btn-lg btn-block">[m
     </form>[m
   </div>[m
