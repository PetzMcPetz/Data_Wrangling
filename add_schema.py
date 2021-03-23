# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 18:11:28 2021

@author: Petzi
"""

def get_schema():

    osm_schema = {
        'node': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'lat': {'required': True, 'type': 'float', 'coerce': float},
                'lon': {'required': True, 'type': 'float', 'coerce': float},
                'user': {'required': True, 'type': 'string'},
                'uid': {'required': True, 'type': 'integer', 'coerce': int},
                'version': {'required': True, 'type': 'string'},
                'changeset': {'required': True, 'type': 'integer', 'coerce': int},
                'timestamp': {'required': True, 'type': 'string'}
            }
        },
        'node_tags': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'id': {'required': True, 'type': 'integer', 'coerce': int},
                    'key': {'required': True, 'type': 'string'},
                    'value': {'required': True, 'type': 'string'},
                    'type': {'required': True, 'type': 'string'}
                }
            }
        },
        'way': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'user': {'required': True, 'type': 'string'},
                'uid': {'required': True, 'type': 'integer', 'coerce': int},
                'version': {'required': True, 'type': 'string'},
                'changeset': {'required': True, 'type': 'integer', 'coerce': int},
                'timestamp': {'required': True, 'type': 'string'}
            }
        },
        'way_nodes': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'id': {'required': True, 'type': 'integer', 'coerce': int},
                    'node_id': {'required': True, 'type': 'integer', 'coerce': int},
                    'position': {'required': True, 'type': 'integer', 'coerce': int}
                }
            }
        },
        'way_tags': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'id': {'required': True, 'type': 'integer', 'coerce': int},
                    'key': {'required': True, 'type': 'string'},
                    'value': {'required': True, 'type': 'string'},
                    'type': {'required': True, 'type': 'string'}
                }
            }
        }
    }
    
    return osm_schema