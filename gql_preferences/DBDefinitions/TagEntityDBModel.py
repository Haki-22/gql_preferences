import sqlalchemy
from sqlalchemy import Column, String, DateTime, ForeignKey
from uoishelpers.uuid import UUIDColumn
from .Base import BaseModel, UUIDFKey

# Define a SQLAlchemy model for the 'preferedtagentities' table
class TagEntityModel(BaseModel):
    # Table name
    __tablename__ = "preferedtagentities"
    
    # Unique identifier for the tag entity
    id = UUIDColumn(postgres=False)

    # Foreign key relationship to the author/user who created the tag entity
    author_id = UUIDFKey(nullable=True, comment="Foreign key to the author/user who created the tag entity")

    # Foreign key relationship to the tag associated with the entity
    tag_id = Column(ForeignKey("preferedtags.id"), index=True, nullable=True, comment="Foreign key to the tag associated with the entity")

    # Foreign key relationship to the entity
    entity_id = UUIDFKey(nullable=True, comment="Foreign key to the entity")

    # Foreign key relationship to the entity type
    entity_type_id = UUIDFKey(nullable=True, comment="Foreign key to the entity type")

    # Timestamp for when the tag entity was created
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp for when the tag entity was created")

    # Timestamp for the last change to the tag entity
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp for the last change to the tag entity")
    
    # Foreign key relationship to the user who created the tag entity
    createdby = UUIDFKey(nullable=True, comment="Foreign key to the user who created the tag entity")

    # Foreign key relationship to the user who last changed the tag entity
    changedby = UUIDFKey(nullable=True, comment="Foreign key to the user who last changed the tag entity")
