from notedlib.logging import logging

logger = logging.getLogger(__name__)


class Subscriber:
    def __init__(self, callback, props=[]):
        self.callback = callback
        self.props = props

    def is_interested_in_props(self, props):
        is_global_subscriber = len(self.props) == 0
        is_interested_in_props = set(props) & set(self.props)
        return is_global_subscriber or is_interested_in_props

    def is_interested_in_prop(self, prop):
        return prop in self.props


class SubscribableDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscribers = []

    def subscribe(self, props, callback):
        self.subscribers.append(Subscriber(callback, props))
        return self

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        affected_subscribers = [sub for sub in self.subscribers
                                if sub.is_interested_in_prop(key)]
        logger.debug('%dst subscribers was curious about %s' %
                     (len(affected_subscribers), key))

        self._emit_subscribers(affected_subscribers)

    def _emit_subscribers(self, subscribers):
        for subscriber in subscribers:
            subscriber.callback(self)

    def emit_all_subscribers(self):
        if self.subscribers:
            self._emit_subscribers(self.subscribers)
