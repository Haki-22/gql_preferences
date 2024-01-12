import strawberry
import datetime
from typing import Union, Optional, List, Annotated

from .externals import UserGQLModel, GroupGQLModel, FacilityGQLModel, EventGQLModel
from uuid import UUID

from ..utils.Dataloaders import  getLoaders, getUser
from ._GraphPermissions import OnlyForAuthentized, RoleBasedPermission

from .BaseGQLModel import BaseGQLModel

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


PreferenceSettingsGQLModel = Annotated["PreferenceSettingsGQLModel", strawberry.lazy(".PreferenceSettingsGQLModel")]

@strawberry.federation.type(keys=["id"], description="Entity representing types of preference settings like language, theme")
class PreferenceSettingsTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoaders(info).preference_settings_types

    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    name_en = resolve_name_en
    rbacobject = resolve_rbacobject


#    """  # Fields representing properties of the PreferenceSettings
#    @strawberry.field(description="primary key")
#    async def id(self, info: strawberry.types.Info) -> UUID:
#        return self.id
#
#    @strawberry.field(description="name of the type preference")
#    async def name(self, info: strawberry.types.Info) -> str:
#        return self.name 
#    
#    @strawberry.field(description="name of the type preference in english")
#    async def name_en(self, info: strawberry.types.Info) -> str:
#        return self.name_en
#
#    @strawberry.field(description="timestamp for when the type preference were created")
#    async def created(self, info: strawberry.types.Info) -> datetime.datetime:
#        return self.created
#    
#    @strawberry.field(description="user who created the type preference")
#    async def createdby(self, info: strawberry.types.Info) -> Union[UserGQLModel, None]:
#        result = await UserGQLModel.resolve_reference(id=self.createdby)
#        return result
#
#    @strawberry.field(description="timestamp for the last change to the type preference")
#    async def lastchange(self, info: strawberry.types.Info) -> datetime.datetime:
#        return self.lastchange
#
#    @strawberry.field(description="user who last changed the type preference")
#    async def changedby(self, info: strawberry.types.Info) -> Union[UserGQLModel, None]:
#        result = await UserGQLModel.resolve_reference(id=self.changedby)
#        return result """

    @strawberry.field(description="Retrieves default preference settings ID", permission_classes=[OnlyForAuthentized()])
    async def default_preference_settings_id(self, info:strawberry.types.info) -> UUID:
        return self.default_preference_settings_id
    
    @strawberry.field(description="Preference settings type's order", permission_classes=[OnlyForAuthentized()])
    async def order(self,  info: strawberry.types.Info) -> Optional[int]:
        return self.order if self.order else 0
    
    @strawberry.field(description="Preference settings", permission_classes=[OnlyForAuthentized()])
    async def preference_settings(self, info: strawberry.types.Info) -> List["PreferenceSettingsGQLModel"]:
        loader = getLoaders(info).preference_settings
        rows = await loader.filter_by(preference_settings_type_id=self.id)
        return rows
    
    async def default_preference_settings_func(self,  info: strawberry.types.Info) -> Optional["PreferenceSettingsGQLModel"]:
        from .PreferenceSettingsGQLModel import PreferenceSettingsGQLModel
        loader = getLoaders(info).preference_settings
        result = await PreferenceSettingsGQLModel.resolve_reference(info=info, id=self.default_preference_settings_id)
        return result
    
    default_preference_settings = strawberry.field(description="Preference settings type's default settings", permission_classes=[OnlyForAuthentized()])(default_preference_settings_func)

#############################################################
#
# Queries
#
#############################################################

 # Query for a page of preference types
#"""@strawberry.field(description="Returns page of preference settings types, [opt.] skip=0, limit=20")
#async def preference_settings_type_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 20) -> List[PreferenceSettingsTypeGQLModel]:
#        loader = getLoaders(info).preference_settings_types
#        return await loader.page(skip, limit) """

from dataclasses import dataclass
from .utils import createInputs

PreferenceSettingsWhereFilter = Annotated["PreferenceSettingsWhereFilter", strawberry.lazy(".PreferenceSettingsGQLModel")]
@createInputs
@dataclass
class PreferenceSettingsTypeWhereFilter:
    name: str
    name_en: str
    id: UUID

    preference_settings: PreferenceSettingsWhereFilter

# Define the function without the decorator
async def preference_settings_type_page_function(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[PreferenceSettingsTypeWhereFilter] = None) -> List[PreferenceSettingsTypeGQLModel]:

    loader = getLoaders(info).preference_settings_types
    wf = None if where is None else strawberry.asdict(where)
    return await loader.page(skip, limit, where=wf)

# Decorate the function with strawberry
preference_settings_type_page = strawberry.field(description="Retrieves the preference Settings type page", permission_classes=[OnlyForAuthentized()])(preference_settings_type_page_function)



import uuid
# Query for searching preference types by ID
async def preference_settings_type_by_id_function(self, info: strawberry.types.Info, id: UUID) -> Optional[PreferenceSettingsTypeGQLModel]:
    return await PreferenceSettingsTypeGQLModel.resolve_reference(info=info, id=id)

preference_settings_type_by_id = strawberry.field(description="""Returns Preference settings type by ID""", permission_classes=[OnlyForAuthentized()])(preference_settings_type_by_id_function)

#@strawberry.field(description="Returns default preference settings in type by it's ID")
#async def preference_settings_default_by_type_id(self, info: strawberry.types.Info, type_id: UUID) -> Optional[UUID]:
#    result = await PreferenceSettingsTypeGQLModel.resolve_reference(info=info, id=type_id)
#    return result.default_preference_settings_id

##Returns all preference settings types IDs in an arrays
#async def preference_settings_type_ids(self, info: strawberry.types.Info) -> List[UUID]:
#    typeloader = getLoaders(info).preference_settings_types
#    rows = await typeloader.page()
#    result = []
#    for row in rows:
#        #if row.id:     
#        #print(row.id, "row.id")
#        result.append(row.id)
#    return result

# Query for searching default preference settings for a type

async def preference_settings_default_by_type_id_func(self, info: strawberry.types.Info, id: UUID) -> List["PreferenceSettingsGQLModel"]:
    result = await PreferenceSettingsTypeGQLModel.resolve_reference(info=info, id=id)
    preference_settings_id = result.default_preference_settings_id
    loader = getLoaders(info).preference_settings
    result = await loader.filter_by(id=preference_settings_id)
    return result

preference_settings_default_by_type_id = strawberry.field(description="Returns default preference settings for a type", permission_classes=[OnlyForAuthentized()])(preference_settings_default_by_type_id_func)
#####################################################################
#
# Mutations
#
#####################################################################

################### 
# Create
@strawberry.input(description="Creates a new preference settings type")
class PreferenceSettingsTypeInsertGQLModel:
    id: Optional[uuid.UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    rbacobject: strawberry.Private[uuid.UUID] = None 

    name: str = strawberry.field(description="Preference settings type name")
    name_en: Optional[str] = strawberry.field(description="Preference settings type name in english", default="")
    
    createdby: strawberry.Private[uuid.UUID] = None 


################# 
# Update
@strawberry.input(description="Updates already existing preference settings type")
class PreferenceSettingsTypeUpdateGQLModel:
    
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")

    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    name: Optional[str] = strawberry.field(description="Preference settings type name", default=None)
    name_en: Optional[str] = strawberry.field(description="Preference settings type english name", default="")
    default_preference_settings_id: Optional[UUID] = strawberry.field(description="ID of default preference settings", default=None)

    changedby: strawberry.Private[uuid.UUID] = None

################# 
# Delete
@strawberry.input(description="Deletes already existing preference settings type")
class PreferenceSettingsTypeDeleteGQLModel:
    
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")



#####################################################################
#                   RESULT
@strawberry.type(description="Result of CU operations")
class PreferenceSettingsTypeResultGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key of CU operation object")
    msg: str = strawberry.field(description="""Should be `ok` if desired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="Object of CU operation, final version")
    async def preference_settings_type(self, info: strawberry.types.Info) -> Union[PreferenceSettingsTypeGQLModel, None]:
        return await PreferenceSettingsTypeGQLModel.resolve_reference(info=info, id=self.id)
#
#####################################################################



#Create new PreferenceSettingsType
@strawberry.mutation(description="""Inserts a new preference settings type, 
                     If name already exists, operation will fail,
                     if no ID is given, generates a new one""", permission_classes=[OnlyForAuthentized()])
async def preference_settings_type_insert(self, info: strawberry.types.Info, preference_settings_type: PreferenceSettingsTypeInsertGQLModel) -> PreferenceSettingsTypeResultGQLModel:
    
    if preference_settings_type.id is None:
        preference_settings_type.id = uuid.uuid4()

    loader = getLoaders(info).preference_settings_types
    rows = await loader.filter_by(name=preference_settings_type.name)
    row = next(rows, None)
    if row is not None:     
        return PreferenceSettingsTypeResultGQLModel(id=preference_settings_type.id, msg="fail name alreade exist")

    actingUser = getUser(info)
    preference_settings_type.createdby = uuid.UUID(actingUser["id"])

    await loader.insert(preference_settings_type)
    return PreferenceSettingsTypeResultGQLModel(id=preference_settings_type.id, msg="OK, created")
 

# Update already existing PreferenceSettingsType
@strawberry.mutation(description="""Updates already existing settings type
                     requires ID and lastchange""", permission_classes=[OnlyForAuthentized()])
async def preference_settings_type_update(self, info: strawberry.types.Info, preference_settings_type: PreferenceSettingsTypeUpdateGQLModel) -> PreferenceSettingsTypeResultGQLModel:
    actingUser = getUser(info)
    loader = getLoaders(info).preference_settings_types
    preference_settings_type.changedby = uuid.UUID(actingUser["id"])

    row = await loader.update(preference_settings_type)
    if row is None:
        return PreferenceSettingsTypeResultGQLModel(id=preference_settings_type.id, msg="fail")
    
    return PreferenceSettingsTypeResultGQLModel(id=preference_settings_type.id, msg="OK, updated")

# Delete existing PreferenceSettingsType
@strawberry.mutation(description="""Deletes already existing settings type
                     requires ID and lastchange""", permission_classes=[OnlyForAuthentized()])
async def preference_settings_type_delete(self, info: strawberry.types.Info, preference_settings_type: PreferenceSettingsTypeDeleteGQLModel) -> PreferenceSettingsTypeResultGQLModel:
    loader = getLoaders(info).preference_settings_types

    rows = await loader.filter_by(id=preference_settings_type.id)
    row = next(rows, None)
    if row is None:     
        return PreferenceSettingsTypeResultGQLModel(id=preference_settings_type.id, msg="Fail bad ID")

    rows = await loader.filter_by(lastchange=preference_settings_type.lastchange)
    row = next(rows, None)
    if row is None:     
        return PreferenceSettingsTypeResultGQLModel(id=preference_settings_type.id, msg="Fail (bad lastchange?)")
    
    #### Delete all children preference settings 
    from .PreferenceSettingsGQLModel import preference_settings_delete
    preference_settings_loader = getLoaders(info).preference_settings
    rows = await preference_settings_loader.filter_by(preference_settings_type_id=preference_settings_type.id)
    for row in rows:
        #print(row.id)
        await preference_settings_loader.delete(row.id)
        
    await loader.delete(preference_settings_type.id)

    return PreferenceSettingsTypeResultGQLModel(id=preference_settings_type.id, msg="OK, deleted")


