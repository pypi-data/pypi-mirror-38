import json
import time
import redis

class Queue(object):
    """Simple Priority Queue with Redis Backend
        Adopted from http://peter-hoffmann.com/2012/python-simple-queue-redis-queue.html"""

    def __init__(self, redis_url, key):
        """redis_url showed be a valid redis url formatted : redis://[:password]@localhost:6379/0"""
        self.__db = redis.from_url(redis_url)
        self.key = key

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.zcount(self.key, "-inf", "+inf")

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item, score):
        """Put any json serializable item into the queue."""
        self.__db.zadd(self.key, json.dumps(item), score)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.
            If optional args block is true and timeout is None (the default), block
            if necessary until an item is available."""

        result = self.__db.zrevrange(self.key, 0, 1)

        while block and len(result) == 0:
            time.sleep(1)
            result = self.__db.zrevrange(self.key, 0, 1)

        if len(result) == 0:
            return None
        else:
            self.__db.zrem(self.key, result[0])
            return json.loads(result[0])

    def remove(self, item):
        """
            input - an item to remove from the queue.
            Returns the number of items that were removed
        """
        removed_item = self.__db.zrem(self.key, json.dumps(item))
        return removed_item

    def delete(self):
        self.__db.delete(self.key)

    def all(self):
        items = self.__db.zrange(self.key, 0, -1)
        return [json.loads(item) for item in items]

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)