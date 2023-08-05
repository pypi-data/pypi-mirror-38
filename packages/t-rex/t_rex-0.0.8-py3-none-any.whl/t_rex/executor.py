from redis import Redis, exceptions
from .result_processors import process_results, build_scoped_cmd


class RedisKeyMetadata:
    def __init__(self, kind, ttl):
        self.kind = kind
        self.ttl = ttl

    def __repr__(self):
        r = ""
        if self.kind:
            r += f"type: {self.kind}"
        if self.ttl:
            r += f"ttl: {self.ttl}"
        return r


class Executor:
    def __init__(self, host="localhost", port=6379, db=None):
        self.conn = Redis(host, port, db)

    def run(self, cmd, reset_cmd_stack=False):
        try:
            results = self.conn.execute_command(cmd)
            return cmd, process_results(cmd, results)
        except exceptions.ResponseError as e:
            return cmd, str(e)

    def scoped_run(self, item, prev_cmd):
        scoped_cmd = build_scoped_cmd(item, prev_cmd, self._get_data_type)
        if scoped_cmd is None:
            return None, None
        return self.run(scoped_cmd)

    def _get_data_type(self, key):
        try:
            results = self.conn.execute_command("type {}".format(key))
        except Exception as e:
            return None
        return results.decode("utf-8")

    def _get_ttl(self, key):
        try:
            ttl = self.con.execute_command("ttl {}".format(key))
        except Exception as e:
            return None
        return str(ttl)

    def get_metadata(self, key):
        kind = self._get_data_type(key)
        ttl = self._get_ttl(key)
        return RedisKeyMetadata(kind, ttl)
