def default_processor(entity):
    """Input entity can be a string, list, map, zip object etc.
       Returns a tuple of (err, transformed_string).
    """
    try:
        if isinstance(entity, str):
            return None, entity
        return None, '\n'.join(map(str, entity))
    except Exception as e:
        return str(e), entity

def json(input_text):
    """Take in the input_text and returns a tuple of
       (err, transformed_string)
    """
    import json
    try:
        json_obj = json.loads(input_text)
        return None, json.dumps(json_obj, sort_keys=True, indent=2)
    except Exception as e:
        return str(e) + ' failed json formatter', input_text
