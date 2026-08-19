members = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "total_results": {
      "type": "number"
    },
    "page": {
      "type": "number"
    },
    "per_page": {
      "type": "number"
    },
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "number"
          },
          "observations_count": {
            "type": "number"
          },
          "user": {
            "type": "object",
            "properties": {
              "id": {
                "type": "number"
              }
            },
            "required": [
              "id"
            ]
          }
        },
        "required": [
          "id",
          "observations_count",
          "user"
        ]
      }
    }
  },
  "required": [
    "total_results",
    "page",
    "per_page",
    "results"
  ]
}