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
    track_dict['ogc_fid']      = instance.ogc_fid
    track_dict['name']         = instance.name
    track_dict['cmt']          = instance.cmt
    track_dict['desc']         = instance.desc
    track_dict['src']          = instance.src
    track_dict['number']       = instance.number
    track_dict['geom'] = json.loads(
        Session.scalar(st_asgeojson(instance.wkb_geometry)))
    logger.debug("Serialized track: %s", track_dict)
    return track_dict

def trackinfo_serializer(instance):
    ti_dict = {}
    ti_dict['ogc_fid']       = instance.ogc_fid
    ti_dict['segments']      = instance.segments
    ti_dict['length_2d']     = instance.length_2d
    ti_dict['length_3d']     = instance.length_3d
    ti_dict['moving_time']   = str(instance.moving_time)
    ti_dict['stopped_time']  = str(instance.stopped_time)
    ti_dict['max_speed']     = instance.max_speed
    ti_dict['uphill']        = instance.uphill
    ti_dict['downhill']      = instance.downhill
    ti_dict['started']       = str(instance.started)
    ti_dict['ended']         = str(instance.ended)
    ti_dict['points']        = instance.points
    ti_dict['start_lon']     = instance.start_lon
    ti_dict['start_lat']     = instance.start_lat
    ti_dict['end_lon']       = instance.end_lon
    ti_dict['end_lat']       = instance.end_lat
    ti_dict['start_geom']    = json.loads(
        Session.scalar(st_asgeojson(instance.start_geom)))
    ti_dict['end_geom']      = json.loads(
        Session.scalar(st_asgeojson(instance.end_geom)))
    logger.debug("Serialized trackinfo: %s", ti_dict)
    return ti_dict
