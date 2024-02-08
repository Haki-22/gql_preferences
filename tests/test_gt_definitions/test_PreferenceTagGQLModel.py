import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery,
    createDeleteQuery
)

test_reference_tag = createResolveReferenceTest(tableName='preferedtags', gqltype='PreferenceTagGQLModel', attributeNames=["id", "name", "lastchange"])

test_query_tag_by_id = createByIdTest(tableName="preferedtags", queryEndpoint="preferenceTagById")
test_query_tag_page = createPageTest(tableName="preferedtags", queryEndpoint="preferenceTagsPage")

#####################################################################
#
# Create
#
#####################################################################

test_tag_insert = createFrontendQuery(query="""
    mutation($name: String!) { 
        result: preferenceTagInsert(tag: {name: $name}) { 
            id
            msg
            tag {
                id
                name
            }
        }
    }
    """, 
    variables={"name": "new tag"}
)

#####################################################################
#
# Update
#
#####################################################################

test_tag_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            preferenceTagUpdate(tag: {id: $id, name: $name, lastchange: $lastchange}) {
                id
                msg
                tag {
                    id
                    name
                    lastchange
                }
            }
        }

    """,
    variables={"id": "7a4c203e-2e3a-4ea0-9037-baa38d8400d2", "name": "new name"},
    tableName="preferedtags"
)

#####################################################################
#
# Specials
#
#####################################################################

####Tags associated with asking user
test_tag_associated_with_user = createFrontendQuery(
    query="""
     query {
        preferenceTags {
            authorId {
                id
            }
            changedby {
                id
            }
            created
            createdby {
                id
            }
            id
            lastchange
            name
            nameEn
        }
    }"""
)

#####################################################################
#
# Delete
#
#####################################################################

#Remove tag
test_preference_tag_remove = createFrontendQuery(
    query="""
        mutation {
            preferenceTagDelete(tag: {id: "7a4c203e-2e3a-4ea0-9037-baa38d8400d2"}) {
                id
                msg
            }
        }
"""
)

#test_preference_tag_remove = createDeleteQuery(tableName="preferedtags", queryBase="preferenceTags", id="7a4c203e-2e3a-4ea0-9037-baa38d8400d2")


#####################################################################
#
# expected failures
#
#####################################################################

#Fail name already exists
test_tag_insert_fail = createFrontendQuery(query="""
    mutation($name: String!) { 
        result: preferenceTagInsert(tag: {name: $name}) { 
            id
            msg
            tag {
                id
                name
            }
        }
    }
    """, 
    variables={"name": "red"}
)


#Remove tag - Fail bad ID
test_preference_tag_remove_fail = createFrontendQuery(
    query="""
        mutation {
            preferenceTagDelete(tag: {id: "11838aab-d06e-445e-9a2e-d3c55bc7cb11"}) {
                id
                msg
            }
        }
"""
)
