

def get_swagger_description_tag( a_item):
    return a_item["app"] + " " + a_item["plural"]


def get_swagger_description_service_tag( a_service):
    return "$service " + a_service.get_name()


def get_swagger_description_path( a_item, a_with_id):
    """ query can be get, getAll, put, post and delete """
    w_path = "/" + a_item["plural"]
    if a_with_id:
        w_path = w_path + "/{id}"
    return w_path


def get_swagger_description_empty( a_item, a_path):
    """ return the path description for the item"""
    a_path["/" + a_item["plural"] + "/$empty"] = {
        "get": {
            "tags": [get_swagger_description_tag(a_item)],
            "operationId": "empty_" + a_item["plural"],
            "consumes": ["application/json"],
            "produces": ["application/json"],
            "parameters": [],
            "responses": {
                "default": {
                    "description": "successful operation"
                }
            }
        }
    }


def get_swagger_description_schema( a_item, a_path):
    """ return the path description for the item"""
    a_path["/" + a_item["plural"] + "/$schema"] = {
        "get": {
            "tags": [get_swagger_description_tag(a_item)],
            "operationId": "schema_" + a_item["plural"],
            "consumes": ["application/json"],
            "produces": ["application/json"],
            "parameters": [],
            "responses": {
                "default": {
                    "description": "successful operation"
                }
            }
        }
    }


def get_swagger_description_service( a_service, a_path):
    """ return the path description for the item"""

    a_path["/$service/" + a_service.get_name()] = {}
    if a_service.has_post():
        a_path["/$service/" + a_service.get_name()]["post"] = {
            "tags": [get_swagger_description_service_tag(a_service)],
            "operationId": "service_" + a_service.get_name(),
            "consumes": ["application/json"],
            "produces": ["application/json"],
            "parameters": [{
                "in": "body",
                "name": "body",
                "required": True,
                "schema": {
                    "type": "string"
                }
            }],
            "responses": {
                "default": {
                    "description": "successful operation"
                }
            }
        }
    if a_service.has_put():
        a_path["/$service/" + a_service.get_name()]["put"] = {
            "tags": [get_swagger_description_service_tag(a_service)],
            "operationId": "service_" + a_service.get_name(),
            "consumes": ["application/json"],
            "produces": ["application/json"],
            "parameters": [{
                "in": "body",
                "name": "body",
                "required": True,
                "schema": {
                    "type": "string"
                }
            }],
            "responses": {
                "default": {
                    "description": "successful operation"
                }
            }
        }


    return a_path


def get_swagger_description( a_item, a_path):
    """ return the path description for the item"""
    a_path[get_swagger_description_path(a_item, False)] = {
        "get": {
            "tags": [get_swagger_description_tag(a_item)],
            "operationId": "getAll_" + a_item["id"],
            "produces": ["application/json"],
            "parameters": [{
                "name": "filter",
                "in": "query",
                "required": False,
                "type": "string"
            }, {
                "name": "offset",
                "in": "query",
                "required": False,
                "type": "integer",
                "default": 0,
                "format": "int32"
            }, {
                "name": "limit",
                "in": "query",
                "required": False,
                "type": "integer",
                "default": 50,
                "format": "int32"
            }, {
                "name": "sort",
                "in": "query",
                "required": False,
                "type": "string"
            }],
            "responses": {
                "default": {
                    "description": "successful operation"
                }
            }
        },
        "post": {
            "tags": [get_swagger_description_tag(a_item)],
            "operationId": "create_" + a_item["id"],
            "consumes": ["application/json"],
            "produces": ["application/json"],
            "parameters": [{
                "in": "body",
                "name": "body",
                "required": True,
                "schema": {
                    "type": "string"
                }
            }],
            "responses": {
                "default": {
                    "description": "successful operation"
                }
            }
        }
    }
    a_path[get_swagger_description_path(a_item, True)] = {
        "get": {
            "tags": [get_swagger_description_tag(a_item)],
            "operationId": "getItem_" + a_item["id"],
            "produces": ["application/json"],
            "parameters": [{
                "name": "id",
                "in": "path",
                "required": True,
                "type": "string"
            }],
            "responses": {
                "default": {
                    "description": "successful operation"
                }
            }
        },
        "put": {
            "tags": [get_swagger_description_tag(a_item)],
            "operationId": "update_" + a_item["id"],
            "consumes": ["application/json"],
            "produces": ["application/json"],
            "parameters": [{
                "in": "body",
                "name": "body",
                "required": True,
                "schema": {
                    "type": "string"
                }
            }, {
                "name": "id",
                "in": "path",
                "required": True,
                "type": "string"
            }],
            "responses": {
                "default": {
                    "description": "successful operation"
                }
            }
        }
    }
    get_swagger_description_empty(a_item, a_path)
    get_swagger_description_schema(a_item, a_path)

    return a_path


def get_swagger_description_item( a_path):
    """ return the path description for the item"""
    a_path["/items"] = {
        "get": {
            "tags": ["Core : Items"],
            "operationId": "getAll_Item",
            "produces": ["application/json"],
            "parameters": [],
            "responses": {
                "default": {
                    "description": "successful operation"
                }
            }
        }
    }
    a_path["/items/{id}"] = {
        "get": {
            "tags": ["Core : Items"],
            "operationId": "getItem_item",
            "produces": ["application/json"],
            "parameters": [{
                "name": "id",
                "in": "path",
                "required": True,
                "type": "string"
            }],
            "responses": {
                "default": {
                    "description": "successful operation"
                }
            }
        }
    }

    return a_path




