import json
from time import sleep
from celery_connectors.redis.redis_wrapper import RedisWrapper
from celery_connectors.redis.base_redis_application import BaseRedisApplication


class RedisJSONApplication(BaseRedisApplication):

    def __init__(self,
                 name,
                 redis_address,
                 redis_port,
                 redis_queue,
                 logger,
                 request_key_name=None,
                 response_key_name=None,
                 debug=False):
        BaseRedisApplication.__init__(self,
                                      name,
                                      redis_address,
                                      redis_port,
                                      redis_queue,
                                      logger,
                                      request_key_name,
                                      response_key_name,
                                      debug)
    # end of __init__

    def disconnect(self):
        if self.m_debug:
            self.lg(("Disconnecting redis={}:{} json queue={}")
                    .format(self.m_host_address,
                            self.m_port,
                            self.m_queue_name), 7)

        if self.m_rw:
            self.m_rw.client_kill()

        return None
    # end of disconnect

    def connect(self):
        if self.m_debug:
            if self.m_redis_password:
                self.lg(("Connecting to Secure redis={}:{}/{} json queue={}")
                        .format(self.m_host_address,
                                self.m_port,
                                self.m_db,
                                self.m_queue_name), 7)
            else:
                self.lg(("Connecting to Unsecure redis={}:{}/{} json queue={}")
                        .format(self.m_host_address,
                                self.m_port,
                                self.m_db,
                                self.m_queue_name), 7)
        # end of debugging

        self.m_rw = RedisWrapper(self.m_queue_name,
                                 serializer=json,
                                 host=self.m_host_address,
                                 port=int(self.m_port),
                                 db=int(self.m_db),
                                 password=self.m_redis_password)
        return None
    # end of connect

    def get_address(self):
        return str(self.m_host_address) + ":" + str(self.m_port)
    # end of get_address

    def get_single_cache(self, key=None):

        if not key:
            key = self.m_queue_name

        # By default RedisWrapper returns None when the timeout is hit
        msg = None
        try:
            # By default RedisWrapper returns None when the timeout is hit
            msg = self.m_rw.get_cached_single_set(key)

        except ValueError as e:
            self.lg(("VALUE ERROR: redis={}:{} key={} non-json ex={}")
                    .format(self.m_host_address,
                            self.m_port,
                            key,
                            e), 0)
        except Exception as e:
            test_for_redis_connectivity = str(e)
            if "Connection refused." in test_for_redis_connectivity:
                self.lg(("ERROR: Connection Failed to redis={}:{} key={} ex={} sleep={}")
                        .format(self.m_host_address,
                                self.m_port,
                                key,
                                e,
                                self.m_sleep_for_connection_outage), 0)
                sleep(self.m_sleep_for_connection_outage)
            else:
                self.lg(("ERROR: not-refused error redis={}:{} key={} ex={}")
                        .format(self.m_host_address,
                                self.m_port,
                                key,
                                e), 0)
        # end of try/ex

        if not msg:
            self.update_failed_get_count()
        else:
            self.update_get_count()

        return msg
    # end of get_single_cache

    def get_cached_set(self, start_idx=0, end_idx=-1, queue=None):

        # By default RedisWrapper returns None when the timeout is hit
        msg = None

        key = queue
        if not key:
            key = self.m_queue_name

        try:
            # By default RedisWrapper returns None when the timeout is hit
            if end_idx == -1:
                msg = self.m_rw.get_cached_single_set(queue)
            else:
                msg = self.m_rw.get_cached_multiple_set(start_idx, end_idx, queue)

        except ValueError as e:
            self.lg(("VALUE ERROR: redis={}:{} key={} non-json ex={}")
                    .format(self.m_host_address,
                            self.m_port,
                            key,
                            e), 0)
        except Exception as e:
            test_for_redis_connectivity = str(e)
            if "Connection refused." in test_for_redis_connectivity:
                self.lg(("ERROR: Connection Failed to redis={}:{} key={} ex={} sleep={}")
                        .format(self.m_host_address,
                                self.m_port,
                                key,
                                e,
                                self.m_sleep_for_connection_outage), 0)
                sleep(self.m_sleep_for_connection_outage)
            else:
                self.lg(("ERROR: not-refused error redis={}:{} key={} ex={}")
                        .format(self.m_host_address,
                                self.m_port,
                                key,
                                e), 0)
        # end of try/ex

        if not msg:
            self.update_failed_get_count()
        else:
            self.update_get_count()

        return msg
    # end of get_cached_set

    def get_message(self, block=False, key=None):

        # By default RedisWrapper returns None when the timeout is hit
        msg = None
        try:
            # By default RedisWrapper returns None when the timeout is hit
            msg = self.m_rw.get(False, self.m_fetch_timeout, key)
        except ValueError as e:
            self.lg(("VALUE ERROR: redis={}:{} key={} non-json ex={}")
                    .format(self.m_host_address,
                            self.m_port,
                            key,
                            e), 0)
        except Exception as e:
            test_for_redis_connectivity = str(e)
            if "Connection refused." in test_for_redis_connectivity:
                self.lg(("ERROR: Connection Failed to redis={}:{} key={} ex={} sleep={}")
                        .format(self.m_host_address,
                                self.m_port,
                                key,
                                e,
                                self.m_sleep_for_connection_outage), 0)
                sleep(self.m_sleep_for_connection_outage)
            else:
                self.lg(("ERROR: not-refused error redis={}:{} key={} ex={}")
                        .format(self.m_host_address,
                                self.m_port,
                                key,
                                e), 0)
        # end of try/ex

        if not msg:
            self.update_failed_get_count()
        else:
            self.update_get_count()

        return msg
    # end of get_message

    def put_into_key(self, key, msg_object):
        self.m_rw.put_into_key(key, msg_object)

        self.update_put_count()
        return None
    # end of put_into_key

    def put_message(self, msg_object):
        self.m_rw.put(msg_object)

        self.update_put_count()
        return None
    # end of put_message

    def wait_for_message_on_key(self, num_seconds, key):

        # By default RedisWrapper returns None when the timeout is hit
        msg = None
        try:
            # By default RedisWrapper returns None when the timeout is hit
            msg = self.m_rw.get(True, num_seconds, key)
        except ValueError as e:
            self.lg(("VALUE ERROR: redis={}:{} key={} non-json ex={}")
                    .format(self.m_host_address,
                            self.m_port,
                            key,
                            e), 0)
        except Exception as e:
            test_for_redis_connectivity = str(e)
            if "Connection refused." in test_for_redis_connectivity:
                self.lg(("ERROR: Connection Failed to redis={}:{} key={} ex={} sleep={}")
                        .format(self.m_host_address,
                                self.m_port,
                                key,
                                e,
                                self.m_sleep_for_connection_outage), 0)
            else:
                self.lg(("ERROR: not-refused error redis={}:{} key={} ex={}")
                        .format(self.m_host_address,
                                self.m_port,
                                key,
                                e), 0)
        # end of try/ex

        if not msg:
            self.update_failed_get_count()
        else:
            self.update_get_count()

        return msg
    # end of wait_for_message_on_key

    def exists(self, key):
        return self.m_rw.exists(key)
    # end of exists

    def delete_cache(self):
        self.m_rw.delete_cache()
        return None
    # end of delete_cache

    def flush_all(self):
        self.m_rw.flush_all()
        return None
    # end of delete_cache

    def get_cached_data_for_key(self, key):

        return_hash = {}

        return_hash["Status"] = "FAILED"
        return_hash["Exception"] = ""
        return_hash["Value"] = None

        try:
            self.connect()
        except Exception as e:
            return_hash["Exception"] = "ERROR: Connection Exception(" + str(e) + ")"
            return return_hash

        try:
            found_cached_values = self.m_rw.safe_get_cached_single_set(str(key))

            if found_cached_values["Status"] == "SUCCESS":
                return_hash["Value"] = found_cached_values["Value"]
                return_hash["Status"] = found_cached_values["Status"]
            else:
                return_hash["Value"] = found_cached_values["Value"]
                return_hash["Status"] = found_cached_values["Status"]
                return_hash["Exception"] = found_cached_values["Exception"]

        except Exception as e:
            return_hash["Exception"] = "ERROR: Disconnection Exception(" + str(e) + ")"
            self.disconnect()
            return return_hash

        try:
            self.disconnect()
        except Exception as e:
            return_hash["Exception"] = "ERROR: Disconnection Exception(" + str(e) + ")"
            return return_hash

        return return_hash
    # end of get_cached_data_for_key

# end of RedisJSONApplication


def build_redis_json_app_from_config(app_name, host, port, queue, logger, debug):
    json_app = RedisJSONApplication(app_name, host, port, queue, logger, debug)
    json_app.connect()
    return json_app
# end build_redis_json_app_from_config
