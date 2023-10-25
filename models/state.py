#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.city import City
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref='state',
                              cascade='all, delete, delete-orphan')
    else:
        name = ''

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """Returns the list of City with state_id equals
            to the current State.id"""
            from models import storage
            linked_cities = []
            cities = storage.all(City)
            for city in cities.values():
                linked_cities.append(city)
            return linked_cities
