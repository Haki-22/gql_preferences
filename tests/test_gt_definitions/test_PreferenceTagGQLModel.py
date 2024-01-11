import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_tag = createResolveReferenceTest(tableName='preferedtags', gqltype='PreferenceTagGQLModel', attributeNames=["id", "name", "lastchange"])

test_query_tag_by_id = createByIdTest(tableName="preferedtags", queryEndpoint="preferenceTagById")
test_query_tag_page = createPageTest(tableName="preferedtags", queryEndpoint="preferenceTagsPage")

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


test_item_update = createUpdateQuery(
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
