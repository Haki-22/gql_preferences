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

- Bash
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