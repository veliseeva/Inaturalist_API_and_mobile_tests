non_existing_users = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "status": {
      "type": "string"
    },
    "errors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "errorCode": {
            "type": "string"
          },
          "message": {
            "type": "string"
          }
        },
        "required": [
          "errorCode",
          "message"
        ]
      }
    }
  },
  "required": [
    "status",
    "errors"
  ]
}