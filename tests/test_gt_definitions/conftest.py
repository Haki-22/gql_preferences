import logging
import datetime
import pytest_asyncio
import uuid

@pytest_asyncio.fixture
async def GQLInsertQueries():
    result = {
        "preference_settings": {
            "create": """
              mutation ($name: String!, $preferenceSettingsTypeId: UUID!) {
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
            "read": """query($id: UUID!){ result: preferenceSettingsById(id: $id) { id }}""",
},
        "preference_settings_types": {"create": """
            mutation ($name: String!) {
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
            "read": """query($id: UUID!){ result: preferenceSettingsTypeById(id: $id) { id }}""",
},
#        "preferedtagentities":{"create": """
#mutation {
#        preferenceTagAddToEntity(
#            tagData: {entityId: "2d9dcd22-a4a2-11ed-b9df-0242ac120003", entityTypeId: "2d3d9801-0017-4cf2-9272-2df7b59da667", tagId: "8148fd61-77b3-45d1-a382-ca3aadafb9a1"}
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
#        }""",
#            "read": """query($id: UUID!){ result: formPartById(id: $id) { id }}""",
#},
#        "formitems": {"create": """
#mutation ($id: UUID!, $name: String!, $order: Int!, $name_en: String!, $part_id: UUID!) {
#  formItemInsert(
#    item: {id: $id, name: $name, order: $order, nameEn: $name_en, partId: $part_id}
#  ) {
#    id
#    msg
#  }
#}""",
#            "read": """query($id: UUID!){ result: formItemById(id: $id) { id }}""",
#},
#        "formrequests": {"create": """
#mutation ($id: UUID!, $name: String!) {
#  formRequestInsert(
#    request: {id: $id, name:$name }
#  ) {
#    id
#    msg
#  }
#}""",
#            "read": """query($id: UUID!){ result: requestById(id: $id) { id }}""",
#},
#        "formhistories": {"create": """
#mutation ($id: UUID!, $name: String!, $form_id: UUID!, $request_id: UUID!) {
#  formHistoryInsert(
#    history: {id: $id, name:$name, requestId: $request_id, formId: $form_id}
#  ) {
#    id
#    msg
#  }
#}""",
#            "read": """query($id: UUID!){ result: formHistoryById(id: $id) { id }}""",
#},
#
    }
    
    return result


@pytest_asyncio.fixture
async def FillDataViaGQL(DemoData, GQLInsertQueries, ClientExecutorAdmin):
    types = [type(""), type(datetime.datetime.now()), type(uuid.uuid1())]
    for tablename, queryset in GQLInsertQueries.items():
        table = DemoData.get(tablename, None)
        assert table is not None, f"{tablename} is missing in DemoData"

        for row in table:
            variable_values = {}
            for key, value in row.items():
                variable_values[key] = value
                if isinstance(value, datetime.datetime):
                    variable_values[key] = value.isoformat()
                elif type(value) in types:
                    variable_values[key] = f"{value}"

            readResponse = await ClientExecutorAdmin(query=queryset["read"], variable_values=variable_values)
            if readResponse["data"]["result"] is not None:
                logging.info(f"row with id `{variable_values['id']}` already exists in `{tablename}`")
                continue
            insertResponse = await ClientExecutorAdmin(query=queryset["create"], variable_values=variable_values)
            assert insertResponse.get("errors", None) is None, insertResponse
        logging.info(f"{tablename} initialized via gql query")
    logging.info(f"All WANTED tables are initialized")