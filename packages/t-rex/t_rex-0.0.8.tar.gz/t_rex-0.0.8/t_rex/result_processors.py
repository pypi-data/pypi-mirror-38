def process_results(cmd, output):
    try:
        processor = result_processors.get(_cmd_type(cmd))
        return processor and processor(output)
    except KeyError:
        return str(output)


def build_scoped_cmd(item, prev_cmd, get_data_type):
    cmd_type = _cmd_type(prev_cmd)
    cmd_builder = scoped_cmd_builders.get(cmd_type)
    if cmd_builder:
        return cmd_builder(item, prev_cmd, get_data_type)
    else:
        return None


def _extract_namespace(cmd):
    try:
        return cmd.split(None)[-1]
    except IndexError:
        return None


def _cmd_type(cmd):
    try:
        if cmd.startswith("config"):
            return " ".join(cmd.split(None, 2)[:2])
        else:
            return cmd.split(None, 1)[0].lower()
    except IndexError:
        return None


def _byteslist2strtuple(lst):
    """Converts a list into a pair to tuples where the subsequent items are
    paired together."""
    l = _bytes2str_list(lst)
    if len(l) < 2:
        return l
    return zip(l[0::2], l[1::2])


def _bytestuple2strtuple_list(lst):
    for tup in lst:
        if tup is None:
            yield "null"
        else:
            x, y = tup
            yield _bytes2str(x), _bytes2str(y)


def _bytes2str_list(lst):
    return [_bytes2str(x) for x in lst]


def _bytes2str(byte_s):
    if byte_s is None:
        return "null"
    return byte_s.decode("utf-8")


def _builder_HKEYS(item, prev_cmd, _):
    namespace = _extract_namespace(prev_cmd)
    return namespace and f"hget {namespace} {item}"


def _builder_KEYS(item, _, get_data_type):
    type2command = {
        "hash": "hkeys {item}",
        "string": "get {item}",
        "set": "smembers {item}",
        "list": "lrange {item} 0 -1",
        "zset": "zrange {item} 0 -1",
    }
    data_type = get_data_type(item)
    scoped_cmd = type2command.get(data_type)
    return scoped_cmd and scoped_cmd.format(item=item)


result_processors = {
    # connection
    "ping": _bytes2str,
    "echo": _bytes2str,
    # Geo
    "geoadd": str,
    "geohash": _bytes2str_list,
    "geopos": _bytestuple2strtuple_list,
    "geodist": _bytes2str,
    "georadius": _bytes2str_list,
    "georadiusbymember": _bytes2str_list,
    # hash
    "hdel": str,
    "hexists": _bytes2str,
    "hget": _bytes2str,
    "hgetall": _byteslist2strtuple,
    "hincrby": str,
    "hincrbyfloat": _bytes2str,
    "hkeys": _bytes2str_list,
    "hlen": str,
    "hmget": _bytes2str_list,
    "hmset": _bytes2str,
    "hset": str,
    "hsetnx": str,
    "hstrlen": str,
    "hvals": _bytes2str_list,
    "hscan": str,
    "keys": _bytes2str_list,
    "get": _bytes2str,
    "type": _bytes2str,
    "config get": _byteslist2strtuple,
    "config set": _bytes2str,
    "set": _bytes2str,
    "lpush": str,
    "lrange": _bytes2str_list,
    "sadd": str,
    "smembers": _bytes2str_list,
    "zadd": str,
    "zscore": _bytes2str,
    "zrange": _bytes2str_list,
    "zrangebyscore": _bytes2str_list,
}

scoped_cmd_builders = {"keys": _builder_KEYS, "hkeys": _builder_HKEYS}
