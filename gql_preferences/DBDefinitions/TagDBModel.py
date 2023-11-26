import sqlalchemy
from sqlalchemy import Column, String, DateTime, ForeignKey
from uoishelpers.uuid import UUIDColumn
from .Base import BaseModel, UUIDFKey

# Define a SQLAlchemy model for the 'preferedtags' table
class TagModel(BaseModel):
    # Table name
    __tablename__ = "preferedtags"
    
    # Unique identifier for the tag
    id = UUIDColumn(postgres=False)

    # Foreign key relationship to the author/user who created the tag
    author_id = UUIDFKey(nullable=True, comment="Foreign key to the author/user who created the tag")

    # Name of the tag
    name = Column(String, comment="Name of the tag")

    # Timestamp for when the tag was created
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp for when the tag was created")

    # Timestamp for the last change to the tag
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp for the last change to the tag")
    
    # Foreign key relationship to the user who created the tag
    createdby = UUIDFKey(nullable=True, comment="Foreign key to the user who created the tag")

    # Foreign key relationship to the user who last changed the tag
    changedby = UUIDFKey(nullable=True, comment="Foreign key to the user who last changed the tag")
