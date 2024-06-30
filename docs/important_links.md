# Important Links API
## Link Types and Link Category Types
There are two types of data associated with the important links API, one is LinkT which describes the link data and the other is LinkCategoryT which describes the link's category
```ts
type LinkT = {
  title : string,
  url : string,
  description : string,
  category : number, // Primary Key for Category
  is_english : boolean
  requires_sso : boolean
  external_access : boolean
  id : number
}

type CategoryT = {
  title_category : string
  title_slug : string
  id : number k
}
```

## Getting all Important Links (or Filtered)
- Endpoint : `api/important_links`
- Query Parameters : TBD
- Request : GET
- Response :
```ts
LinkT[]
```

## Getting all Categories (or Filtered)
- Endpoint : `api/important_links/category`
- Query Parameters :TBD
- Request : GET
- Response :
```ts
CategoryT[]
```

<!--
### Tip
- To get the information of a single category given the primary key of the category perform the following query :
```ts
{
  endpoint : `api/important_links/category?id=${categoryId}`
}
```
the above query will return one single category containing the category specified by the primary key `categoryId`

- To filter by category name the following query can be done
```ts
{
  endpoint : `api/important_links/category?title_category__startswith=${some_string}`
}
``` -->
