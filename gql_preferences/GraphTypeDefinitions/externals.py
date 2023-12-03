#import typing
import strawberry
from uuid import UUID

@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: UUID):
        if(id is None):
            return None
        return cls(id=id)

@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: UUID):
        if(id is None):
            return None
        return cls(id=id)

@strawberry.federation.type(extend=True, keys=["id"])
class EventGQLModel:

    id: UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: UUID):
        if(id is None):
            return None
        return cls(id=id)
    
@strawberry.federation.type(extend=True, keys=["id"])
class FacilityGQLModel:

    id: UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: UUID):
        if(id is None):
            return None
        return cls(id=id)