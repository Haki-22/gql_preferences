import pytest


from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)


test_reference_preference_settings = createResolveReferenceTest(tableName='preference_settings', gqltype='PreferenceSettingsGQLModel', attributeNames=["id", "name", "lastchange"])

test_query_preference_settings_by_id = createByIdTest(tableName="preference_settings", queryEndpoint="preference_settings_by_id")
test_query_preference_settings_page = createPageTest(tableName="preference_settings", queryEndpoint="preference_settings_page")

test_insert_preference_settings = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!) {
        result:   preferenceSettingsInsert(
            preferenceSettings: {name: "new name", preferenceSettingsTypeId: ""})
            {
                msg
                id
                preferenceSettings {
                    name
                    lastchange
                    id
                }
            }
        }""",
    variables={"preferenceSettingsTypeId": "89838aab-d06e-445e-9a2e-d3c55bc7cb90", "name": "new preference setting"}
)

test_update_form_category = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: formCategoryUpdate(formCategory: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            category {
                id
                name
            }
        }
    }""",
    variables={"id": "37675bd4-afb0-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="formcategories"
)