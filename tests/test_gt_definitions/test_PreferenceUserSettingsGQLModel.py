import pytest


from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery,
    createDeleteQuery
)


test_reference_preference_user_settings = createResolveReferenceTest(tableName='user_settings', gqltype='PreferenceUserSettingsGQLModel', attributeNames=["id", "lastchange","changedby {id}", "created"])

#test_query_preference_settings_by_id = createByIdTest(tableName="user_settings", queryEndpoint="preferenceSettingsById")
 #= createPageTest(tableName="user_settings", queryEndpoint="preferenceSettingsUserPage")

test_query_preference_settings_user_page = createFrontendQuery(
    query="""
     query {
        preferenceSettingsUserPage {
            created
            id
            lastchange
            changedby {
                id
            }
            preferenceSettingsId {
                id
                name
            }
            preferenceSettingsTypeId {
                id
                name
            }
            rbacobject {
                id
            }
            userId {
                id
            }
        }
    }"""
)


test_query_preference_settings_user_in_a_type = createFrontendQuery(
    query="""
     query {
        preferenceSettingsUserInType(
            preferenceSettingsTypeId: "89838aab-d06e-445e-9a2e-d3c55bc7cb90"
        ) {
            created
            id
            preferenceSettingsId {
                id
                name
            }
            preferenceSettingsTypeId {
                id
                name
            }
        }
    }
"""
)

#####################################################################
#
# Create
#
#####################################################################

test_insert_preference_settings_for_user = createFrontendQuery(
    query="""
        mutation MyMutation {
        preferenceUserSettingsTypeInsert(
            userSettings: {preferenceSettingsId: "928a8aab-d06e-445e-982e-d3c55bc7cb91", preferenceSettingsTypeId: "89838aab-d06e-445e-982a-d3c55bc7cb90"}
        ) {
            id
            msg
            preferenceUserSettings {
            id
            preferenceSettingsId {
                name
            }
            preferenceSettingsTypeId {
                name
            }
            }
        }
    }"""
)

######################################################################
##
## Update
##
######################################################################

test_update_preference_settings_for_user_to_default = createFrontendQuery( 
    query="""
        mutation MyMutation {
            preferenceUserSettingsTypeUpdate(
                userSettings: {lastchange: "2024-01-12T12:08:31.595430", id: "11838aab-d06e-445e-9a2e-d3c55bc7cb11", preferenceSettingsId: "90838aab-d06e-445e-9a2e-d3c55bc7cb90"}
            ) {
                id
                msg
            }
        }""",
)

test_update_preference_settings_for_user = createUpdateQuery(
    query="""
        mutation ($id: UUID!, $lastchange: DateTime!, $preferenceSettingsTypeId: UUID, $preferenceSettingsId: UUID) {
        result: preferenceUserSettingsTypeUpdate(
                userSettings: {id: $id, lastchange: $lastchange, preferenceSettingsTypeId: $preferenceSettingsTypeId, preferenceSettingsId: $preferenceSettingsId}) {
                id
                msg
                preferenceUserSettings {
                    id
                }
            }
        }
    """,
    variables={"id": "11838aab-d06e-445e-9a2e-d3c55bc7cb11", "preferenceSettingsTypeId": "89838aab-d06e-445e-982a-d3c55bc7cb90", "preferenceSettingsId": "928a8aab-d06e-445e-982e-d3c55bc7cb90"},
    tableName="user_settings"
)


######################################################################
##
## expected failures
##
######################################################################
#
test_update_preference_settings_for_user_bad_id = createFrontendQuery( 
    query="""
            mutation MyMutation {
            preferenceUserSettingsTypeUpdate(
                userSettings: {preferenceSettingsTypeId: "89838aab-d06e-445e-982a-d3c55bc7cb90", preferenceSettingsId: "928a8aab-d06e-445e-982e-d3c55bc7cb90", lastchange: "2024-01-12T01:25:17.956662", id: "ffab3d50-b45f-4c3d-a6c7-5db99204cf88"}
            ) {
                id
                msg
            }
        }
""",
)

test_update_preference_settings_for_user_bad_lastchange = createFrontendQuery( 
    query="""
            mutation MyMutation {
            preferenceUserSettingsTypeUpdate(
                userSettings: {preferenceSettingsTypeId: "89838aab-d06e-445e-982a-d3c55bc7cb90", preferenceSettingsId: "928a8aab-d06e-445e-982e-d3c55bc7cb90", lastchange: "2024-01-12T01:25:17.956662", id: "11838aab-d06e-445e-9a2e-d3c55bc7cb11"}
            ) {
                id
                msg
            }
        }
""",
)

test_insert_preference_settings_for_user_already_existing = createFrontendQuery(
    query="""
        mutation MyMutation {
        preferenceUserSettingsTypeInsert(
            userSettings: {preferenceSettingsId: "928a8aab-d06e-445e-982e-d3c55bc7cb91", preferenceSettingsTypeId: "89838aab-d06e-445e-9a2e-d3c55bc7cb90"}
        ) {
            id
            msg
            }
    }"""
)

test_delete__preference_settings_for_user_fail_bad_id = createFrontendQuery(
    query="""

        mutation ($id: UUID!) {
            result: preferenceUserSettingsDelete(
            userSettings: {id: $id})
            {
                id
                msg
            }
        }""",
        variables={"id":"81838aab-d06e-445e-9a2e-d3c55bc7cb11"},
)
## Create update query wasnt meant to be testing expected failitues

#test_delete__preference_settings_for_user_fail_bad_id = createUpdateQuery(
#    query="""
#
#        mutation ($id: UUID!, $lastchange: DateTime!) {
#            result: preferenceUserSettingsDelete(
#            userSettings: {id: $id, lastchange: $lastchange})
#            {
#                id
#                msg
#                preferenceUserSettings{
#                    id
#                }
#                
#            }
#        }""",
#        variables={"id":"928a8aab-d06e-445e-982e-d3c55bc7cb91"},
#        tableName="user_settings"
#)

#
##### Cant get to make it go through line 247, even the msg is "fail"
## Create update query wasnt meant to be testing expected failitues
## 
#
##test_update_preference_settings_fail = createUpdateQuery(
##    query="""mutation ($id: UUID!, $lastchange: DateTime!) {
##        result: preferenceSettingsUpdate(
##            preferenceSettings: {id: $id, lastchange: $lastchange})
##             {
##                id
##                msg
##                preferenceSettings {
##                    id
##                    }
##            }
##    }""",
##    variables={"id": "928a8aab-d06e-445e-982e-d3c55bc7cb90"},
##    tableName="preference_settings"
##)
#
######################################################################
##
## Delete
##
######################################################################
#
test_delete__preference_settings_for_user = createFrontendQuery(
    query="""

        mutation ($id: UUID!) {
            result: preferenceUserSettingsDelete(
            userSettings: {id: $id})
            {
                id
                msg
            }
        }""",
        variables={"id":"11838aab-d06e-445e-9a2e-d3c55bc7cb11"},
)

#test_delete__preference_settings_for_user = createDeleteQuery(tableName="user_settings", queryBase="userSettings", id="11838aab-d06e-445e-9a2e-d3c55bc7cb11")
