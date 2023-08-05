def default_processor(entity):
    """Input entity can be a string, list, map, zip object etc.
       Returns a tuple of (err, transformed_string).
    """
    try:
        if isinstance(entity, str):
            return None, entity
        return None, "\n".join(map(str, entity))
    except Exception as e:
        return str(e), entity


def shell_processor(cmd, input_text):
    """Take in the input_text and returns a tuple of
       (err, transformed_string)
    """
    import subprocess

    try:
        r = subprocess.run(
            cmd,
            input=input_text,
            text=True,
            shell=True,
            capture_output=True,
            check=True,
        )
        return None, r.stdout
    except subprocess.CalledProcessError as e:
        return str(e), input_text
