## backend python deník

### till 26.10.

Github fork

Virtual environment (venv) 

### till 26.11.

gql_evolution

PgAdmin

Code understanding

SearchById

### till 3.12.

- change to versions (requirements)

- changes to dbfeeder (get_demodata)

- getLoaders moved to dataloaders

- PreferenceSettings (Types)

- Query:
```
query PSQuery {
 preferenceSettingsTypePage {
    id
    name
    nameEn
    preferenceSettings {
      id
      name
      nameEn
      lastchange
      order
    }
    lastchange
    order
  }
}

 ```
- Mutation:
```
mutation PSTInsert {
  preferenceSettingsTypeInsert(preferenceSettingsType: {name: "Typ"}) {
    id
    msg
  }
}
 ```


- Copy of GraphResolvers, BaeGQLMode, utils (where), RBCAObject

### till 8.12.

- PreferenceEntityTags

- PreferenceTags

- Settings as a user preference, default is set in frontend

- fixed entities on external models (UserGQLModel, GroupGQLModel, EventGQLModel, FacilityGQLModel)

### 8.12.

- exxternals.py:

  - Page of tags for entity in external models

  - Specific settings for a user added to User external group

- all strawberry.id changed to UUID

- added another tag entity to systemdata.json -> preference_entities_labeled works

- Every name set to Preference... for easier search in GraphiQL when implemented with others

- links work

### 11.12.

docker [image](https://hub.docker.com/repository/docker/haki22/gql-preferences/general)


### 6-7.1.24

- unsuccessfully tried pytests

  ```
  FAILED tests/test_gt_definitions/test_PreferenceSettingsDBModel.py::test_reference_preference_settings - AssertionError: [GraphQLError("'all'", locations=[SourceLocation(line=1, column=23)], path=['_entities', 0])]  
  ```

  Might be because of bad data loader ("all") or bad written pytest

- Moved and changed Dataloaders, DBFeeder to utils, copied gql_ug_proxy

- changed:
  ```
  from. uuid import UUIDFKey, UUIDColumn
  ```
  to
  ```
  from .uuid import UUIDFKey, UUIDColumn
  ```

- can't resolve

  ```
  from uoishelpers.authenticationMiddleware import createAuthentizationSentinel
  ```

- Changed versions in requirements

### 9.1.

- Added RBACObject to mutations (CRUD)   
  ```
  rbacobject: strawberry.Private[UUID] = None 
  ```


### 10.1.

- changed whole main.py to newer version from hrbolek/gql/forms

- Changed DataLoaders to be predefined one by one instead of lambda function

- Started pytesting 
  
  ```
  pytest --cov-report term-missing --cov=DBDefinitions --cov=GraphTypeDefinitions --cov=utils  --log-cli-level=INFO -x
  ```

- Changed systamdata.json, preferencesettings and tags to follow new default user (John Newbie, 2d9dc5ca-a4a2-11ed-b9df-0242ac120003)

- Fixed PreferenceTagEntityGQL -> preference_entities_labeled -> because of changed main and now  asyncSessionMaker = info.context["asyncSessionMaker"] is invalid

- Changed actingUser["id"] to UUID(actingUser["id"])

- Pytest up to  74%


### 11.1.

- Added permission_classes=[OnlyForAuthentized()] to all queries and strawberry fields (GQLModels and _GraphResolvers) (- rbacobject to what all queries)

### 12.1.

- Added None to result GQL model (for delete) Union[GQLModel, None]

- Changed User Settings to delete the entry if the udpate is to default one

- Changed whole structure (removed gql_preferences folder and moved files to root for pytests)

- Imported authentication middleware from uois helpers

- More pytests, 

  - missing authorizations and expected failiures that require lastchange:

 ```
  ==================================================================================== warnings summary ==================================================================================== 
  .venv\lib\site-packages\strawberry\types\fields\resolver.py:229
    gql_preferences\.venv\lib\site-packages\strawberry\types\fields\resolver.py:229: DeprecationWarning: Argument name-based matching of 'info' is deprecated and will 
  be removed in v1.0. Ensure that reserved arguments are annotated their respective types (i.e. use value: 'DirectiveValue[str]' instead of 'value: str' and 'info: Info' instead of a plain 
  'info').
      return {spec: spec.find(parameters, self) for spec in self.RESERVED_PARAMSPEC}

  tests/test_gt_definitions/test_PreferenceSettingsGQLModel.py: 9 warnings
  tests/test_gt_definitions/test_PreferenceSettingsTypeGQLModel.py: 10 warnings
  tests/test_gt_definitions/test_PreferenceTagEntityGQLModel.py: 7 warnings
  tests/test_gt_definitions/test_PreferenceTagGQLModel.py: 9 warnings
  tests/test_gt_definitions/test_PreferenceUserSettingsGQLModel.py: 10 warnings
  tests/test_gt_definitions/test__permisions.py: 4 warnings
    gql_preferences\.venv\lib\site-packages\pytest_asyncio\plugin.py:884: DeprecationWarning: There is no current event loop
      _loop = asyncio.get_event_loop()

  -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

  ---------- coverage: platform win32, python 3.10.5-final-0 -----------
  Name                                                     Stmts   Miss  Cover   Missing
  --------------------------------------------------------------------------------------
  DBDefinitions\Base.py                                       35     18    49%   20-30, 42-50
  DBDefinitions\PreferenceSettingsDBModel.py                  19      0   100%
  DBDefinitions\PreferenceSettingsTypeDBModel.py              18      0   100%
  DBDefinitions\PreferenceTagDBModel.py                       15      0   100%
  DBDefinitions\PreferenceTagEntityDBModel.py                 16      0   100%
  DBDefinitions\PreferenceUserSettingsDBModel.py              18      0   100%
  DBDefinitions\__init__.py                                    6      0   100%
  DBDefinitions\uuid.py                                        6      0   100%
  GraphTypeDefinitions\BaseGQLModel.py                        19      1    95%   9
  GraphTypeDefinitions\PreferenceSettingsGQLModel.py         119      4    97%   260, 267-270
  GraphTypeDefinitions\PreferenceSettingsTypeGQLModel.py     132      7    95%   280-289
  GraphTypeDefinitions\PreferenceTagEntityGQLModel.py        141      2    99%   266-267
  GraphTypeDefinitions\PreferenceTagGQLModel.py              116      1    99%   185
  GraphTypeDefinitions\PreferenceUserSettingsGQLModel.py     131      3    98%   288, 295-297
  GraphTypeDefinitions\_GraphPermissions.py                   92     52    43%   44, 191-205, 208, 270-273, 294-295, 300, 311, 317-385
  GraphTypeDefinitions\_GraphResolvers.py                     51      2    96%   280-281
  GraphTypeDefinitions\_RBACObjectGQLModel.py                 13      3    77%   14-16
  GraphTypeDefinitions\__init__.py                             5      0   100%
  GraphTypeDefinitions\externals.py                           39      1    97%   13
  GraphTypeDefinitions\mutation.py                            18      0   100%
  GraphTypeDefinitions\query.py                               20      0   100%
  GraphTypeDefinitions\utils.py                              106      7    93%   30-38
  utils\DBFeeder.py                                           40      5    88%   29, 34-36, 61
  utils\Dataloaders.py                                       129     50    61%   151-155, 167-171, 174, 177-212, 217-222, 344, 413-414, 461-464, 469-471
  utils\gql_ug_proxy.py                                       38      8    79%   29-31, 39-42, 55
  utils\sentinel.py                                            8      0   100%
  --------------------------------------------------------------------------------------
  TOTAL                                                     1350    164    88%

  ====================================================================== 49 passed, 50 warnings in 206.70s (0:03:26) ======================================================================= 
  ```

---

## Notes

 `uvicorn main:app --reload `

- Bash:

    `python3 -m venv .venv`

    `source .venv/bin/activate`

- Windows
 
    `source .venv/bin/activate.ps1`


- Docker:

  POSTGRES_HOST : host.docker.internal:5432

- Specific Pytest:

   ```
  pytest --cov-report term-missing --cov=DBDefinitions --cov=GraphTypeDefinitions --cov=utils  --log-cli-level=INFO -x .\tests\test_gt_definitions\test_PreferenceUserSettingsGQLModel.py::test_update_preference_settings_type
  ```

---

## TODO

Pretify code (Unify)

  - PreferenceTagEntityGQL -> preference_entities_labeled

  - Comment code

tests:

  - Fail tests missing when they need lastchange (updates) (CreateUpdateQuery isnt meant to check for failiures)

  - Authorized tests missing

Fronted loads into default and should search for user specific user settings if there are some -> apply them.

Use the same entity resolution? (return whole enitty not just ID)  (PreferenceTagEntityGQLModel)

  - Whole GQL model for EntityTypes? 
  
  @strawberry.field(description="Retrieves the entity_type_id ") 
    def entity_type_id(self) -> UUID:
        return self.entity_type_id

- Map all groups, events, users, facilities to existing data? (GraphTypeDefinitions/PreferenceTagEntityGQLModel)

```
# Dictionary mapping entity type IDs to corresponding classes
entity_type_ids = {                                                 #Identify all
    UUID("e8479a21-b7c4-4140-9562-217de2656d55"): UserGQLModel,     #users
    UUID("2d3d9801-0017-4cf2-9272-2df7b59da667"): GroupGQLModel,    #Groups
    UUID("a7457888-ed8a-4720-b116-13558cd7963b"): EventGQLModel,    #Events
    UUID("9feb8037-6c62-45bb-ac20-916763731f5d"): FacilityGQLModel  #Facilities
}
```

- Change where filter to ingore UPPER / lower case

## ?

Při updatu Preference Settings, neměla by nastat změna lastchange u Preference Settings Type?

Result entity?

name_en u tagů? Nebo si jména vytváří user?

filter_by nejde pouzit s ARRAY, porovnana ID=ID PreferenceSettingsGQLModel -> user_settings_page

Pokud nenajde user settings -> default settings?

## Zadání:

PREFERENCES

Entity (TagGQLModel, TagTypeGQLModel)

Entity (PreferenceSettingsGQLModel)

Modely v databázi pomocí SQLAlchemy, API endpoint typu GraphQL s pomocí knihovny Strawberry.

Přístup k databázi řešte důsledně přes AioDataloder, resp. (https://github.com/hrbolek/uoishelpers/blob/main/uoishelpers/dataloaders.py).

Zabezpečte kompletní CRUD operace nad entitami ExternalIdModel, ExternalIdTypeModel, ExternalIdCategoryModel

CUD operace jako návratový typ nejméně se třemi prvky id, msg a „entityresult“ (pojmenujte adekvátně podle dotčené entity), vhodné přidat možnost nadřízené entity, speciálně pro operaci D.

Řešte autorizaci operací (permission classes).

Kompletní CRUD dotazy na GQL v souboru externalids_queries.json (dictionary), jméno klíče nechť vhodně identifikuje operaci, hodnota je dictionary s klíči query (obsahuje parametrický dotaz) nebo mutation (obsahuje parametrické mutation) a variables (obsahuje dictionary jako testovací hodnoty).

Kompletní popisy API v kódu (description u GQLModelů) a popisy DB vrstvy (comment u DBModelů).

Zabezpečte více jak 90% code test coverage (standard pytest).
