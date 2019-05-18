import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    username = Column(String(80), nullable=False)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    password_hash = Column(String(80), nullable=False)
    online = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Messages(Base):
    __tablename__ = 'messages'

    message = Column(String(500), nullable=False)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)

#     @property
#     def serialize(self):
#         return {
#             'name': self.name,
#             'id': self.id
#         }


# class Novels(Base):
#     __tablename__ = 'novels'

#     name = Column(String(80), nullable=False)
#     id = Column(Integer, primary_key=True)
#     year = Column(Integer)
#     description = Column(String(250))
#     lastAdded = Column(DateTime)
#     author_id = Column(Integer, ForeignKey('authors.id'))
#     author = relationship(Authors, backref='novels')
#     user_id = Column(Integer, ForeignKey('users.id'))
#     user = relationship(Users)

#     @property
#     def serialize1(self):
#         return {
#             'name': self.name,
#             'id': self.id,
#             'author_id': self.author_id,
#             'year': self.year,
#             'description': self.description
#         }


engine = create_engine('sqlite:///users.db')

Base.metadata.create_all(engine)
