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

11.12.

docker [image:](https://hub.docker.com/repository/docker/haki22/gql-preferences/general)

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

Fronted loads into default and should search for user specific user settings if there are some -> apply them.

#### Use the same entity resolution? (return whole enitty not just ID)  (PreferenceTagEntityGQLModel)

- Whole GQL model for EntityTypes? 
 
@strawberry.field(description="Retrieves the entity_type_id ") 
  def entity_type_id(self) -> UUID:
      return self.entity_type_id

- Check Mutations


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

