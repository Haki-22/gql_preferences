import pytest


from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)


test_reference_preference_settings = createResolveReferenceTest(tableName='preference_settings', gqltype='PreferenceSettingsGQLModel', attributeNames=["id", "name", "lastchange"])

test_query_preference_settings_by_id = createByIdTest(tableName="preference_settings", queryEndpoint="preferenceSettingsById")
test_query_preference_settings_page = createPageTest(tableName="preference_settings", queryEndpoint="preferenceSettingsPage")

test_insert_preference_settings = createFrontendQuery(
    query="""mutation ($name: String!, $preferenceSettingsTypeId: UUID!) {
        result:   preferenceSettingsInsert(
            preferenceSettings: {name: $name, preferenceSettingsTypeId: $preferenceSettingsTypeId})
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

test_update_preference_settings = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: preferenceSettingsUpdate(
            preferenceSettings: {id: $id, name: $name, lastchange: $lastchange})
             {
                id
                msg
                preferenceSettings {
                    id
                    name
                }
            }
    }""",
    variables={"id": "918a8aab-d06e-445e-982e-d3c55bc7cb91", "name": "updated name"},
    tableName="preference_settings"
)