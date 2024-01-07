#import typing
import strawberry
from uuid import UUID
from typing import List, Annotated, Optional
from ..utils.Dataloaders import  getLoaders

PreferenceUserSettingsGQLModel = Annotated["PreferenceUserSettingsGQLModel", strawberry.lazy(".PreferenceUserSettingsGQLModel")]
PreferenceTagEntityGQLModel = Annotated["PreferenceTagEntityGQLModel", strawberry.lazy(".PreferenceTagEntityGQLModel")]

@classmethod
async def resolve_reference(cls, id: UUID):
    if(id is None):
        return None
    return cls(id=id)

async def preference_tags_for_entity_func(self, info: strawberry.types.Info) -> Optional[List["PreferenceTagEntityGQLModel"]]:
        loader = getLoaders(info).preferedtagentities
        result = await loader.filter_by(entity_id=self.id)
        return result

@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    @strawberry.field(description="Returns specific preference settings page for a user")
    async def preference_settings_user_page(self, info: strawberry.types.Info) -> Optional[List["PreferenceUserSettingsGQLModel"]]:
        from .PreferenceUserSettingsGQLModel import PreferenceUserSettingsGQLModel
        return await PreferenceUserSettingsGQLModel.preference_settings_user_page_func(self, info)
    
    preference_tags_for_entity = strawberry.field(description="Returns page of tags for the entity.")(preference_tags_for_entity_func)

@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: UUID = strawberry.federation.field(external=True)

    resolve_reference = resolve_reference
    preference_tags_for_entity = strawberry.field(description="Returns page of tags for the entity.")(preference_tags_for_entity_func)

@strawberry.federation.type(extend=True, keys=["id"])
class EventGQLModel:

    id: UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference
    preference_tags_for_entity = strawberry.field(description="Returns page of tags for the entity.")(preference_tags_for_entity_func)

    
@strawberry.federation.type(extend=True, keys=["id"])
class FacilityGQLModel:

    id: UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference
    preference_tags_for_entity = strawberry.field(description="Returns page of tags for the entity.")(preference_tags_for_entity_func)
