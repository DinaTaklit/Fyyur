#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
# Import Migrate 
from flask_migrate import Migrate 
import sys 
from sqlalchemy import func
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    description = db.Column(db.String(500), default='')
    seeking_talent = db.Column(db.Boolean, default=False)
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    artists = db.relationship('Show', back_populates='venue')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    #genres = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    venues = db.relationship('Show', back_populates='artist')
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'),nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'),nullable=False)
  start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
  artist = db.relationship('Artist',back_populates='venues')
  venue = db.relationship('Venue',back_populates='artists') 
  def details(self):
    return{
      'venue_id': self.venue_id,
      'venue_name': self.venue.name,
      'artist_id': self.artist_id,
      'artist_name': self.artist.name,
      'artist_image': self.artist.image_link,
      'start_time': str(self.start_time)
    }
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  #return babel.dates.format_datetime(date, format)
  #to fix the problem AttributeError: 'NoneType' object has no attribute 'days'
  return babel.dates.format_datetime(date, format, locale='en')
app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = db.session.query(Venue.city,Venue.state).group_by(Venue.city,Venue.state).all()
  result = []
  current_time = datetime.utcnow()
  for venue_data in data: 
    city_name = venue_data[0]
    city_state = venue_data[1]
    q = db.session.query(Venue).filter(Venue.city == city_name, Venue.state == city_state)
    group = {
      "city": city_name,
      "state": city_state,
      "venues": []
    }
    venues = q.all()
    for venue in venues: 
      print(venue.id)
      group['venues'].append({
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_show': len(Venue.query.join(Show).filter(venue.id == Show.venue_id,Show.start_time > current_time).all())
      })
      print('num_upcoming_show => {}'.format(len(Venue.query.join(Show).filter(venue.id == Show.venue_id,Show.start_time > current_time).all())))
    result.append(group)     
  return render_template('pages/venues.html', areas=result)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = Venue.query.filter_by(id=venue_id).order_by('id').all()
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)
  #flash(form.errors)
  if request.method == "POST" and form.validate():
    try: 
      new_venue = Venue(
                name=request.form['name'],
                address=request.form['address'],
                city=request.form['city'],
                state=request.form['state'],
                phone=request.form['phone'],
                image_link='',
                facebook_link=request.form['facebook_link'],
                description='',
                seeking_talent=False,
                website='',
                genres=request.form.getlist('genres'),             
            )
      #Venue.insert(new_venue)
      db.session.add(new_venue)
      db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as error:
      # TODO: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      #see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      db.session.rollback()
      flash(error)   
    finally:
      db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Venue with id' + venue_id + ' was successfully deleted!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue with id' + venue_id + ' could not be deleted.')
  finally: 
    db.session.close()
    #return jsonify({ 'success': True })

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data =  Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the atritst page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  data = Artist.query.filter_by(id=artist_id).order_by('id').all()
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  #flash(form.errors)
  if form.validate():
    try: 
      new_artist = Artist(
                name=request.form['name'],
                #address=request.form['address'],
                city=request.form['city'],
                state=request.form['state'],
                phone=request.form['phone'],
                genres=request.form.getlist('genres'),     
                image_link='',
                facebook_link=request.form['facebook_link'],
            )
      db.session.add(new_artist)
      db.session.commit()
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as error:
      # TODO: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Artist ' + request.form['name']  + ' could not be listed.')
      #see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      db.session.rollback()
      flash(error)   
    finally:
      db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.join(Venue).join(Artist).all()
  data = list(map(Show.details, shows))
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  #flash(form.errors)
  if form.validate():
    try: 
      new_show = Show(
                venue_id=request.form['venue_id'],
                artist_id=request.form['artist_id'],
                start_time=request.form['start_time'],          
            )
      #Venue.insert(new_venue)
      db.session.add(new_show)
      db.session.commit()
      # on successful db insert, flash success
      flash('Show was successfully listed!')
    except Exception as error:
      # TODO: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Show could not be listed.')
      #see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      db.session.rollback()
      flash(error)   
    finally:
      db.session.close()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
