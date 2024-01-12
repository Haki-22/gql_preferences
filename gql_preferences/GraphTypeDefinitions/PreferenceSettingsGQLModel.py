import strawberry
import datetime
from typing import Union, Optional, List, Annotated
import logging

from .externals import UserGQLModel, GroupGQLModel, FacilityGQLModel, EventGQLModel
from uuid import UUID, uuid4

from ..utils.Dataloaders import  getLoaders, getUser
from ._GraphPermissions import OnlyForAuthentized, RoleBasedPermission

from .BaseGQLModel import BaseGQLModel
import sqlalchemy.sql

from ._GraphResolvers import(
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_rbacobject,
)

PreferenceSettingsTypeGQLModel = Annotated["PreferenceSettingsTypeGQLModel", strawberry.lazy(".PreferenceSettingsTypeGQLModel")]
UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]

@strawberry.federation.type(keys=["id"], description="Entity representing preference setting / value of a preference settings type like English or Dark")
class PreferenceSettingsGQLModel(BaseGQLModel):
    """
    Entity representing preference setting of parent Preference Settings Type
    """
    @classmethod
    def getLoader(cls, info):
        return getLoaders(info).preference_settings
    
    # @classmethod
    # async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
    # implementation is inherited

    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    name_en = resolve_name_en
    rbacobject = resolve_rbacobject

    @strawberry.field(description="Preference settings's order", permission_classes=[OnlyForAuthentized()])
    def order(self) -> int:
        return self.order if self.order else 0
    
    """ @strawberry.field(description="Default preference settings of a parent type (1=Default, 0=Not-default)")
    def default_settings(self) -> int:
        return self.default_settings """
    
    @strawberry.field(description="Retrieves the preference_settings_type_id ", permission_classes=[OnlyForAuthentized()])
    def preference_settings_type_id(self) -> UUID:
        return self.preference_settings_type_id


    @strawberry.field(description="Retrieves the Preference Settings Type", permission_classes=[OnlyForAuthentized()])
    async def type(self, info: strawberry.types.Info) -> Optional["PreferenceSettingsTypeGQLModel"]:
        from .PreferenceSettingsTypeGQLModel import PreferenceSettingsTypeGQLModel
        result = None if self.preference_settings_type_id is None else await PreferenceSettingsTypeGQLModel.resolve_reference(info=info, id=self.preference_settings_type_id)
        return result
    
    """ @strawberry.field(description="Retrieves users that have this settings")
    async def user_ids(self, info: strawberry.types.Info) -> Optional["UserGQLModel"]:
        from .externals import UserGQLModel
        #print(self.userids, "neco")
        return await UserGQLModel.resolve_array_reference(id=self.userids) """
    
#############################################################
#
# Queries
#
#############################################################

""" # Query for a page of a preference setting
@strawberry.field(description="Returns page of preference settings, [opt.] skip=0, limit=20")
async def preference_settings_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 20) -> List[PreferenceSettingsGQLModel]:
        loader = getLoaders(info).preference_settings
        return await loader.page(skip, limit) """

from dataclasses import dataclass
from .utils import createInputs

@createInputs
@dataclass
class PreferenceSettingsWhereFilter:
    name: str
    name_en: str

    preference_settings_type_id: UUID
    createdby: UUID

    from .PreferenceSettingsTypeGQLModel import PreferenceSettingsTypeWhereFilter
    type: PreferenceSettingsTypeWhereFilter

@strawberry.field(description="Returns page of preference settings, [opt.] skip=0, limit=20, where", permission_classes=[OnlyForAuthentized()])
async def preference_settings_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[PreferenceSettingsWhereFilter] = None) -> List[PreferenceSettingsGQLModel]:

    wf = None if where is None else strawberry.asdict(where)
    loader = getLoaders(info).preference_settings
    return await loader.page(skip, limit, where=wf)


# Query for searching preference settings  by ID
@strawberry.field(description="Returns Preference settings by ID", permission_classes=[OnlyForAuthentized()])
async def preference_settings_by_id(self, info: strawberry.types.Info, id: UUID) -> Optional[PreferenceSettingsGQLModel]:
    return await PreferenceSettingsGQLModel.resolve_reference(info=info, id=id)

#""" # Query default settings 
#@strawberry.field(description="Returns default preference settings page")
#async def preference_settings_default_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 20) -> List[PreferenceSettingsGQLModel]:
#    loader = getLoaders(info).preference_settings
#    result = await loader.filter_by(default_settings=True)
#    return result """
#
#""" # Query for searching default preference settings for a type
#@strawberry.field(description="Returns default preference settings for a type")
#async def preference_settings_default_by_type_id(self, info: strawberry.types.Info, type_id: UUID) -> List[PreferenceSettingsGQLModel]:
#    loader = getLoaders(info).preference_settings
#    result = await loader.filter_by(preference_settings_type_id=type_id, default_settings=True)
#    return result
# """
#
######## filter by nejde pouzit s ARRAY, porovnana ID=ID
#""" # Query for a page of a user settings
#@strawberry.field(description="Returns preference settings page for a user")
#async def user_settings_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 20) -> List[PreferenceSettingsGQLModel]:
#    loader = getLoaders(info).preference_settings
#    actingUser = getUser(info)
#    actingUserId = actingUser["id"]
#    print(actingUserId, "user_id")
#    #result = await loader.filter_by(userids=actingUserId)
#    #print(self.userids, "userids")
#    
#    result = await loader.filter_by(userids=actingUserId)
#    return result
# """


#####################################################################
#
# Mutations
#
#####################################################################

################### 
# Create
@strawberry.input(description="Creates a new preference settings")
class PreferenceSettingsInsertGQLModel:
    id: Optional[UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)

    name: str = strawberry.field(description="Preference settings name")
    name_en: Optional[str] = strawberry.field(description="Preference settings english name", default="")
    rbacobject: strawberry.Private[UUID] = None 
    
    order: Optional[int] = strawberry.field(description="Position in parent entity", default=None)
    preference_settings_type_id: UUID = strawberry.field(description="id of parent entity")
    createdby: strawberry.Private[UUID] = None 

################# 
# Update
@strawberry.input(description="Updates already existing preference settings")
class PreferenceSettingsUpdateGQLModel:
    id: UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")
    
    name: Optional[str] = strawberry.field(description="Preference settings name", default=None)
    name_en: Optional[str] = strawberry.field(description="Preference settings english name", default="")
    
    order: Optional[int] = strawberry.field(description="Position in parent entity", default=None)
    changedby: strawberry.Private[UUID] = None


#####################################################################
#                   RESULT
@strawberry.type(description="Result of CU operations")
class PreferenceSettingsResultGQLModel:
    id: Optional[UUID] = strawberry.field(description="primary key of CU operation object")
    msg: str = strawberry.field(description="""Should be `ok` if desired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="Object of CU operation, final version")
    async def preference_settings(self, info: strawberry.types.Info) -> Union[PreferenceSettingsGQLModel, None]:
        return await PreferenceSettingsGQLModel.resolve_reference(info=info, id=self.id)
#
#####################################################################



#""" async def update_parent(info:strawberry.types.Info, parentID: UUID):
#    
#    print(parentID, "moment")
#    preference_settings_type_loader = getLoaders(info).preference_settings_types
#    rows = await preference_settings_type_loader.filter_by(id=parentID)
#    row = next(rows, None)
#    if row:
#        print(row.id, "moment")
#        return await preference_settings_type_loader.update
#    else:
#        print(f"No row found for ID: {parentID}")
#        return None
#
# """

#Create new PreferenceSettings
@strawberry.mutation(description="""Inserts a new preference settings, 
                     If name already exists, operation will fail,
                     if no ID is given, generates a new one""", permission_classes=[OnlyForAuthentized()])
async def preference_settings_insert(self, info: strawberry.types.Info, preference_settings: PreferenceSettingsInsertGQLModel) -> PreferenceSettingsResultGQLModel:
    if preference_settings.id is None:
        preference_settings.id = uuid4()

    loader = getLoaders(info).preference_settings
    rows = await loader.filter_by(name=preference_settings.name)
    row = next(rows, None)
    if row is not None:     
        return PreferenceSettingsResultGQLModel(id=preference_settings.id, msg="fail name alreade exist")

    user = getUser(info)
    preference_settings.createdby = UUID(user["id"])

    #await update_parent(info, parentID=preference_settings.preference_settings_type_id)
      
    await loader.insert(preference_settings)
    
    return PreferenceSettingsResultGQLModel(id=preference_settings.id, msg="OK, created")
 

# Update already existing PreferenceSettings
@strawberry.mutation(description="""Updates already existing settings
                     requires ID and lastchange""", permission_classes=[OnlyForAuthentized()])
async def preference_settings_update(self, info: strawberry.types.Info, preference_settings: PreferenceSettingsUpdateGQLModel) -> PreferenceSettingsResultGQLModel:
    actingUser = getUser(info)
    loader = getLoaders(info).preference_settings
    preference_settings.changedby = UUID(actingUser["id"])

    row = await loader.update(preference_settings)
    if row is None:
        return PreferenceSettingsResultGQLModel(id=preference_settings.id, msg="fail (bad lastchange?)")
    
    return PreferenceSettingsResultGQLModel(id=preference_settings.id, msg="OK, updated")

# Delete existing PreferenceSettings
@strawberry.mutation(description="""Deletes already existing preference settings 
                     rrequires ID and lastchange""", permission_classes=[OnlyForAuthentized()])
async def preference_settings_delete(self, info: strawberry.types.Info, preference_settings: PreferenceSettingsUpdateGQLModel) -> PreferenceSettingsResultGQLModel:
    loader = getLoaders(info).preference_settings

    rows = await loader.filter_by(id=preference_settings.id)
    row = next(rows, None)
    if row is None:     
        return PreferenceSettingsResultGQLModel(id=preference_settings.id, msg="Fail bad ID")

    rows = await loader.filter_by(lastchange=preference_settings.lastchange)
    row = next(rows, None)
    if row is None:     
        return PreferenceSettingsResultGQLModel(id=preference_settings.id, msg="Fail (bad lastchange?)")
    
    id_for_resposne = preference_settings.id
    await loader.delete(preference_settings.id)
    
    return PreferenceSettingsResultGQLModel(id=id_for_resposne, msg="OK, deleted")