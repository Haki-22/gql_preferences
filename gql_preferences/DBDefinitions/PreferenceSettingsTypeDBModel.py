import sqlalchemy
from sqlalchemy import Column, String, DateTime, JSON, Uuid, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .Base import BaseModel
from. uuid import UUIDFKey, UUIDColumn
from uuid import UUID

# Define a SQLAlchemy model for the 'preference_settings' table
class PreferenceSettingsTypeModel(BaseModel):
    # Table name
    __tablename__ = "preference_settings_types"

    # Unique identifier for preference settings
    id = UUIDColumn()

    # Name for the type of preferences
    name = Column(String, comment="Name for the set of preferences (name:jazyk, name:barevny motiv)")

    # Name in english for the type of preferences
    name_en =Column(String, comment="English name for the set of preferences (name_en:language, name_en:theme)")

    # Timestamp for when the preference type was created
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp for when the preference type was created")
    
    # Timestamp for the last change to the preference type
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), onupdate=sqlalchemy.sql.func.now(), comment="Timestamp for the last change to the preference type")

    # Foreign key relationship to the user who created the type of preferences
    createdby = UUIDFKey(comment="Foreign key to the user who created the preference type")

    # Foreign key relationship to the user who changed the type of preferences
    changedby = UUIDFKey(comment="Foreign key to the user who has changed this preference type")

    #default_preference_settings = Column(Uuid, comment="Default preference settings ID")

    #order (Preference Settings Type)
    order = Column(Integer, comment="order")

    preference_settings = relationship("PreferenceSettingsModel", back_populates="type", uselist=True)

