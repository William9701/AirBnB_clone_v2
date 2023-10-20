from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.base_model import Base


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        user = os.environ.get('HBNB_MYSQL_USER', 'default_user')
        password = os.environ.get('HBNB_MYSQL_PWD', 'default_password')
        host = os.environ.get('HBNB_MYSQL_HOST', 'localhost')
        database = os.environ.get('HBNB_MYSQL_DB', 'default_db')
        env = os.environ.get('HBNB_ENV', 'development')

        # Define the MySQL connection URL using the retrieved values
        mysql_url = f"mysql://{user}:{password}@{host}/{database}"

        # Create the SQLAlchemy Engine
        self.__engine = create_engine(mysql_url, pool_pre_ping=True)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

        # Drop tables if environment is "test"
        if env == 'test':
            metadata = MetaData()
            metadata.reflect(bind=self.__engine)

            # Drop each table
            for table in metadata.tables.values():
                table.drop(bind=self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        obj_dict = {}
        classes_to_query = [State, City, User, Place, Review, Amenity]

        if cls is None:
            for class_to_query in classes_to_query:
                objects = self.__session.query(class_to_query).all()
                for obj in objects:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    obj_dict[key] = obj
        else:
            if isinstance(cls, str):
                cls = eval(cls)
            if cls in classes_to_query:
                objects = self.__session.query(cls).all()
                for obj in objects:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)
            self.__session.commit()

    def close(self):
        """Close the current SQLAlchemy Session"""
        self.__session.close()

    def reload(self):
        # Create all tables in the database
        Base.metadata.create_all(self.__engine)

        # Create the current database session with specified options
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
