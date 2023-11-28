## backend python deník

### till 26.10.

Github fork

Virtual environment (venv) 

### till 26.11.

gql_evolution

PgAdmin

Code understanding

SearchById

---

- Query:
```python
{
  tagById(id: "8148fd61-77b3-45d1-a382-ca3aadafb9a1") {
    id
    name
  }
}
 ```
- Mutation:
```python
mutation {
  tagInsert(tag: { name: "Ahoj" }) {
    tag {
      name
    }
  }
}
 ```

---

## Notes

 `uvicorn main:app --reload `

- Bash:

    `python3 -m venv .venv`

    `source .venv/bin/activate`

- Windows
 
    `source .venv/bin/activate.ps1`

---

## ?

TagType?  PreferenceSettings?

TagTypeGQLModel: Co je TagType?, systemdata.json:
 - preferedtags

 - preferedtagentities

External ID? - externals.py

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