from sqlalchemy import create_engine
from os import getenv
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.exc import InvalidRequestError
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

class DBStorage:
    """
    This class manages database storage for all ORM entities.
    It handles connection setup, session management, object retrieval,
    object saving, and teardown.
    """
    __engine = None
    __session = None

    def __init__(self) -> None:
        """
        Initializes the DBStorage instance by setting up the database engine
        using environment variables and dropping all tables if in testing environment.
        """
        username = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database_name = getenv("HBNB_MYSQL_DB")
        database_url = f"mysql+mysqldb://{username}:{password}@{host}/{database_name}"
        self.__engine = create_engine(database_url, pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries the database and returns a dictionary of all objects.
        If a class is specified, it returns all instances of that class.
        Otherwise, it returns all instances of all classes.
        """
        objs_list = []
        if cls:
            if isinstance(cls, str):
                cls = globals().get(cls, cls) 
            if issubclass(cls, Base):
                objs_list = self.__session.query(cls).all()
        else:
            for subclass in Base.__subclasses__():
                objs_list.extend(self.__session.query(subclass).all())
        obj_dict = {f"{obj.__class__.__name__}.{obj.id}": obj for obj in objs_list}
        return obj_dict

    def new(self, obj):
        """
        Adds a new object to the session (staging it for insertion).
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes to the database (persisting them).
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the session and database if it is not None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Reloads the database schema by first dropping all tables and then
        creating them anew. Also, initializes a new session factory.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)()