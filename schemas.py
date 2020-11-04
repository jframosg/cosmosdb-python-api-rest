SCHEMA_ADD_ORDER = {
    'type': 'object',
    'properties': {
        'item': {'type': 'string'},
        'cname': {'type': 'string'},
        'description': {'type': 'string'},
        'origin': {'type': 'string'},
        'quantity': {'type': 'integer'}
    },
    'required': ['item', 'cname', 'description', 'origin', 'quantity' ],
    'additionalProperties': False
}

SCHEMA_UPDATE_ORDER = {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'},
        'item': {'type': 'string'},
        'cname': {'type': 'string'},
        'description': {'type': 'string'},
        'origin': {'type': 'string'},
        'quantity': {'type': 'integer'}
    },
    'required': ['id', 'item' ],
    'additionalProperties': False
}

SCHEMA_DELETE_ORDER = {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'}
    },
    'required': ['id' ],
    'additionalProperties': False
}
