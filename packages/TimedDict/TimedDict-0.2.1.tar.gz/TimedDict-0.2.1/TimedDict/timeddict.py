from threading import Thread, Event
import time
import logging
from contextlib import contextmanager


class TimedDict(dict):
    def __init__(self, ttl: float = 1, purge_interval=0.1, overwrite_action: str = 'keep_last', logger=None):
        """
        Initialization of the TimedDict data type.
        :param ttl:                 [T]ime [T]o [L]ive, specifies the amount of time, in seconds, an element will stay in the TimedDict before being purged.
        :param purge_interval:      Specifies ether an interval, in seconds, for when the purge thread should run OR if the purge should be event based by setting it to: on_add
        :param overwrite_action:    Various behaviors if an overwrite of a key is about to happen: keep_last (normal / allow overwrite),
                                    keep_first (disallow overwrite), mean (takes the mean of the old and new value) and sum (add the new value to the existing).
        :param logger:              Parse a logger object is such exist, if not a simple print will be used.
        """

        super().__init__()
        self.store = dict()
        self.ttl = ttl
        self.purge_interval = purge_interval
        self.overwrite_action = overwrite_action

        if logger is None:
            self.logger = logging.getLogger()
        else:
            self.logger = logger

        self.enable_controls = False
        self._poison_pill = False
        self._pause = False
        self._pause_event = Event()
        self._pause_activated = Event()
        self._completed_purge = Event()

        if type(purge_interval) in [float, int]:
            self.enable_controls = True
            t = Thread(target=self._ttl_remove)
            t.start()

    def __setitem__(self, key, value):
        if self.purge_interval == 'on_add':
            self._event_remove(key)

        if self.overwrite_action == 'keep_first':
            if key not in self.store:
                # Do NOT overwrite!
                self.store[key] = value
                return

        elif self.overwrite_action == 'mean':
            if key in self.store:
                # Take the mean of the old and new value
                try:
                    self.store[key] = (self.store[key] + value) / 2
                    return

                except Exception as exp:
                    self.logger.error(exp)

        elif self.overwrite_action == 'sum':
            if key in self:
                self.update({key: self[key] + value})
                return

        self.update({key: value})

    def _event_remove(self, new_key):
        keys_to_delete = list()

        for key in self:
            if new_key - key > self.ttl:
                keys_to_delete.append(key)

        self._delete_keys(keys_to_delete)

    def _ttl_remove(self):
        while True:
            if self._poison_pill:
                break

            time.sleep(self.purge_interval)
            _now = time.time()
            keys_to_delete = list()

            if self._pause:
                self._pause_activated.set()
                self._pause_event.wait()
                self._pause_event.clear()

            for k in self.keys():
                if k < _now - self.ttl:
                    keys_to_delete.append(k)

            self._delete_keys(keys_to_delete)
            self._completed_purge.set()

    def _delete_keys(self, keys_to_delete):
        for key in keys_to_delete:
            try:
                self.pop(key)
            except KeyError:
                self.logger.warning('Key ({deleted_key}) does not exist'.format(deleted_key=key))
                pass

    def _perform_debug_logging(self, line):
        if self.logger is None:
            print('TimedDict LOG: {}'.format(line))
        else:
            self.logger.debug(line)

    def pause(self):
        if self.enable_controls:
            self._pause = True
            self._pause_activated.wait()
            self._pause_activated.clear()

    def resume(self):
        if self.enable_controls:
            self._pause = False
            self._pause_event.set()
            self._completed_purge.clear()
            self._completed_purge.wait()

    def stop(self):
        if self.enable_controls:
            self._poison_pill = True

    @contextmanager
    def protect(self):
        self.pause()
        yield self
        self.resume()
