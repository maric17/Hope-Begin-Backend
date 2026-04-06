# API Response Standard

To ensure a consistent experience for frontend integration (especially with NextAuth and React Query), all API endpoints follow a standardized JSON structure.

## Structure

```json
{
  "status": true,
  "message": "success",
  "data": []
}
```


### Fields

- **`status`** (boolean): 
  - `true`: Request was successful (2xx range).
  - `false`: Request failed (4xx or 5xx range).
- **`message`** (string): 
  - A short, human-readable description of the result (e.g., "Login successful", "Validation failed").
- **`data`** (any): 
  - The actual payload. For lists, this is an `array`. For single objects, it's a `dict`. For errors, this contains the detailed error messages.

---

## Example Success (Login)

**Status Code:** `200 OK`

```json
{
  "status": true,
  "message": "success",
  "data": {
    "access": "...",
    "user": { "email": "user@example.com", "role": "admin" }
  }
}
```

## Example Success (Logout)

**Status Code:** `205 Reset Content`

```json
{
  "status": true,
  "message": "Logged out successfully.",
  "data": null
}
```

## Example Error (Validation)

**Status Code:** `400 Bad Request`

```json
{
  "status": false,
  "message": "Bad Request",
  "data": {
    "email": ["User with this email already exists."]
  }
}
```
