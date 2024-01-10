import strawberry
from strawberry import lazy
import datetime
from typing import Union, Optional, List, TYPE_CHECKING, Annotated
from uuid import UUID, uuid4

from ..utils.Dataloaders import  getLoaders, getUser
from ._GraphPermissions import OnlyForAuthentized

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

PreferenceTagEntityGQLModel = Annotated["PreferenceTagEntityGQLModel", lazy(".PreferenceTagEntityGQLModel")]
UserGQLModel = Annotated["UserGQLModel", lazy(".externals")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing a tag""",
)
class PreferenceTagGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoaders(info).preferedtags
    
    id = resolve_id
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    name_en = resolve_name_en
    name = resolve_name
    rbacobject = resolve_rbacobject
    

    @strawberry.field(description="""entities marked with this tag""")
    async def links(self, info: strawberry.types.Info) -> List["PreferenceTagEntityGQLModel"]:
        loader = getLoaders(info).preferedtagentities
        result = await loader.filter_by(tag_id=self.id)
        return result

    @strawberry.field(description="Retrieves the user")
    async def author_id(self, info: strawberry.types.Info) -> Optional["UserGQLModel"]:
        from .externals import UserGQLModel
        return await UserGQLModel.resolve_reference(id=self.author_id)


#####################################################################
#
# Special fields for query
#
#####################################################################

# Query for a page of preference types
@strawberry.field(description="""Returns a page of tags, [opt.] skip=0, limit=20""")
async def preference_tags_page(
        self, info: strawberry.types.Info, skip: int = 0, limit: int = 20
    ) -> List[PreferenceTagGQLModel]:
        loader = getLoaders(info).preferedtags
        result = await loader.page(skip, limit)
        return result

tags_description = """Returns list of tags associated with asking user."""
@strawberry.field(description=tags_description)
async def preference_tags(self, info: strawberry.types.Info) -> List["PreferenceTagGQLModel"]:
    actingUser = getUser(info)
    loader = getLoaders(info).preferedtags
    return await loader.filter_by(author_id=actingUser["id"])

# New query field for searching by ID
@strawberry.field(description="Returns a tag by ID")
async def preference_tag_by_id(info: strawberry.types.Info, id: UUID) -> Optional[PreferenceTagGQLModel]:
    """ if id is not UUID: # doesnt work :C
        return None """
    return await PreferenceTagGQLModel.resolve_reference(info=info, id=id)


#####################################################################
#
# Mutation section
#
#####################################################################

import datetime

@strawberry.input(description="""Creates a new tag""")
class PreferenceTagInsertGQLModel:
    name: str = strawberry.field(default="new tag", description="tag name")
    id: Optional[UUID] = strawberry.field(default=None, description="optional primary key value of tag, UUID expected")
    createdby: strawberry.Private[UUID] = None #strawberry.field(default=None, description="user who created this db record")
    author_id: strawberry.Private[UUID] = None #strawberry.field(default=None, description="user who owns this tag")
    rbacobject: strawberry.Private[UUID] = None 

@strawberry.input(description="""Updates the tag""")
class PreferenceTagUpdateGQLModel:
    id: UUID = strawberry.field(default=None, description="primary key value, aka tag identification")
    name: str = strawberry.field(default=None, description="tag name")
    lastchange: datetime.datetime = strawberry.field(default=None, description="timestamp")
    updatedby: strawberry.Private[UUID] = None #strawberry.field(default=None, description="user who updates the tag")

@strawberry.input(description="""Removes the tag""")
class PreferenceTagDeleteGQLModel:
    name: str = strawberry.field(default=None, description="tag name, could be used as an identification")
    id: Optional[UUID] = strawberry.field(default=None, description="primary key, aka tag identification")


#####################################################################
#                   RESULT
@strawberry.type(description="""result of tag operation""")
class PreferenceTagResultGQLModel:
    id: Union[UUID, None] = strawberry.field(default=None, description="id of tag")
    msg: str = strawberry.field(default=None, description="""result of operation, should be "ok" or "fail" """)

    @strawberry.field(description="""Result of drone operation""")
    async def tag(self, info: strawberry.types.Info) -> Union[PreferenceTagGQLModel, None]:
        result = await PreferenceTagGQLModel.resolve_reference(info, self.id)
        return result
#
#####################################################################


@strawberry.mutation(description="inserts a new tag, if the name is already defined, operation will fail", permission_classes=[OnlyForAuthentized()])
async def preference_tag_insert(self, info: strawberry.types.Info, tag: PreferenceTagInsertGQLModel) -> PreferenceTagResultGQLModel:
    if tag.id is None:
        tag.id = uuid4()
    
    actingUser = getUser(info)
    loader = getLoaders(info).preferedtags
    tag.changedby = actingUser["id"]
    tag.author_id = actingUser["id"]
    result = PreferenceTagResultGQLModel()
    rows = await loader.filter_by(name=tag.name, author_id=actingUser["id"])
    row = next(rows, None)
    if row is None:
        row = await loader.insert(tag)
        result.id = row.id
        result.msg = "ok"
    else:
        result.id = row.id
        result.msg = "fail"
    return result

@strawberry.mutation(description="""deletes the tag""", permission_classes=[OnlyForAuthentized()])
async def preference_tag_delete(self, info: strawberry.types.Info, tag: PreferenceTagDeleteGQLModel) -> PreferenceTagResultGQLModel:
    actingUser = getUser(info)
    loader = getLoaders(info).preferedtags
    
    result = PreferenceTagResultGQLModel()
    result.id = tag.id
    if tag.id is None:
        # rows = await loader.filter_by(author_id=actingUser["id"])
        rows = await loader.filter_by(name=tag.name, author_id=actingUser["id"])
        row = next(rows, None)
    else:
        row = await loader.load(tag.id)

    if row is None:
        result.msg = "fail"
    else:
        await loader.delete(row.id)
        result.msg = "ok"
        result.id = None
        
    return result

@strawberry.mutation(description="""updates the tag""", permission_classes=[OnlyForAuthentized()])
async def preference_tag_update(self, info: strawberry.types.Info, tag: PreferenceTagUpdateGQLModel) -> PreferenceTagResultGQLModel:
    actingUser = getUser(info)
    loader = getLoaders(info).preferedtags
    tag.updatedby = actingUser["id"]

    result = PreferenceTagResultGQLModel()
    result.id = tag.id
    row = await loader.update(tag)
    if row is None:
        result.msg = "fail"
    else:
        result.msg = "ok"        
    return result
