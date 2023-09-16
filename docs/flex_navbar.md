# Flexible Navbar
Flexible Navigation bar is meant to be a navigation bar where its content can be changed easily from the backend by modifying the entries. In the frontend, the following data should be rendered into the corresponding navigation bar. First, the invidual entries :
```typescript
type GenericNavEntryT<T, U> = {
    type : T, data : U
}
type NavLinkT = GenericNavEntryT<"link", {
    href : string,
    text : string,
    style? : {
        hover? : HTMLStyle, normal? : HTMLStyle, active? : HTMLStyle
    }
}>
type NavDropdownT = GenericNavEntryT<"dropdown", {
  display : string, entries : NavLink[]
} >
```
The above details how the navigation bar should be rendered.
## GenericNavEntry
GenericNavEntry is a general type describing the data used to render the navigation bar. GenericNavEntry contains two fields, one is type while the other is data. The former details the type of the navigation entry while the latter details the data used to render the contents.

## NavLink
NavLink is the mainly used entry, it deflates into the following :
```typescript
type NavLinkT = {
    type : "link",
    data : {
        href : string,
        text : string,
        style? : {
            hover? : HTMLStyle, normal? : HTMLStyle, active? : HTMLStyle
        }
    }
}
```
The above should render to the following an `<a><a/>` tag with the correct configuration specified in the file.

## NavDropdown
NavDropdown specifies a dropdown from the navigation bar. The following shows the configuration of the dropdown when deflated.
```typescript
type NavDropdownT = {
    type : "dropdown"
    data : {
      display : string,
      entries : Array<NavLink>
    }
}
```
The above should render to a dropdown menu.

## NavEntry
Finally, a navigation bar entry can be described as a union between a link and a dropdown
```ts
type NavEntryT = NavLinkT | NavDropdownT
```
# API
## Getting all Navigation Bar Entries
- Endpoint : `api/misc/navbar/`
- Request : GET
- Response :
```ts
Array<NavEntryT>
```
