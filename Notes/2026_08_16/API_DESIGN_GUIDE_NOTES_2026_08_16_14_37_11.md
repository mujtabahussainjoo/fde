# API Design Guide: Short Notes

## What Is API Design?

API design is the process of planning how an API will work before it is implemented.

It includes decisions about:

- Users and their needs.
- Resources and available data.
- Endpoints and operations.
- Request and response formats.
- Technology, security, and architecture.
- Documentation and maintenance.

API design is usually the first stage of the API development lifecycle.

## Why API Design Matters

Investing time in API design helps to:

- Reduce confusion during implementation.
- Avoid duplicated work.
- Support incremental development.
- Make documentation easier to create.
- Reduce integration errors and support requests.
- Create a better experience for API consumers.

## Characteristics of a Well-Designed API

A good API should be:

- **Easy to understand:** Resources and operations are clear and predictable.
- **Hard to misuse:** Requests and errors provide helpful feedback.
- **Complete but concise:** It provides the data users need without unnecessary complexity.
- **Well documented:** Endpoints, requests, responses, and features are explained clearly.
- **Reliable:** It remains available and changes are communicated properly.

## Main Parts of API Design

API design commonly focuses on:

1. Collections, resources, and URLs
2. Requests
3. Responses

## 1. Collections, Resources, and URLs

### Use Nouns in URLs

Use clear and consistent nouns to represent resources. Avoid putting actions such as `get` or `retrieve` in the URL.

```text
GET /photos       # Retrieve all photos
GET /photos/1     # Retrieve one photo
```

Choose either singular or plural resource names and use the same style throughout the API.

### Use HTTP Methods for Actions

HTTP methods describe what should happen to a resource.

| Method | Purpose | Example |
| --- | --- | --- |
| `GET` | Retrieve data | `GET /photos/1` |
| `POST` | Create data | `POST /photos` |
| `PUT` | Replace or update data | `PUT /photos/34` |
| `PATCH` | Partially update data | `PATCH /photos/4` |
| `DELETE` | Delete data | `DELETE /photos/12` |

Using standard HTTP methods makes API behavior easier to understand.

## 2. Requests

### Use Query Parameters for Flexible Requests

Query parameters can filter, search, sort, or limit returned data.

```text
GET /photos?location=boston&hashtag=winter&limit=10
```

This request gets up to 10 photos from Boston with the `winter` hashtag.

Good request design should:

- Return the data users need.
- Support relationships between resources.
- Avoid returning unnecessary data.
- Consider performance and server load.
- Keep complex behavior simple and predictable.

A useful principle is: **When in doubt, leave it out.** Add extra features after receiving real user feedback.

## 3. Responses

### Provide Helpful Feedback

Responses should clearly show whether a request succeeded or failed. Error messages should help developers understand and fix the problem.

Common response categories are:

- **2xx:** The request was successful.
- **4xx:** The client sent an invalid request.
- **5xx:** The server or API encountered an error.

Use specific status codes and concise error messages. Include links to additional documentation when more help is needed.

## Best Practices Summary

- Design the API before writing the implementation.
- Focus on the needs of API consumers.
- Use simple, consistent, noun-based URLs.
- Use HTTP methods according to their standard purposes.
- Use query parameters for filtering and limiting results.
- Return only useful data.
- Provide clear success and error responses.
- Document all endpoints and behavior.
- Improve the API gradually based on user feedback.

## Final Idea

Good API design makes an API easier to build, understand, integrate, document, and maintain. Clear choices made early can prevent many problems later.
