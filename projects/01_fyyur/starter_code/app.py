#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from os import name
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler, error
from flask_wtf import Form
from sqlalchemy.orm import backref
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120)) 
    shows = db.relationship('Show', backref='venue', lazy='joined', cascade="all, delete")

  
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy='joined', cascade="all, delete")

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
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
  data = []
  venues = Venue.query.all()
  places = Venue.query.distinct(Venue.city, Venue.state).all()

  for place in places:
    tmp_venues = []
    for venue in venues:
        if venue.city == place.city and venue.state == place.state:
            tmp_venues.append({
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': len([show for show in venue.shows if show.start_time > datetime.now()])
                })
    
    data.append({
        'city': place.city,
        'state': place.state,
        'venues': tmp_venues
        })
  
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  results = Venue.query.filter(Venue.name.ilike("%" + search_term + "%")).all()
  
  response={
    "count": len(results),
    "data": []
  }

  for result in results:
    response["data"].append({
      'id': result.id,
      'name': result.name
    })

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  venue = db.session.query(Venue).filter(Venue.id == venue_id).one()
  shows = db.session.query(Show).filter(Show.venue_id == venue_id)
  past_shows = []
  upcoming_shows = []

  for show in shows:
    artist = db.session.query(Artist.name, Artist.image_link).filter(Artist.id == show.artist_id).one()
    show_add = {
      "artist_id": show.artist_id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(show.start_time)
    }
    if (show.start_time < datetime.now()):
      past_shows.append(show_add)
    else:
      upcoming_shows.append(show_add)

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(csrf_enabled=False)
  if form.validate():
    try:
      venue = Venue(
        name=form.name.data, 
        city=form.city.data,
        state=form.state.data, 
        address=form.address.data, 
        phone=form.phone.data, 
        image_link=form.image_link.data, 
        genres=form.genres.data, 
        facebook_link=form.facebook_link.data, 
        website_link=form.website_link.data, 
        seeking_talent=form.seeking_talent.data, 
        seeking_description=form.seeking_description.data)

      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + form.name.data + ' was successfully listed!')
    except ValueError as e:
      print(e)
      db.session.rollback()
      error = True
      flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|'.join(err))
      flash('Errors ' + str(message))

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    db.sesssion.delete(venue)
    db.session.commit()
    flash('The Venue has been successfully deleted!')
    return render_template('pages/home.html')
  except:
    db.session.rollback()
    flash('Delete was unsuccessful. Try again!')
  finally:
    db.session.close()
  return None



  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  results = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()

  response = {
      "count": len(results),
      "data": []
    }
  for result in results:
    response["data"].append({
        "id": result.id,
        "name": result.name
      })

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = db.session.query(Artist).filter(Artist.id == artist_id).one()
  shows = db.session.query(Show).filter(Show.artist_id == artist_id)
  past_shows = []
  upcoming_shows = []

  for show in shows:
    venue = db.session.query(Venue.name, Venue.image_link).filter(Venue.id == show.venue_id).one()
    show_add = {
      "venue_id": show.venue_id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": str(show.start_time)
    }
    if (show.start_time < datetime.now()):
      past_shows.append(show_add)
    else:
      upcoming_shows.append(show_add) 
  
  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist= Artist.query.get_or_404(artist_id)
  form = ArtistForm(obj=artist) 
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  artist = Artist.query.get_or_404(artist_id)
  form = ArtistForm(request.form)
  error = False

  try:
    artist = Artist(
    name = form.name.data,
    genres = form.genres.data,
    city = form.city.data,
    state = form.state.data,
    phone = form.phone.data,
    website_link = form.website_link.data,
    facebook_link = form.facebook_link.data,
    seeking_venue = form.seeking_venue.data,
    seeking_description = form.seeking_description.data,
    image_link = form.image_link.data
    )
    db.session.add(artist)
    db.session.commit()

  except ValueError as e:
    print(e)
    db.session.rollback()
    error = True
 
  finally:
    db.session.close()

  if error:
    flash('Error when trying to update ' + request.form['name'] + '. Update unsuccessful.')

  else:
    flash('Artist ' + request.form['name'] + ' was successfully updated!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm(obj=venue)

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

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm(request.form)
  error = False
  
  try:
    venue = Venue(
      name = form.name.data,
      genres = form.genres.data,
      address = form.address.data,
      city = form.city.data,
      state = form.city.data,
      phone = form.phone.data,
      website_link = form.website_link.data,
      facebook_link = form.facebook_link.data,
      seeking_talent = form.seeking_talent.data,
      seeking_description = form.seeking_description.data,
      image_link = form.image_link.data
    )
    db.session.add(venue)
    db.session.commit()

  except ValueError as e:
    print(e)
    db.session.rollback()
    error = True
 
  finally:
    db.session.close()

  if error:
    flash('Error when trying to update ' + request.form['name'] + '. Update unsuccessful.')

  else:
    flash('Venue ' + request.form['name'] + ' was successfully updated!')


  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(csrf_enabled=False)
  if form.validate():
    try:
      artist = Artist(
        name=form.name.data, 
        city=form.city.data,
        state=form.state.data, 
        phone=form.phone.data, 
        image_link=form.image_link.data, 
        genres=form.genres.data, 
        facebook_link=form.facebook_link.data, 
        website_link=form.website_link.data, 
        seeking_venue=form.seeking_venue.data, 
        seeking_description=form.seeking_description.data)

      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + form.name.data + ' was successfully listed!')
    except ValueError as e:
      print(e)
      db.session.rollback()
      error = True
      flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|'.join(err))
      flash('Errors ' + str(message))

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():

  data = []

  shows = Show.query.order_by(Show.start_time.desc()).all()

  for show in shows:
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(csrf_enabled=False)
  if form.validate():
    try:
      show = Show(
        artist_id = form.artist_id.data,
        venue_id = form.venue_id.data,
        start_time = form.start_time.data)

      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')

    except ValueError as e:
      print(e)
      db.session.rollback()
      error = True
      flash('An error occurred. Show' + form.name.data + ' could not be listed.')
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|'.join(err))
      flash('Errors ' + str(message))

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
