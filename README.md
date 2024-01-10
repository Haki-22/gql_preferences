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
  pytest --cov-report term-missing --cov=gql_preferences.DBDefinitions --cov=gql_preferences.GraphTypeDefinitions --cov=gql_preferences.utils  --log-cli-level=INFO -x
  ```

- Changed systamdata.json, preferencesettings and tags to follow new default user (John Newbie, 2d9dc5ca-a4a2-11ed-b9df-0242ac120003)

---

## Notes

 `uvicorn main:app --reload `

- Bash:

    `python3 -m venv .venv`

    `source .venv/bin/activate`

- Windows
 
    `source .venv/bin/activate.ps1`

---

## TODO

Pretify code (Unify)

Docker image

tests

- rbacobject to what queries?

Fronted loads into default and should search for user specific user settings if there are some -> apply them.

#### Use the same entity resolution? (return whole enitty not just ID)  (PreferenceTagEntityGQLModel)

- Whole GQL model for EntityTypes? 
 
@strawberry.field(description="Retrieves the entity_type_id ") 
  def entity_type_id(self) -> UUID:
      return self.entity_type_id

- Check Mutations

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

TagType - je v GraphTypeDefinitions/TaEntityGQLModel.entity_type_ids  

Při updatu Preference Settings, neměla by nastat změna lastchange u Preference Settings Type?

Result entity?

name_en u tagů? Nebo si jména vytváří user?


```
query MyQuery {
  defaultPreferenceSettingsByTypeId(
    typeId: "90838aab-d06e-445e-9a2e-d3c55bc7cb90"
  ) {
    id
    name
    type {
      id
      name
      preferenceSettings {
        nameEn
        id
      }
    }
  }
}
```

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

