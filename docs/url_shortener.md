# Url Shortener
This is perhaps one of the few APIs that require a POST request to be done. The following describes the pipeline :
## User visits `shorten/:url_name`
The webpage should parse the url for url_name with the `useParams()` hook and send a request to the backend for a corresponding longer url.
## User is Redirected to `longer url`
After receiving the data to the backend, the user should be redirected to the longer url.

## Backend APIs
### Getting a Shortened URL Entry
- Endpoint : `api/url_shortener`
- Request : POST
- Payload :
```ts
{
  ip_address : string // This corresponds to the ip_address of the user
}
```
- Response (If the requested url_name exists, otherwise 404)
```ts
string
```
