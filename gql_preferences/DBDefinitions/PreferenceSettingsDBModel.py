import sqlalchemy
from sqlalchemy import Column, String, DateTime, JSON, Uuid, ForeignKey, Integer, Boolean, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .Base import BaseModel
from .uuid import UUIDFKey, UUIDColumn

# Define a SQLAlchemy model for the 'preference_settings' table
class PreferenceSettingsModel(BaseModel):
    # Table name
    __tablename__ = "preference_settings"

    # Unique identifier for preference settings
    id = UUIDColumn()

    # Name for the preference
    name = Column(String, comment="Name for preference settings (name:čeština, name:Světlý)")

    # Name in english for the type of preferences
    name_en =Column(String, comment="English name for the preference settings (name_en:czech, name_en:Light)")

    # Timestamp for when the preference was created
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp for when the preference settings was created")
    
    # Timestamp for the last change to the preference
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), onupdate=sqlalchemy.sql.func.now(), comment="Timestamp for the last change to the preference settings")

    # Foreign key relationship to the user who created the type of preferences
    createdby = UUIDFKey(comment="Foreign key to the user who created the preference settings")

    # Foreign key relationship to the user who changed the type of preferences
    changedby = UUIDFKey(comment="Foreign key to the user who has changed this preference settings")

    #Foreign key to the parent preference settings type
    preference_settings_type_id =  Column(ForeignKey("preference_settings_types.id"), index=True, comment="Preference Settings type of this settings (parent type)")

    #order in parent entity (Preference Settings Type)
    order = Column(Integer, comment="order in parent entity")

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")

    #default_settings = Column(Boolean,comment="is it default preference settings? True=Default", default=False)

    #userids = Column(ARRAY(Uuid), comment="Array of user IDs with this preference setting")

    #Relationship to parent preference settings type
    type = relationship("PreferenceSettingsTypeModel", back_populates="preference_settings", uselist=False)
