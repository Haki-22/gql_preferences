#import typing
import strawberry
from uuid import UUID
from typing import List, Annotated

PreferenceSettingsGQLModel = Annotated["PreferenceSettingsGQLModel", strawberry.lazy(".PreferenceSettingsGQLModel")]

@classmethod
async def resolve_reference(cls, id: UUID):
    if(id is None):
        return None
    return cls(id=id)

@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    @strawberry.field()
    async def settings(self, info: strawberry.types.Info) -> List[PreferenceSettingsGQLModel]:
        pass
    
    """ @classmethod
    async def resolve_array_reference(cls, id):
        if id is None:
            return None
        id_strings = [f"'{user_id}'" for user_id in id]
        formatted_string = ', '.join(id_strings)
        return cls(id=formatted_string) """
    
@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: UUID = strawberry.federation.field(external=True)

    resolve_reference = resolve_reference

    """ @classmethod
    async def resolve_reference(cls, id: UUID):
        if(id is None):
            return None
        return cls(id=id) """

@strawberry.federation.type(extend=True, keys=["id"])
class EventGQLModel:

    id: UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    """ @classmethod
    async def resolve_reference(cls, id: UUID):
        if(id is None):
            return None
        return cls(id=id) """
    
@strawberry.federation.type(extend=True, keys=["id"])
class FacilityGQLModel:

    id: UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    """ @classmethod
    async def resolve_reference(cls, id: UUID):
        if(id is None):
            return None
        return cls(id=id) """