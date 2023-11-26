# Aboutus
## Data Types
There are several data types contained in the about us application. Most of the data are immutable and hence will mostly involve only a GET request.
```ts
type DivisionT = {
  division_name : string,
  id : number
}
type MemberT = {
  name : string
  image : string // Link to image basically the src
  year : string
  semester : string
  sns_link : string
  division : number // Division Primary Key
}
type InternalBoardMemberT = {
  name : string
  image : string // Link to image basically the src
  year : string
  semester : string
  sns_link : string
  position : string
  division : number
}

```

## Getting all Members
- Endpoint : `api/aboutus/members`
- Query Params : all fields in the response
- Request : GET
- Response :
```ts
MemberT[]
```

## Getting all Internal Members
- Endpoint : `api/aboutus/internal-members`
- Query Params : all fields in the response
- Request : GET
- Response :
```ts
InternalBoardMemberT[]
```

## Getting all Divisions
- Endpoint : `api/aboutus/divisions`
- Request : GET
- Response :
```ts
DivisionT[]
```
