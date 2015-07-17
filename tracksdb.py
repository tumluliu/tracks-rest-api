"""
ORM definitions for mapping tracks data stored in PostgreSQL database
"""

from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.dialects.postgresql import INTERVAL, TIMESTAMP
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_AsGeoJSON as st_asgeojson
from settings import PG_DB_CONF
import json
import logging

logger = logging.getLogger(__name__)

engine = create_engine(URL(**PG_DB_CONF))
Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker(engine))

class Track(Base):
    __tablename__ = 'tracks'
    ogc_fid       = Column(Integer, primary_key=True)
    name          = Column(String)
    cmt           = Column(String)
    desc          = Column(String)
    src           = Column(String)
    number        = Column(Integer)
    wkb_geometry  = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326))


class TrackInfo(Base):
    __tablename__ = 'trackinfo'
    ogc_fid       = Column(Integer, primary_key=True)
    segments      = Column(Integer)
    length_2d     = Column(Float)
    length_3d     = Column(Float)
    moving_time   = Column(INTERVAL)
    stopped_time  = Column(INTERVAL)
    max_speed     = Column(Float)
    uphill        = Column(Float)
    downhill      = Column(Float)
    started       = Column(TIMESTAMP)
    ended         = Column(TIMESTAMP)
    points        = Column(Integer)
    start_lon     = Column(Float)
    start_lat     = Column(Float)
    end_lon       = Column(Float)
    end_lat       = Column(Float)
    start_geom    = Column(Geometry(geometry_type='POINT', srid=4326))
    end_geom      = Column(Geometry(geometry_type='POINT', srid=4326))

def track_serializer(instance):
    track_dict = {}
    track_dict['ID']          = instance.ogc_fid
    track_dict['Name']        = instance.name
    track_dict['CMT']         = instance.cmt
    track_dict['Description'] = instance.desc
    track_dict['Source']      = instance.src
    track_dict['Number']      = instance.number
    track_dict['GeoJSON']     = json.loads(
        Session.scalar(st_asgeojson(instance.wkb_geometry)))
    logger.debug("Serialized track: %s", track_dict)
    return track_dict

def trackinfo_serializer(instance):
    ti_dict = {}
    ti_dict['ID']                  = instance.ogc_fid
    ti_dict['Segments']            = instance.segments
    ti_dict['2D length']           = instance.length_2d
    ti_dict['3D length']           = instance.length_3d
    ti_dict['Moving time']         = str(instance.moving_time)
    ti_dict['Stopped time']        = str(instance.stopped_time)
    ti_dict['Max speed']           = instance.max_speed
    ti_dict['Uphill distance']     = instance.uphill
    ti_dict['Downhill distance']   = instance.downhill
    ti_dict['Started time']        = str(instance.started)
    ti_dict['Ended time']          = str(instance.ended)
    ti_dict['Points']              = instance.points
    ti_dict['Started longitude']   = instance.start_lon
    ti_dict['Started latitute']    = instance.start_lat
    ti_dict['Ended longitude']     = instance.end_lon
    ti_dict['Ended latitude']      = instance.end_lat
    ti_dict['Start point GeoJSON'] = json.loads(
        Session.scalar(st_asgeojson(instance.start_geom)))
    ti_dict['End point GeoJSON']   = json.loads(
        Session.scalar(st_asgeojson(instance.end_geom)))
    logger.debug("Serialized trackinfo: %s", ti_dict)
    return ti_dict
