import pytest


from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery,
    createDeleteQuery
)


test_reference_preference_settings_type = createResolveReferenceTest(tableName='preference_settings_types', gqltype='PreferenceSettingsTypeGQLModel', attributeNames=["id", "name", "lastchange", "defaultPreferenceSettingsId"])

test_query_preference_settings_type_by_id = createByIdTest(tableName="preference_settings_types", queryEndpoint="preferenceSettingsTypeById")
test_query_preference_settings_type_page = createPageTest(tableName="preference_settings_types", queryEndpoint="preferenceSettingsTypePage")

#####################################################################
#
# Create
#
#####################################################################

test_insert_preference_settings_type = createFrontendQuery(
    query="""mutation ($name: String!) {
        result: preferenceSettingsTypeInsert(preferenceSettingsType: {name: $name}) {
            msg
            id
            preferenceSettingsType {
                name
                lastchange
                id
                created
                changedby {
                    id
                }
                createdby {
                    id
                }
                defaultPreferenceSettings {
                    id
                }
                nameEn
                order
                preferenceSettings {
                    id
                }
            }
        }
    }""",
    variables={"name": "new preference setting type"}
)

#####################################################################
#
# Update
#
#####################################################################

test_update_preference_settings_type = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: preferenceSettingsTypeUpdate(
            preferenceSettingsType: {id: $id, name: $name, lastchange: $lastchange})
             {
                id
                msg
                preferenceSettingsType {
                    id
                    name
                }
            }
    }""",
    variables={"id": "89838aab-d06e-445e-982a-d3c55bc7cb90", "name": "updated name"},
    tableName="preference_settings_types"
)

#####################################################################
#
# expected failures
#
#####################################################################

test_insert_preference_settings_type_with_existing_name = createFrontendQuery(
    query="""mutation ($name: String!) {
        result:   preferenceSettingsTypeInsert(
            preferenceSettingsType: {name: $name})
            {
                msg
                id
            }
        }""",
    variables={"name": "Jazyk"}
)

# Create update query wasnt meant to be testing expected failitues
# 

test_delete_preference_settings_type_bad_id = createFrontendQuery(
    query="""
        mutation ($id: UUID!) {
            result: preferenceSettingsTypeDelete(
            preferenceSettingsType: {id: $id})
            {
                id
                msg
            }
        }""",
        variables={"id":"789a8aab-d06e-445e-982e-d3c55bc7cb90"},
)

test_update_preference_settings_type_fail = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: preferenceSettingsTypeUpdate(
            preferenceSettingsType: {id: $id, name: $name, lastchange: $lastchange})
             {
                id
                msg
                preferenceSettingsType {
                    id
                    name
                }
            }
    }""",
    variables={"id": "89838aab-d06e-445e-982a-d3c55bc7cb90", "name": "updated name", "lastchange": "2024-01-12T16:53:59.454452"},
)

#####################################################################
#
# Delete
#
#####################################################################

#test_delete_preference_settings_type = createFrontendQuery(
#    query="""
#
#        mutation ($id: UUID!) {
#            result: preferenceSettingsTypeDelete(
#            preferenceSettingsType: {id: $id})
#            {
#                id
#                msg
#            }
#        }""",
#        variables={"id":"898a8aab-d06e-445e-982e-d3c55bc7cb90"}
#)


test_delete_preference_settings_type = createDeleteQuery(tableName="preference_settings_types", queryBase="preferenceSettingsType", id="898a8aab-d06e-445e-982e-d3c55bc7cb90")

#####################################################################
#
# Specials
#
#####################################################################

test_preference_settings_type_default_id = createFrontendQuery(
    query="""query ($id: UUID!) {
        preferenceSettingsDefaultByTypeId(id: $id) {
            id
            preferenceSettingsTypeId
            type {
                id
                name
            }
            name
        }
}""",
    variables={"id": "898a8aab-d06e-445e-982e-d3c55bc7cb90"}
)