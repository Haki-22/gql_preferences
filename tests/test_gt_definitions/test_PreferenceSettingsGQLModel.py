import pytest


from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery,
    createDeleteQuery
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

test_update_preference_settings_fail = createFrontendQuery(
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
    variables={"id": "918a8aab-d06e-445e-982e-d3c55bc7cb91", "name": "updated name", "lastchange": "2024-01-12T14:32:19.259899"},
)

# 260, doesnt work?
test_delete_preference_settings_fail_bad_id = createFrontendQuery(
    query="""mutation ($id: UUID!) {
        result: preferenceSettingsDelete(
            preferenceSettings: {id: $id})
             {
                id
                msg
            }
    }""",
    variables={"id": "958a8aab-d06e-445e-982e-d3c55bc7cb91"},
)

#####################################################################
#
# Delete
#
#####################################################################

#test_delete_preference_settings = createFrontendQuery(
#    query="""
#        mutation ($id: UUID!, $lastchange: DateTime!) {
#            preferenceSettingsDelete(preferenceSettings: {id: $id, lastchange: $lastchange}) {
#                id
#                msg
#            }
#        }""",
#        variables={"id":"928a8aab-d06e-445e-982e-d3c55bc7cb90", "lastchange": "2024-02-07T08:17:10.955338"},
#
#)

test_delete_preference_settings = createDeleteQuery(tableName="preference_settings", queryBase="preferenceSettings", id="928a8aab-d06e-445e-982e-d3c55bc7cb90")
