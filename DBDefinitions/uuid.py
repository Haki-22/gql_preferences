from uuid import uuid4
from sqlalchemy import Column, Uuid

def UUIDFKey(comment=None, nullable=True, **kwargs):
    return Column(Uuid, index=True, comment=comment, nullable=nullable, **kwargs)

def UUIDColumn():
    return Column(Uuid, primary_key=True, comment="Unique identifier / primary key", default=uuid4, index=True)