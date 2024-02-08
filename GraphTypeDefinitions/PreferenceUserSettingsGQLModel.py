import strawberry
import datetime
from typing import Union, Optional, List, Annotated

from .externals import UserGQLModel, GroupGQLModel, FacilityGQLModel, EventGQLModel
from uuid import UUID, uuid4

from utils.Dataloaders import  getLoaders, getUser
from ._GraphPermissions import OnlyForAuthentized

from .BaseGQLModel import BaseGQLModel
import sqlalchemy.sql

from ._GraphResolvers import(
    resolve_id,

    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_rbacobject,
)

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
PreferenceSettingsTypeGQLModel = Annotated["PreferenceSettingsTypeGQLModel", strawberry.lazy(".PreferenceSettingsTypeGQLModel")]
PreferenceSettingsGQLModel = Annotated["PreferenceSettingsGQLModel", strawberry.lazy(".PreferenceSettingsGQLModel")]

@strawberry.federation.type(keys=["id"], description="Entity representing preference setting for a user")
class PreferenceUserSettingsGQLModel(BaseGQLModel):
    """
    Entity representing preference setting for a specific user
    Relationship table contains only non-default settings, those should be already setup in frontend
    (Cant load a page into no language, etc..)
    """
    
    @classmethod
    def getLoader(cls, info):
        return getLoaders(info).user_settings

    # @classmethod
    # async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
    # implementation is inherited

    id = resolve_id
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    rbacobject = resolve_rbacobject

    
    @strawberry.field(description="Retrieves the type of settings", permission_classes=[OnlyForAuthentized()])
    async def preference_settings_type_id(self, info: strawberry.types.Info) -> Optional["PreferenceSettingsTypeGQLModel"]:
        from .PreferenceSettingsTypeGQLModel import PreferenceSettingsTypeGQLModel
        return await PreferenceSettingsTypeGQLModel.resolve_reference(info, id=self.preference_settings_type_id)
    
    @strawberry.field(description="Retrieves the setting", permission_classes=[OnlyForAuthentized()])
    async def preference_settings_id(self, info: strawberry.types.Info) -> Optional["PreferenceSettingsGQLModel"]:
        from .PreferenceSettingsGQLModel import PreferenceSettingsGQLModel
        return await PreferenceSettingsGQLModel.resolve_reference(info, id=self.preference_settings_id)
    
    @strawberry.field(description="Retrieves the user", permission_classes=[OnlyForAuthentized()])
    async def user_id(self, info: strawberry.types.Info) -> Optional["UserGQLModel"]:
        from .externals import UserGQLModel
        return await UserGQLModel.resolve_reference(id=self.user_id)
    
    """ @strawberry.field(description="Retrieves if the user has default settings")
    async def user_default_settings(self, info: strawberry.types.Info) -> Optional["UserGQLModel"]:
        return await self.user_default_settings """
                
    # Query for a page of a user settings
    async def preference_settings_user_page_func(self, info: strawberry.types.Info, user_id: Optional[UUID] = None, skip: int = 0, limit: int = 20 ) -> List["PreferenceUserSettingsGQLModel"]:
        loader = getLoaders(info).user_settings
        
        if user_id is None:
            actingUser = getUser(info)
            user_id = UUID(actingUser["id"])
        
        return await loader.filter_by(user_id=user_id)
    
#############################################################
#
# Queries
#
#############################################################

##### User wont be able to see the relationship table, he can only change his settings with this GQLModel
##### The server should know the relationship table so that it can apply his settings
##### User should see the type (preference_settings_type_page_function) table and when he selects new settings value it shuould be saved in relationship table

""" # Query for a page of a user settings
@strawberry.field(description="Returns preference settings page for a user")
async def preference_settings_user_page(self, info: strawberry.types.Info, user_id: Optional[UUID] = None, skip: int = 0, limit: int = 20 ) -> List[PreferenceSettingsGQLModel]:
    loader = getLoaders(info).user_settings
    
    if user_id is None:
        actingUser = getUser(info)
        user_id = actingUser["id"]
    #print(user_id)

    #
    # Compare UserSettings Table and default settings table, if user settings type is not present -> default settings
    # Typ id s user_settings.preference_settings_type_id #maybe do on client side?
    from .PreferenceSettingsTypeGQLModel import preference_settings_type_ids
    typeids = await preference_settings_type_ids(self, info)
    
    print(typeids)

    user_result = await loader.filter_by(user_id=user_id)
    result = list(user_result)
    #rows= await loader.filter_by(user_id=user_id)
    user_type_ids = []
    for row in result:
        if row.preference_settings_type_id:
            user_type_ids.append(row.preference_settings_type_id)


    from .PreferenceSettingsTypeGQLModel import preference_settings_default_by_type_id_func
    # Iterate through typeids
    for typeid in typeids:
        # Check if typeid is not in user_type_ids
        if typeid not in user_type_ids:
            # get default preferenceSettings
            new = await preference_settings_default_by_type_id_func(self, info, id=typeid)
            result.append(new)
            #user_result += await preference_settings_default_by_type_id_func(self, info, id=typeid)
            
    
    

    #futures, asynciogather = prvně vytáhnout data z types s defaultem, potom k tomu joinnout ty co jsou v tabulce
    print(user_type_ids)
    #if result is not None: #Result = generated object
    return result
    #else:
    #    return default_settings
 """



preference_settings_user_page = strawberry.field(description="Returns preference settings page for a user", permission_classes=[OnlyForAuthentized()])(PreferenceUserSettingsGQLModel.preference_settings_user_page_func)

# Query for a page of a user settings
@strawberry.field(description="Returns preference settings in a type for a user", permission_classes=[OnlyForAuthentized()])
async def preference_settings_user_in_type(self, info: strawberry.types.Info, preference_settings_type_id: UUID, user_id: Optional[UUID] = None) -> List[PreferenceUserSettingsGQLModel]:
    loader = getLoaders(info).user_settings
    
    if user_id is None:
        actingUser = getUser(info)
        user_id = UUID(actingUser["id"])
    result = await loader.filter_by(user_id=user_id,preference_settings_type_id=preference_settings_type_id )
    #print(result, "result")
    
    return result


#(First look into new table, then asing default?) / Asign default then join changed ones

#####################################################################
#
# Mutations
#
#####################################################################

# Create
@strawberry.input(description="Creates a new preference settings for the user")
class PreferenceUserSettingsInsertGQLModel:
    id: Optional[UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)

    preference_settings_type_id: UUID = strawberry.field(description="id of type")
    preference_settings_id: UUID = strawberry.field(description="id of settings")
    user_id:  Optional[UUID] = strawberry.field(description="id of user, if not given gets the acting user", default=None)
    rbacobject: strawberry.Private[UUID] = None 
    #createdby: strawberry.Private[UUID] = None 

#################
# Update
@strawberry.input(description="Updates preference settings for the user")
class PreferenceUserSettingsUpdateGQLModel:
    id: UUID = strawberry.field(description="primary key (UUID)", default=None)
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")

    preference_settings_type_id: Optional[UUID] = strawberry.field(description="id of type", default=None)
    preference_settings_id: Optional[UUID] = strawberry.field(description="id of settings", default=None)
    user_id:  Optional[UUID] = strawberry.field(description="id of user, if not given gets the acting user", default=None)

    changedby: strawberry.Private[UUID] = None

################# 
# Delete
@strawberry.input(description="Deletes already existing preference settings")
class PreferenceUserSettingsDeleteGQLModel:
    
    id: UUID = strawberry.field(description="primary key (UUID), identifies object of operation")



#####################################################################
#                   RESULT
@strawberry.type(description="Result of CU operations")
class PreferenceUserSettingsResultGQLModel:
    id: Optional[UUID] = strawberry.field(description="primary key of CU operation object")
    msg: str = strawberry.field(description="""Should be `ok` if desired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")

    @strawberry.field(description="Object of CU operation, final version")
    async def preference_user_settings(self, info: strawberry.types.Info) -> Union[PreferenceUserSettingsGQLModel, None]:
        result = await PreferenceUserSettingsGQLModel.resolve_reference(info=info, id=self.id)
        return result

# Delete result   
@strawberry.type(description="Result of D operations")
class PreferenceUserSettingsDeleteResultGQLModel:
    id: UUID = strawberry.field(description="primary key of CU operation object")
    msg: str = strawberry.field(description="""Should be `ok` if desired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")


#
#####################################################################


#Create new User settings
@strawberry.mutation(description="""Inserts a new user setting, 
                     if User already has settings in this type, operation will fail
                     if no ID is given, generates a new one""", permission_classes=[OnlyForAuthentized()])
async def preference_user_settings_type_insert(self, info: strawberry.types.Info, user_settings: PreferenceUserSettingsInsertGQLModel) -> PreferenceUserSettingsResultGQLModel:
    
    if user_settings.id is None:
        user_settings.id = uuid4()

    loader = getLoaders(info).user_settings
    
    if(user_settings.user_id) is None:
        user = getUser(info)
        user_settings.user_id = UUID(user["id"])
        print(user["id"], 'UserID')
    
    rows = await loader.filter_by(preference_settings_type_id=user_settings.preference_settings_type_id, user_id= user_settings.user_id )
    row = next(rows, None)
    if row is not None:     
        return PreferenceUserSettingsResultGQLModel(id=user_settings.id, msg="fail user already has settings of this type, (update?)")

    await loader.insert(user_settings)
    return PreferenceUserSettingsResultGQLModel(id=user_settings.id, msg="OK, created")


# Update already existing User settings
@strawberry.mutation(description="""Updates already existing settings type
                     requires ID, ID of Type and lastchange
                     if the change is to default, removes settings type""", permission_classes=[OnlyForAuthentized()])
async def preference_user_settings_type_update(self, info: strawberry.types.Info, user_settings: PreferenceUserSettingsUpdateGQLModel) -> PreferenceUserSettingsResultGQLModel:
    actingUser = getUser(info)
    loader = getLoaders(info).user_settings
    
    user_settings.changedby = UUID(actingUser["id"])

    rows_type = await loader.filter_by(id=user_settings.id)
    row_type = next(rows_type, None)
    if row_type is None:     
        return PreferenceUserSettingsResultGQLModel(id=user_settings.id, msg="Fail bad ID")
    
    type_id = user_settings.preference_settings_type_id

    
    type_id = row_type.preference_settings_type_id
    
    if user_settings.preference_settings_type_id == None:
        user_settings.preference_settings_type_id = type_id

    print("TypeID:", type_id)

    ### Check if the update isnt to default settings, if it is -> delete it  
    from .PreferenceSettingsTypeGQLModel import preference_settings_type_by_id_function
    result = await preference_settings_type_by_id_function(self, info, id=type_id)
    
    if result.default_preference_settings_id == user_settings.preference_settings_id:
        await loader.delete(user_settings.id)
        return PreferenceUserSettingsResultGQLModel(id=user_settings.id, msg="OK, changed to default")
    

    row = await loader.update(user_settings)
    if row is None:
        return PreferenceUserSettingsResultGQLModel(id=user_settings.id, msg="fail")

    return PreferenceUserSettingsResultGQLModel(id=user_settings.id, msg="OK, updated")

# Delete existing User settings
@strawberry.mutation(description="""Deletes already existing User settings 
                     requires ID""", permission_classes=[OnlyForAuthentized()])
async def preference_user_settings_delete(self, info: strawberry.types.Info, user_settings: PreferenceUserSettingsDeleteGQLModel) -> PreferenceUserSettingsDeleteResultGQLModel:
    loader = getLoaders(info).user_settings

    rows = await loader.filter_by(id=user_settings.id)
    row = next(rows, None)
    if row is None:     
        return PreferenceUserSettingsDeleteResultGQLModel(id=user_settings.id, msg="Fail bad ID")
    
    await loader.delete(user_settings.id)
    
    return PreferenceUserSettingsDeleteResultGQLModel(id=user_settings.id, msg="OK, deleted")