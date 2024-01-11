import pytest


from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)


test_reference_preference_settings = createResolveReferenceTest(tableName='preference_settings', gqltype='PreferenceSettingsGQLModel', attributeNames=["id", "name", "lastchange", "createdby {id}","changedby {id}", "nameEn"])

test_query_preference_settings_by_id = createByIdTest(tableName="preference_settings", queryEndpoint="preferenceSettingsById")
test_query_preference_settings_page = createPageTest(tableName="preference_settings", queryEndpoint="preferenceSettingsPage")

#####################################################################
#
# Create
#
#####################################################################

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
                    created
                    createdby {
                        id
                    }
                    nameEn
                    order
                    preferenceSettingsTypeId
                    changedby {
                        id
                    }
                    type {
                        id
                    }
                }
            }
        }""",
    variables={"preferenceSettingsTypeId": "89838aab-d06e-445e-9a2e-d3c55bc7cb90", "name": "new preference setting"}
)

#####################################################################
#
# Update
#
#####################################################################

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

#####################################################################
#
# expected failures
#
#####################################################################

test_insert_preference_settings_with_existing_name = createFrontendQuery(
    query="""mutation ($name: String!, $preferenceSettingsTypeId: UUID!) {
        result:   preferenceSettingsInsert(
            preferenceSettings: {name: $name, preferenceSettingsTypeId: $preferenceSettingsTypeId})
            {
                msg
                id
            }
        }""",
    variables={"preferenceSettingsTypeId": "89838aab-d06e-445e-9a2e-d3c55bc7cb90", "name": "Zapnute"}
)

#### Cant get to make it go through line 247, even the msg is "fail"
# Create update query wasnt meant to be testing expected failitues
# 

#test_update_preference_settings_fail = createUpdateQuery(
#    query="""mutation ($id: UUID!, $lastchange: DateTime!) {
#        result: preferenceSettingsUpdate(
#            preferenceSettings: {id: $id, lastchange: $lastchange})
#             {
#                id
#                msg
#                preferenceSettings {
#                    id
#                    }
#            }
#    }""",
#    variables={"id": "928a8aab-d06e-445e-982e-d3c55bc7cb90"},
#    tableName="preference_settings"
#)

#####################################################################
#
# Delete
#
#####################################################################

test_delete_preference_settings = createUpdateQuery(
    query="""

        mutation ($id: UUID!, $lastchange: DateTime!) {
            result: preferenceSettingsDelete(
            preferenceSettings: {id: $id, lastchange: $lastchange})
            {
                id
                msg
                preferenceSettings {
                    id
                    }
            }
        }""",
        variables={"id":"928a8aab-d06e-445e-982e-d3c55bc7cb90"},
        tableName="preference_settings"
)

