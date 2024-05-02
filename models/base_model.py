#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String

Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        for key, value in kwargs.items():
            if key in ["created_at", "updated_at"]:
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
            setattr(self, key, value)
        if 'created_at' not in kwargs:
            self.created_at = datetime.utcnow()
        if 'updated_at' not in kwargs:
            self.updated_at = datetime.utcnow()

    def __str__(self):
        """Returns a string representation of the instance"""
        return f"<{type(self).__name__} ({self.id}) {self.__dict__}>"

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the instance."""
        dictionary = {
            '__class__': self.__class__.__name__,
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if hasattr(self, '_sa_instance_state'):
            del dictionary['_sa_instance_state']
        return dictionary

    
    def delete(self):
        """Deletes the instance from storage."""
        from models import storage
        storage.delete(self)