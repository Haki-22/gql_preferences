import sqlalchemy
from sqlalchemy import Column, String, DateTime, ForeignKey
from .Base import BaseModel
from. uuid import UUIDFKey, UUIDColumn

# Define a SQLAlchemy model for the 'preferedtags' table
class PreferenceTagModel(BaseModel):
    # Table name
    __tablename__ = "preferedtags"
    
    # Unique identifier for the tag
    id = UUIDColumn()

    # Foreign key relationship to the author/user who created the tag
    author_id = UUIDFKey( comment="Foreign key to the author/user who created the tag")

    # Name of the tag
    name = Column(String, comment="Name of the tag")
    
    # Name in english for the tag      
    name_en =Column(String, comment="English name for the preference settings (name_en:czech, name_en:Light)")

    # Timestamp for when the tag was created
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp for when the tag was created")

    # Timestamp for the last change to the tag
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp for the last change to the tag")
    
    # Foreign key relationship to the user who created the tag
    createdby = UUIDFKey( comment="Foreign key to the user who created the tag")

    # Foreign key relationship to the user who last changed the tag
    changedby = UUIDFKey( comment="Foreign key to the user who last changed the tag")

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")
