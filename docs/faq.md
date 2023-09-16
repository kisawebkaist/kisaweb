# FAQ API
## Types
```ts
type FaqT = {
  question : string
  timestamp : string // Datetime string
  category : number // Primary Key
  answer : string
  id : number
}

type CategoryT = {
  title_category : string
  title_slug : string
  id : number
}
```


## Getting all FAQs (or Filtered)
- Endpoint : `api/faq`
- Query Parameters : All Fields in FaqT including linking fields by category__title_category
- Request : GET
- Response :
```ts
FaqT[]
```

## Getting all Categories (or Filtered)
- Endpoint : `api/faq/category`
- Query Parameters : All Fields in CategoryT (Filters based on the parameters)
- Request : GET
- Response :
```ts
CategoryT[]
```


### Tip
- To get the information of a single category given the primary key of the category perform the following query :
```ts
{
  endpoint : `api/faq/category?id=${categoryId}`
}
```
the above query will return one single category containing the category specified by the primary key `categoryId`

- To filter by category name the following query can be done
```ts
{
  endpoint : `api/faq/category?title_category__startswith=${some_string}`
}
```


