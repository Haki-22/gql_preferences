import strawberry
import datetime
from typing import Union, Optional, List, Annotated

from .externals import UserGQLModel, GroupGQLModel, FacilityGQLModel, EventGQLModel

from utils.Dataloaders import  getLoaders, getUser
from ._GraphPermissions import OnlyForAuthentized

from uuid import UUID

from .BaseGQLModel import BaseGQLModel

from ._GraphResolvers import(
    resolve_id,

    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_rbacobject,
)

# GraphQL type representing GQL model ID and name
@strawberry.type(description="""represents a GQL model""")
class PreferenceEntityIdGQLModel:
    @strawberry.field(description="""primary key""")
    async def model_id(self, info: strawberry.types.Info) -> UUID:
        return self["id"]

    @strawberry.field(description="""GQL model name""")
    async def model_name(self, info: strawberry.types.Info) -> str:
        return self["name"]

# Dictionary mapping entity type IDs to corresponding classes
entity_type_ids = {                                                 #Identify all
    UUID("e8479a21-b7c4-4140-9562-217de2656d55"): UserGQLModel,     #users
    UUID("2d3d9801-0017-4cf2-9272-2df7b59da667"): GroupGQLModel,    #Groups
    UUID("a7457888-ed8a-4720-b116-13558cd7963b"): EventGQLModel,    #Events
    UUID("9feb8037-6c62-45bb-ac20-916763731f5d"): FacilityGQLModel  #Facilities
}


PreferenceTagGQLModel = Annotated["PreferenceTagGQLModel", strawberry.lazy(".PreferenceTagGQLModel")]

# GraphQL type representing a tag or label that can be assigned to entities
@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing a tag / label which can be assigned to entities""",
)
class PreferenceTagEntityGQLModel(BaseGQLModel):
    # Reference resolution for the tag entity
    
    @classmethod
    def getLoader(cls, info):
        return getLoaders(info).preferedtagentities

    # Fields representing properties of the tag entity
    id = resolve_id
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    rbacobject = resolve_rbacobject

    """ @strawberry.field(description="Time stamp")
    async def lastchange(self, info: strawberry.types.Info) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="date of creation")
    async def created(self, info: strawberry.types.Info) -> datetime.datetime:
        return self.created

    @strawberry.field(description="user who created this tag")
    async def createdby(self, info: strawberry.types.Info) -> Union[UserGQLModel, None]:
        result = await UserGQLModel.resolve_reference(id=self.createdby)
        return result

    strawberry.field(description="user who created this tag")
    async def createdby(self, info: strawberry.types.Info) -> Union[UserGQLModel, None]:
        result = await UserGQLModel.resolve_reference(id=self.createdby)
        return result """

    """ @strawberry.field(description="tag value, can be "red", "2023", etc. ")
    async def value(self, info: strawberry.types.Info) -> Union[str, None]:
        return self.value """

    """     @strawberry.field(description="Entities associated with this tag")
    async def entities(self, info: strawberry.types.Info) -> List[Optional[Union[Union["UserGQLModel", "GroupGQLModel"], Union["EventGQLModel","FacilityGQLModel" ]]]]:
        loader = getLoaders(info).preferedtagentities
        actingUser = getUser(info)
        actingUserId = actingUser["id"]
        rows = await loader.filter_by(tag_id=self.tag_id, author_id=actingUserId)
        print(self.tag_id, "tagID")
        result = []
        for row in rows:
            entity_type_id = row.entity_type_id
            entity_id = row.entity_id
            print(entity_id, "Neco")
            print(row.author_id, "author")
            print(entity_type_ids, "entity_type_ids")
            print(entity_type_id, "entityType")
            
            print("Keys in entity_type_ids:", list(entity_type_ids.keys()))
            
            entityClass = entity_type_ids.get(entity_type_id, None)
            print(entityClass, "entityClass")
            for key in entity_type_ids.keys():
                print(repr(entity_type_id), repr(key), entity_type_id == key)

            if entityClass is not None:
                entity = await entityClass.resolve_reference(id=entity_id)
                print(entity_id, "Neco1")
                result.append(row)
        return result """


    @strawberry.field(description="""Entities associated with this tag""", permission_classes=[OnlyForAuthentized()])
    async def entities(self, info: strawberry.types.Info) -> List[Optional[Union[UserGQLModel, GroupGQLModel, EventGQLModel, FacilityGQLModel]]]:
        loader = getLoaders(info).preferedtagentities
        #actingUser = getUser(info)
        #actingUserId = actingUser["id"]
        rows = await loader.filter_by(tag_id=self.tag_id) #,author_id=actingUserId
        print(self.tag_id, "tagID")
        result = []
        for row in rows:
            entity_type_id = row.entity_type_id
            entity_id = row.entity_id
            #print(entity_type_id, "entityType")
            entityClass = entity_type_ids.get(entity_type_id, None)
            if entityClass is not None:
                # Assuming that resolve_reference returns an instance of the appropriate class
                entity = await entityClass.resolve_reference(id=entity_id)
                #print(entityClass, "entityClass")
                result.append(entity)
        return result

    @strawberry.field(description="Retrieves the tag", permission_classes=[OnlyForAuthentized()])
    async def tag(self, info: strawberry.types.Info) -> Optional["PreferenceTagGQLModel"]:
        from .PreferenceTagGQLModel import PreferenceTagGQLModel
        result = None if self.tag_id is None else await PreferenceTagGQLModel.resolve_reference(info=info, id=self.tag_id)
        return result
    
    @strawberry.field(description="Retrieves the entity_type_id", permission_classes=[OnlyForAuthentized()]) # Use the same entity resolution? (return whole enitty not just ID)
    async def entity_type_id(self, info: strawberry.types.Info) -> UUID:
        return self.entity_type_id
    
    async def preference_tags_for_entity_func(info: strawberry.types.Info, entity_id: UUID) -> List["PreferenceTagEntityGQLModel"]:
        
        actingUser = getUser(info)
        actingUserId = UUID(actingUser["id"])
        loader = getLoaders(info).preferedtagentities
        result = await loader.filter_by(author_id=actingUserId, entity_id=entity_id)
        return result
    
    """ @strawberry.field(description="Retrieves the entity_type_id ") # No Loaders...
    async def entity_type(self, info: strawberry.types.Info) -> UUID:
        return  None if self.entity_type_id is None else await PreferenceEntityIdGQLModel.resolve_reference(info=info, id=self.entity_type_id)
 """

""" for entity_type_id in entity_type_ids:
                # Check if typeid is not in user_type_ids
                if entity_type_id in entity_type_ids:
                    entityClass = entity_type_id
                    print(entity_type_id, "entityType")
                    print(entityClass, "entity") """

#####################################################################
#
# Special fields for queries
#
#####################################################################



# list of hardwired models for tags
tags_description = """Returns page of hardwired entity types for entity_type_id."""
@strawberry.field(description=tags_description, permission_classes=[OnlyForAuthentized()])
async def preference_entity_types(info: strawberry.types.Info) -> List["PreferenceEntityIdGQLModel"]:
    result = list(map(lambda item: {"id": item[0], "name": item[1].__strawberry_definition__.name}, entity_type_ids.items()))
    return result

# list of tags for the entity
preference_tags_for_entity = strawberry.field(description="Returns page of tags for the entity.", permission_classes=[OnlyForAuthentized()])(PreferenceTagEntityGQLModel.preference_tags_for_entity_func)


# list of entities labeled by tags
entities_description = """Returns page of entities labeled by tags."""
@strawberry.field(description=entities_description, permission_classes=[OnlyForAuthentized()])
async def preference_entities_labeled(info: strawberry.types.Info, tags: List[UUID]) -> List[Optional[Union[UserGQLModel, GroupGQLModel, EventGQLModel, FacilityGQLModel]]]:
    # TODO
    idsSet = set(tags)
    actingUser = getUser(info)
    actingUserId =UUID(actingUser["id"])

    loader = getLoaders(info).preferedtagentities

    stmt = loader.getSelectStatement()
    model = loader.getModel()
    
    fullstmt = stmt.filter_by(author_id=actingUserId).filter(model.tag_id.in_(tags))
    rows = await loader.execute_select(fullstmt)
    #Take all entities
    indexed = {}
    for row in rows:
        key = row.entity_id
        indexedvalue = indexed.get(key, None)
        if indexedvalue is None:
            indexedvalue = {"tags": set(), "type": row.entity_type_id}
            indexed[key] = indexedvalue
        indexedvalue["tags"].add(row.tag_id)
    # If issubset = True (Entity has both tags) then add to resultlist
    results = filter(lambda item: idsSet.issubset(item[1]["tags"]), indexed.items())
    resultList = []
    for id, value in results:
        cls = entity_type_ids[value["type"]]
        resultList.append(await cls.resolve_reference(id=id))
    return resultList


#####################################################################
#
# Mutation section
#
#####################################################################


# GraphQL input representing data to add a tag to an entity
@strawberry.input(description="""allows to create link between an GQL entity, tag and user who defined it""")
class PreferenceEntityAddTagGQLModel:
    entity_id: UUID = strawberry.field(default=None, description="GQL entity primary key value, aka GQL entity identification")
    rbacobject: strawberry.Private[UUID] = None 
    entity_type_id: UUID = strawberry.field(default=None, description="GQL entity type, aka UserGQLModel id")
    tag_id: UUID = strawberry.field(default=None, description="tag identification")
    createdby: strawberry.Private[UUID] = None

# GraphQL input representing data to remove a tag from an entity
@strawberry.input(description="""removes a tag from entity""")
class PreferenceEntityRemoveTagGQLModel:
    #entity_id: Optional[UUID] = strawberry.field(default=None, description="GQL entity primary key value, aka GQL entity identification")
    #tag_id: Optional[UUID] = strawberry.field(default=None, description="tag identification")
    id: UUID = strawberry.field(default=None, description="direct identification of the link, if not given, other two ids are used together")

# GraphQL type representing the result of a tag-related operation
@strawberry.type(description="reports the result of operation")
class PreferenceEntityTagResultGQLModel:
    msg: str = strawberry.field(default=None, description="""result of operation, should be "ok" or "fail" """)
    id: Optional[UUID] = strawberry.field(default=None, description="tag id")
    @strawberry.field(description="""""")
    async def tag(self, info: strawberry.types.Info) -> Union[PreferenceTagEntityGQLModel, None]:
        result = await PreferenceTagEntityGQLModel.resolve_reference(info, self.id)
        return result

# Delete result   
@strawberry.type(description="Result of D operations")
class PreferenceEntityTagDeleteResultGQLModel:
    id: UUID = strawberry.field(description="primary key of CU operation object")
    msg: str = strawberry.field(description="""Should be `ok` if desired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")


# GraphQL mutation to add a tag to an entity
@strawberry.mutation(description="""Marks an entity with a tag""", permission_classes=[OnlyForAuthentized()])
async def preference_tag_add_to_entity(self, info: strawberry.types.Info, tag_data: PreferenceEntityAddTagGQLModel) -> PreferenceEntityTagResultGQLModel:
    #assert tag_data.entity_type_id in entity_type_ids, "unknown entity type"
    actingUser = getUser(info)
    loader = getLoaders(info).preferedtagentities
    # is this entity already marked?
    rows = await loader.filter_by(tag_id=tag_data.tag_id, entity_id=tag_data.entity_id)
    row = next(rows, None)
    result = PreferenceEntityTagResultGQLModel()
    #no
    if row is None:
        row = await loader.insert(tag_data)
        result.id = row.id
        result.msg = "ok"
    #yes
    else:
        result.id = row.id
        result.msg = "fail"
    return result

# GraphQL mutation to remove a tag from an entity
@strawberry.mutation(description="""Removes a tag from entity""", permission_classes=[OnlyForAuthentized()])
async def preference_tag_remove_from_entity(self, info: strawberry.types.Info, tag_data: PreferenceEntityRemoveTagGQLModel) -> PreferenceEntityTagDeleteResultGQLModel:
    
    actingUser = getUser(info)
    loader = getLoaders(info).preferedtagentities
    #if tag_data.id is None:
    #    rows = await loader.filter_by(tag_id=tag_data.tag_id, entity_id=tag_data.entity_id)
    #    row = next(rows, None)
    #else:
    
    row = await loader.load(tag_data.id)
    await loader.delete(id=tag_data.id)
 
    result = PreferenceEntityTagDeleteResultGQLModel(id=tag_data.id, msg="tag removed from entity") if row else (
        PreferenceEntityTagDeleteResultGQLModel(id=tag_data.id, msg="fail")
    )
    return result



#####################################################################
#
# Special resolvers
#
#####################################################################



