# OpenAPI Specification: Short Notes

## What is OpenAPI?

The **OpenAPI Specification (OAS)** is a standard format for describing an API in a clear, human-readable way.

It defines the contract between a client and a server, including:

- Available endpoints.
- HTTP methods.
- Request parameters.
- Response formats.
- Possible errors.
- Server details.

OpenAPI supports better API design, documentation, testing, and collaboration between developers.

## Main Sections

### 1. `openapi` and `info`

These sections describe basic API information.

```yaml
openapi: 3.0.0
info:
  title: Simple Pet Store
  version: 1.0.0
  description: A sample API for a pet store.
```

The `info` section may also include:

- Contact details.
- License information.
- Terms of service.
- API description.

### 2. `servers`

The `servers` section defines where the API is hosted.

```yaml
servers:
  - url: https://development.example.com/v1
    description: Development server
  - url: https://api.example.com/v1
    description: Production server
```

Multiple servers can be specified for development, staging, and production.

### 3. `paths`

The `paths` section lists the API endpoints and their HTTP methods.

```yaml
paths:
  /pets/{petId}:
    get:
      summary: Find a pet by ID
      responses:
        '200':
          description: Successful operation
        '404':
          description: Pet not found
```

It describes:

- Endpoint URLs.
- HTTP methods such as `GET` and `POST`.
- Request parameters.
- Responses.
- Error status codes.

## Types of Parameters

OpenAPI supports four common parameter types:

- **Path parameters:** `/users/{id}`
- **Query parameters:** `/users?role=admin`
- **Header parameters:** `X-MyHeader: Value`
- **Cookie parameters:** Values sent through the `Cookie` header.

### 4. External Documentation

The `externalDocs` section links to additional API information.

```yaml
externalDocs:
  description: Find more information
  url: https://example.com/docs
```

### 5. Tags

Tags group related API operations.

```yaml
tags:
  - name: pets
    description: Operations related to pets
```

This makes large APIs easier to navigate and understand.

### 6. Components

The `components` section stores reusable API definitions, such as:

- Schemas.
- Parameters.
- Responses.
- Examples.
- Security definitions.

Reusable components are referenced with `$ref`.

```yaml
components:
  schemas:
    Pet:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
```

## Key Benefits

- Creates a clear API contract.
- Improves communication between teams.
- Helps identify design problems early.
- Supports automatic documentation.
- Enables mock servers and client generation.
- Encourages consistent API design.
- Makes testing and integration easier.

## Final Idea

OpenAPI provides the rules for describing an API, but good API design depends on how clearly and effectively those rules are used.
