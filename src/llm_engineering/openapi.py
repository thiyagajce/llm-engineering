"""OpenAPI/Swagger documentation for AI projects API."""

OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "AI Projects API",
        "description": "API documentation for chatbot, sentiment analysis, and RAG system",
        "version": "1.0.0"
    },
    "servers": [
        {"url": "http://localhost:5001", "description": "Chatbot server"},
        {"url": "http://localhost:5003", "description": "RAG system server"}
    ],
    "paths": {
        "/health": {
            "get": {
                "summary": "Health check",
                "tags": ["Common"],
                "responses": {
                    "200": {
                        "description": "Service is healthy",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "ok"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/chat": {
            "post": {
                "summary": "Send message to chatbot",
                "tags": ["Chatbot"],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {"type": "string", "example": "Hello!"}
                                },
                                "required": ["message"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Chatbot response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "reply": {"type": "string"},
                                        "intent": {"type": "string"},
                                        "confidence": {"type": "number"},
                                        "history_length": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/history": {
            "get": {
                "summary": "Get conversation history",
                "tags": ["Chatbot"],
                "responses": {
                    "200": {
                        "description": "Conversation history",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "history": {
                                            "type": "array",
                                            "items": {
                                                "type": "object"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/clear": {
            "post": {
                "summary": "Clear conversation history",
                "tags": ["Chatbot"],
                "responses": {
                    "200": {
                        "description": "History cleared",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "cleared"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/query": {
            "post": {
                "summary": "Query the RAG system",
                "tags": ["RAG"],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string", "example": "What is machine learning?"}
                                },
                                "required": ["query"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "RAG system answer",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string"},
                                        "answer": {"type": "string"},
                                        "documents_retrieved": {"type": "integer"},
                                        "retrieved_docs": {
                                            "type": "array",
                                            "items": {
                                                "type": "object"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/documents": {
            "get": {
                "summary": "Get all loaded documents",
                "tags": ["RAG"],
                "responses": {
                    "200": {
                        "description": "List of documents",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "count": {"type": "integer"},
                                        "documents": {
                                            "type": "array",
                                            "items": {
                                                "type": "object"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}


def get_openapi_json():
    """Get OpenAPI spec as JSON."""
    import json
    return json.dumps(OPENAPI_SPEC, indent=2)
