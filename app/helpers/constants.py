from enum import Enum


# Status codes
class Status(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    CONFLICT = 409
    UPDATED = 204
    DELETED = 204
