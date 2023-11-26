import strawberry
@strawberry.type(description="""Root query""")
class Query:

    from .TagEntityGQLModel import preference_entities
    preference_entities = preference_entities
    
    from .TagGQLModel import preference_tags
    preference_tags = preference_tags
    
    from .TagEntityGQLModel import preference_entity_tags
    preference_entity_tags = preference_entity_tags

    from .TagGQLModel import tag_by_id
    tag_by_id = tag_by_id

    pass