import strawberry

@strawberry.type
class Mutation:
    
    from .TagGQLModel import tag_insert
    tag_insert = tag_insert

    from .TagGQLModel import tag_update
    tag_update = tag_update

    from .TagGQLModel import tag_delete
    tag_delete = tag_delete

    from .TagEntityGQLModel import tag_add_to_entity
    tag_add_to_entity = tag_add_to_entity

    from .TagEntityGQLModel import tag_remove_from_entity
    tag_remove_from_entity = tag_remove_from_entity
    pass