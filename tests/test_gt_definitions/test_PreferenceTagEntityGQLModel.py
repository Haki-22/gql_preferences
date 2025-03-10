import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery,
    createDeleteQuery
)

test_preference_tag_etntity = createResolveReferenceTest(tableName='preferedtagentities', gqltype='PreferenceTagEntityGQLModel', attributeNames=["id", "lastchange"])

#####################################################################
#
# Specials
#
#####################################################################

#Entities labeled by tags + externals
test_preference_tag_etntities_labeled = createFrontendQuery(
    query="""
        query ($tags: [UUID!]!) {
            preferenceEntitiesLabeled(tags: $tags) {
                ... on UserGQLModel {
                id
                preferenceTagsForEntity {
                    id
                    }
                preferenceSettingsUserPage {
                    id
                    }
                }
                ... on GroupGQLModel {
                id
                }
                ... on EventGQLModel {
                id
                }
                ... on FacilityGQLModel {
                id
                }
            }
        }""",

        variables={"tags": ["8148fd61-77b3-45d1-a382-ca3aadafb9a1", "7a4c0d3e-2e3a-4ea0-9037-baa38d8400d2"]}
)


#Hardwired IDS for types of entities
test_preference_entity_types = createFrontendQuery(
    query="""
        query  {
            preferenceEntityTypes {
                modelId
                modelName
            }
        }"""
)

## Entities with this tag
test_preference_entitties_associated_with_tag = createFrontendQuery(
    query="""
        query  {
            preferenceTagsForEntity(entityId: "2d9dcd22-a4a2-11ed-b9df-0242ac120003") {
                created
                entities {
                    ... on UserGQLModel {
                        id
                    }
                    ... on GroupGQLModel {
                        id
                    }
                }
                entityTypeId
                id
                lastchange
                tag {
                    created
                    id
                    lastchange
                    name
                    nameEn
                    links {
                        id
                        created
                        createdby {
                            id
                        }
                    }
                }
            }
        }"""
)

#####################################################################
#
# Create
#
#####################################################################
##Add tag to entity
test_preference_tag_add_to_entity = createFrontendQuery(
    query="""
        mutation {
        preferenceTagAddToEntity(
            tagData: {entityId: "2d9dcd22-a4a2-11ed-b9df-0242ac120003", entityTypeId: "2d3d9801-0017-4cf2-9272-2df7b59da667", tagId: "8148fd61-77b3-45d1-a382-ca3aadafb9a1"}
        ) {
            id
            msg
            tag {
            created
            id
            entities {
                ... on UserGQLModel {
                id
                }
                ... on GroupGQLModel {
                id
                }
            }
            }
        }
        }

"""
)

#####################################################################
#
# expected failures
#
#####################################################################

#266-267 fail msg
#test_preference_tag_add_to_entity_fail = createFrontendQuery(
#    query="""
#        mutation {
#        preferenceTagAddToEntity(
#            tagData: {entityId: "2d9dcd22-a4a2-11ed-b9df-0242ac120003", entityTypeId: "2d3d9801-0017-4cf2-9272-2df7b59da667", tagId: "8148fd51-77b3-45d1-a382-ca3aadafb9a1"}
#        ) {
#            id
#            msg
#            tag {
#            created
#            id
#            entities {
#                ... on UserGQLModel {
#                id
#                }
#                ... on GroupGQLModel {
#                id
#                }
#            }
#            }
#        }
#        }
#
#"""
#)

test_preference_tag_add_to_entity_fail_already_exists = createFrontendQuery(
    query="""
        mutation {
        preferenceTagAddToEntity(
            tagData: {entityId: "2d9dc868-a4a2-11ed-b9df-0242ac120003", entityTypeId: "e8479a21-b7c4-4140-9562-217de2656d55", tagId: "8148fd61-77b3-45d1-a382-ca3aadafb9a1"}
        ) {
            id
            msg
            }
        }""")

#Remove tag from entity by ID fil bcs of bad id
test_preference_tag_remove_from_entity_fail = createFrontendQuery(
    query="""
        mutation {
            preferenceTagRemoveFromEntity(tagData: {id: "11838aab-d06e-445e-9a2e-d3c55bc7cb11"}) 
                {
                    id
                    msg
                }
    }
"""
)


#####################################################################
#
# Delete
#
#####################################################################

#Remove tag from entity by ID
test_preference_tag_remove_from_entity = createFrontendQuery(
    query="""
        mutation {
            preferenceTagRemoveFromEntity(tagData: {id: "2f22d834-5d74-4746-86f8-09f2989dc6a7"}) 
                {
                    id
                    msg
                }
    }
"""
)

#test_preference_tag_remove_from_entity = createDeleteQuery(tableName="preferedtagentities", queryBase="preferenceTag", id="2f22d834-5d74-4746-86f8-09f2989dc6a7")


#test_query_tag_by_id = createByIdTest(tableName="preferedtagentities", queryEndpoint="preferenceTagById")
#test_query_tag_page = createPageTest(tableName="preferedtagentities", queryEndpoint="preferenceTagsPage")

#test_tag_insert = createFrontendQuery(query="""
#    mutation($name: String!) { 
#        result: preferenceTagInsert(tag: {name: $name}) { 
#            id
#            msg
#            tag {
#                id
#                name
#            }
#        }
#    }
#    """, 
#    variables={"name": "new tag"}
#)


#test_item_update = createUpdateQuery(
#    query="""
#        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
#            preferenceTagUpdate(tag: {id: $id, name: $name, lastchange: $lastchange}) {
#                id
#                msg
#                tag {
#                    id
#                    name
#                    lastchange
#                }
#            }
#        }
#
#    """,
#    variables={"id": "7a4c203e-2e3a-4ea0-9037-baa38d8400d2", "name": "new name"},
#    tableName="preferedtagentities"
#)

