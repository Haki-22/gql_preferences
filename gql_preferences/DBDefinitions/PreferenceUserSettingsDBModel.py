import sqlalchemy
from sqlalchemy import Column, String, DateTime, JSON, Uuid, ForeignKey, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .Base import BaseModel
from .uuid import UUIDFKey, UUIDColumn

# Relationship table for user defined settings (value) in a preferencesettings type (language:english theme:dark)
class PreferenceUserSettingsModel(BaseModel):
    # Table name
    __tablename__ = "user_settings"

    # Unique identifier for preference settings
    id = UUIDColumn()
    
    user_id = UUIDFKey(comment="Foreign key to the user with this setting")

    # Timestamp for when the tag entity was created
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp for when the user settings entity was created")

    # Timestamp for the last change to the preference
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), onupdate=sqlalchemy.sql.func.now(), comment="Timestamp for the last change to the preference settings")

    # Foreign key relationship to the user who changed the type of preferences
    changedby = UUIDFKey(comment="Foreign key to the user who has changed this preference settings")

    #Foreign key to the preference settings type
    preference_settings_type_id =  UUIDFKey(comment="Foreign key to the preference settings Type")

    #Foreign key to the preference settings 
    preference_settings_id = UUIDFKey(comment="Foreign key to the preference settings")

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")
    
    #order (Preference Settings Type)
    #order = Column(Integer, comment="order")

    #user_default_settings = Column(Boolean,comment="Does this user have default settings? True=Defdault", default=True)

    """ 
    #Relationship to preference settings type
    type = relationship("PreferenceSettingsTypeModel", back_populates="user_settings", uselist=False)

    #Relationship to preference settings 
    preference_settings = relationship("PreferenceSettingsModel", back_populates="user_settings", uselist=False) """

    """ #Foreign key to the preference settings type
    preference_settings_type_id =  Column(ForeignKey("preference_settings_types.id"), index=True, comment="Preference Settings type of this setting (parent type)")

    #Foreign key to the preference settings 
    preference_settings_id = Column(ForeignKey("preference_settings.id"), index=True, comment="children Preference Settings of parent type") """