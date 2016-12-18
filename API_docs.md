API v1 specification
====================

All API endpoints are accessed from the `https://facebook.tracking.exposed/api/v1` root.

# API: Server to parsers

The following specifications are implemented in the server and in the
components executing parsing and analysis of posts.

The following APIs are intended to distribute the effort of HTML parsing,
data extraction and data mining.

## Parser identification

Every parser performing the request has a key (provided by the server) and a name. The key is secret, and authenticates the specific parser.

A parser is intended to extract a specific content from the HTML snippet.

*For example: a parser extracting the author info (name and userId) is different from a parser extracting the preview image display, and they
would have self explanatory names like 'imagePreview' and 'authorInfo'.*

The key is a string of 20 chars in base58, random bytes, and take name of
`parserKey` in this specification.

### Get available HTML snippet

- **Endpoint**:

  `/snippet/status`

- **Method:**

  `POST`

- **Payload**

  ```json
  {
    "since": "<ISO8601 DateTime>",
    "until": "<ISO8601 DateTime>",
    "parserName": "<string>",
    "requirements": "<object>"
  }
  ```

  For example, if your parser is analyzing promoted posts received in the last 48 hours:

  ```json
  {
    "requirements": { "postType" : "promoted " },
    "since": "2016-11-08T21:15:13.511Z",
    "until": "2016-11-10T21:15:13.516Z",
    "parserName": "postType",
  }
  ```

- **Success Response:**

  - **Code:** `200`
  - **Content:**
    ```json
    {
      "available": "<Int>",
      "limit": "<Int>"
    }
    ```

  The server checks the stored HTML pieces in the requested time range. It then returns the number of `available` HTML snippets that do not yet have a key named `parserName`, and the maximum amount of HTML snippets that would be returned when the endpoint content (below) is invoked.

- **Sample Call:**

  ```python
  payload = {
    "requirements": { "postType" : "promoted " },
    "since": "2016-12-17",
    "until": "2016-12-18T21:15:13.516Z",
    "parserName": "postType",
  }
  requests.post(
      'https://facebook.tracking.exposed/api/v1/snippet/status',
      data=payload)
  ```

### Get HTML snippet content

- **Endpoint**:

  `/snippet/content`

- **Method:**

  `POST`

- **Payload**

  ```json
  {
    "since": "<ISO8601 DateTime>",
    "until": "<ISO8601 DateTime>",
    "parserName": "<string>",
    "requirements": "<object>"
  }
  ```

- **Success Response:**

  - **Code:** `200`
  - **Content:**
    ```json
    [
      {
        "html": "<html snippet>",
        "metadata-1": "<value>",
        "metadata-2": "<value>",
        "snippetId": "<hash of html snippet>"
        },
    ]
    ```

    The call returns a list of objects, each one containing the HTML section, the id, writingTime, and the previously added metadata.


- **Sample Call:**

  ```python
  payload = {
    "requirements": { "postType" : "promoted " },
    "since": "2016-12-17",
    "until": "2016-12-18T21:15:13.516Z",
    "parserName": "postType",
  }
  requests.post(
      'https://facebook.tracking.exposed/api/v1/snippet/content',
      data=payload)
  ```

### Commit the parser results

When the parser has operated, it has to commit a result in order to mark the snippet already processed by the parser. Even if the parser hasn't given back any answer the results have to be committed (so that they would be marked as processed).

- **Endpoint**:

  `/snippet/result`

- **Method:**

  `POST`

- **Payload**

  ```json
  {
    "snippetId": "<hash of html snippet>",
    "parserName": "<string>",
    "parserKey": "<parserKey>",
    "result": "<metadata>"
  }
  ```

- **Success Response:**

  - **Code:** `200`
  - **Content:**

- **Sample Call:**
