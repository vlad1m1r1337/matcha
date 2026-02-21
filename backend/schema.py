"""
Custom OpenAPI schema for hello app endpoints.
Used to extend drf-spectacular schema for function-based views.
"""


def custom_preprocessing_hook(endpoints):
    """Filter out endpoints if needed."""
    return endpoints


def custom_postprocessing_hook(result, generator, request, public):
    """Add custom endpoints to the schema."""

    # User schema definition
    user_schema = {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer', 'example': 1},
            'profile_id': {'type': 'integer', 'example': 1, 'nullable': True},
            'name': {'type': 'string', 'example': 'John'},
            'surname': {'type': 'string', 'example': 'Doe'},
            'email': {'type': 'string', 'format': 'email', 'example': 'john@example.com'},
            'created_at': {'type': 'string', 'format': 'date-time'},
            'updated_at': {'type': 'string', 'format': 'date-time'},
        }
    }

    error_schema = {
        'type': 'object',
        'properties': {
            'error': {'type': 'string', 'example': 'Error message'},
            'details': {
                'type': 'object',
                'additionalProperties': {'type': 'string'},
                'nullable': True
            }
        }
    }

    create_user_schema = {
        'type': 'object',
        'required': ['name', 'surname', 'email', 'password'],
        'properties': {
            'name': {'type': 'string', 'example': 'John'},
            'surname': {'type': 'string', 'example': 'Doe'},
            'email': {'type': 'string', 'format': 'email', 'example': 'john@example.com'},
            'password': {'type': 'string', 'format': 'password', 'example': 'securepassword123'},
            'profile_id': {'type': 'integer', 'nullable': True, 'description': 'Optional profile ID to link (user can fill profile later)'},
        }
    }

    update_user_schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string', 'example': 'John'},
            'surname': {'type': 'string', 'example': 'Doe'},
            'email': {'type': 'string', 'format': 'email', 'example': 'john@example.com'},
            'password': {'type': 'string', 'format': 'password', 'example': 'newpassword123'},
        }
    }

    # Add schemas to components
    if 'components' not in result:
        result['components'] = {}
    if 'schemas' not in result['components']:
        result['components']['schemas'] = {}

    result['components']['schemas']['User'] = user_schema
    result['components']['schemas']['Error'] = error_schema
    result['components']['schemas']['CreateUser'] = create_user_schema
    result['components']['schemas']['UpdateUser'] = update_user_schema
    result['components']['schemas']['UserList'] = {
        'type': 'object',
        'properties': {
            'users': {
                'type': 'array',
                'items': {'$ref': '#/components/schemas/User'}
            }
        }
    }
    result['components']['schemas']['DeleteResponse'] = {
        'type': 'object',
        'properties': {
            'deleted': {'type': 'boolean', 'example': True}
        }
    }

    # Add paths for function-based views
    if 'paths' not in result:
        result['paths'] = {}

    # GET/POST /api/users/
    result['paths']['/api/users/'] = {
        'get': {
            'operationId': 'listUsers',
            'summary': 'List all users',
            'description': 'Retrieve a paginated list of all users.',
            'tags': ['Users'],
            'parameters': [
                {
                    'name': 'limit',
                    'in': 'query',
                    'description': 'Maximum number of users to return (default: 100)',
                    'required': False,
                    'schema': {'type': 'integer', 'default': 100}
                },
                {
                    'name': 'offset',
                    'in': 'query',
                    'description': 'Number of users to skip (default: 0)',
                    'required': False,
                    'schema': {'type': 'integer', 'default': 0}
                }
            ],
            'responses': {
                '200': {
                    'description': 'List of users',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/UserList'}
                        }
                    }
                },
                '500': {
                    'description': 'Internal server error',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/Error'}
                        }
                    }
                }
            }
        },
        'post': {
            'operationId': 'createUser',
            'summary': 'Create a new user',
            'description': 'Create a new user with the provided data.',
            'tags': ['Users'],
            'requestBody': {
                'required': True,
                'content': {
                    'application/json': {
                        'schema': {'$ref': '#/components/schemas/CreateUser'}
                    }
                }
            },
            'responses': {
                '201': {
                    'description': 'User created successfully',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/User'}
                        }
                    }
                },
                '400': {
                    'description': 'Invalid request data',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/Error'}
                        }
                    }
                },
                '409': {
                    'description': 'User already exists',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/Error'}
                        }
                    }
                },
                '500': {
                    'description': 'Internal server error',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/Error'}
                        }
                    }
                }
            }
        }
    }

    # GET/PUT/DELETE /api/users/{user_id}/
    result['paths']['/api/users/{user_id}/'] = {
        'get': {
            'operationId': 'getUser',
            'summary': 'Get user by ID',
            'description': 'Retrieve a specific user by their ID.',
            'tags': ['Users'],
            'parameters': [
                {
                    'name': 'user_id',
                    'in': 'path',
                    'description': 'User ID',
                    'required': True,
                    'schema': {'type': 'integer'}
                }
            ],
            'responses': {
                '200': {
                    'description': 'User details',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/User'}
                        }
                    }
                },
                '404': {
                    'description': 'User not found',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/Error'}
                        }
                    }
                },
                '500': {
                    'description': 'Internal server error',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/Error'}
                        }
                    }
                }
            }
        },
        'put': {
            'operationId': 'updateUser',
            'summary': 'Update user',
            'description': 'Update an existing user. All fields are optional.',
            'tags': ['Users'],
            'parameters': [
                {
                    'name': 'user_id',
                    'in': 'path',
                    'description': 'User ID',
                    'required': True,
                    'schema': {'type': 'integer'}
                }
            ],
            'requestBody': {
                'required': True,
                'content': {
                    'application/json': {
                        'schema': {'$ref': '#/components/schemas/UpdateUser'}
                    }
                }
            },
            'responses': {
                '200': {
                    'description': 'User updated successfully',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/User'}
                        }
                    }
                },
                '400': {
                    'description': 'Invalid request data',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/Error'}
                        }
                    }
                },
                '404': {
                    'description': 'User not found',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/Error'}
                        }
                    }
                },
                '409': {
                    'description': 'Email already taken',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/Error'}
                        }
                    }
                },
                '500': {
                    'description': 'Internal server error',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/Error'}
                        }
                    }
                }
            }
        },
        'delete': {
            'operationId': 'deleteUser',
            'summary': 'Delete user',
            'description': 'Delete a user by their ID.',
            'tags': ['Users'],
            'parameters': [
                {
                    'name': 'user_id',
                    'in': 'path',
                    'description': 'User ID',
                    'required': True,
                    'schema': {'type': 'integer'}
                }
            ],
            'responses': {
                '200': {
                    'description': 'User deleted successfully',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/DeleteResponse'}
                        }
                    }
                },
                '404': {
                    'description': 'User not found',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/Error'}
                        }
                    }
                },
                '500': {
                    'description': 'Internal server error',
                    'content': {
                        'application/json': {
                            'schema': {'$ref': '#/components/schemas/Error'}
                        }
                    }
                }
            }
        }
    }

    # Legacy endpoints
    result['paths']['/'] = {
        'get': {
            'operationId': 'index',
            'summary': 'Hello World',
            'description': 'Returns a simple Hello World message.',
            'tags': ['Legacy'],
            'responses': {
                '200': {
                    'description': 'Hello World response',
                    'content': {
                        'text/html': {
                            'schema': {'type': 'string', 'example': 'Hello World'}
                        }
                    }
                }
            }
        }
    }

    result['paths']['/users/'] = {
        'get': {
            'operationId': 'usersListLegacy',
            'summary': 'List users (legacy)',
            'description': 'Legacy endpoint to fetch all users with raw SQL.',
            'tags': ['Legacy'],
            'responses': {
                '200': {
                    'description': 'List of users',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'ok': {'type': 'boolean', 'example': True},
                                    'count': {'type': 'integer', 'example': 10},
                                    'users': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {
                                                'id': {'type': 'integer'},
                                                'profile_id': {'type': 'integer', 'nullable': True},
                                                'name': {'type': 'string'},
                                                'surname': {'type': 'string'},
                                                'email': {'type': 'string'}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                '500': {
                    'description': 'Database error',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'ok': {'type': 'boolean', 'example': False},
                                    'error': {'type': 'string'}
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    return result
