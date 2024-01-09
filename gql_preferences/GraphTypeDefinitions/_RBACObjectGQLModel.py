import strawberry
import uuid
from .externals import resolve_reference

from ..utils.Dataloaders import getLoaders

@strawberry.federation.type(extend=False, keys=["id"])
class RBACObjectGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    @classmethod
    async def resolve_roles(cls, info: strawberry.types.Info, id: uuid.UUID):
        loader = getLoaders(info).authorizations
        authorizedroles = await loader.load(id)
        return authorizedroles
        