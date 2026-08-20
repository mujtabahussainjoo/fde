# YAML: Short Notes

## What is YAML?

- YAML stands for **YAML Ain't Markup Language**.
- It is a human-readable format for storing and exchanging data.
- YAML is commonly used for configuration files, APIs, and automation tools.
- YAML files usually use the `.yaml` or `.yml` extension.

## Basic Rules

- Use spaces for indentation, not tabs.
- Indentation shows the relationship between data items.
- YAML is case-sensitive.
- Use `key: value` pairs.
- Comments begin with `#`.
- Strings can be written without quotes in simple cases.

## Simple Example

```yaml
name: Mujtaba
age: 25
active: true
```

## Lists

- Lists begin with a hyphen (`-`).
- Each list item should use the same indentation.

```yaml
languages:
  - Python
  - JavaScript
  - YAML
```

## Nested Data

```yaml
user:
  name: Mujtaba
  contact:
    email: mujtaba@example.com
    phone: "123-456-7890"
```

## Common Data Types

- **String:** `name: Mujtaba`
- **Number:** `age: 25`
- **Boolean:** `active: true`
- **List:** `colors: [red, blue, green]`
- **Null:** `value: null`

## YAML in Configuration

```yaml
server:
  host: localhost
  port: 8080
  debug: true
```

## Key Benefits

- Easy for humans to read and write.
- Supports nested data and lists.
- Works well for configuration files.
- Can be converted to JSON and other formats.
- Supported by many programming languages and tools.

## Final Idea

YAML is a simple and readable way to represent structured data, especially configuration settings.
