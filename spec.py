SPEC = {
    "Root": {
        "fields": {
            "title": "str",
        },
        "required_fields": [],
        "allowed_children": ["Line"],
    },
    "Line": {
        "fields": {
            "x": "data",
            "y": "data",
            "width": "length",
        },
        "required_fields": ["x", "y"],
        "allowed_children": [],
    },
}