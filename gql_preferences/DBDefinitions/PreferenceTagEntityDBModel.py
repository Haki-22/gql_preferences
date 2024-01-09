import sqlalchemy
from sqlalchemy import Column, String, DateTime, ForeignKey
from uoishelpers.uuid import UUIDColumn
from .Base import BaseModel
from .uuid import UUIDFKey, UUIDColumn

# Define a SQLAlchemy model for the 'preferedtagentities' table
class PreferenceTagEntityModel(BaseModel):
    # Table name
    __tablename__ = "preferedtagentities"
    
    # Unique identifier for the tag entity
    id = UUIDColumn()

    # Foreign key relationship to the author/user who created the tag entity
    author_id = UUIDFKey(comment="Foreign key to the author/user who created the tag entity")

    # Foreign key relationship to the tag associated with the entity
    tag_id = Column(ForeignKey("preferedtags.id"), index=True, comment="Foreign key to the tag associated with the entity")

    # Foreign key relationship to the entity
    entity_id = UUIDFKey( comment="Foreign key to the entity, which is labeled")

    # Foreign key relationship to the entity type
    entity_type_id = UUIDFKey(comment="Hardwired foreign key to the entity type like User / Group,")

    # Timestamp for when the tag entity was created
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp for when the tag entity was created")

    # Timestamp for the last change to the tag entity
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp for the last change to the tag entity")
    
    # Foreign key relationship to the user who created the tag entity
    createdby = UUIDFKey(comment="Foreign key to the user who created the tag entity")

    # Foreign key relationship to the user who last changed the tag entity
    changedby = UUIDFKey(comment="Foreign key to the user who last changed the tag entity")

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")
