import chatexchange6 as ce
import logging


class Chat:

    def __init__(self, user, password, room=22091):
        client = ce.client.Client('stackoverflow.com')
        client.login(user, password)

        room = client.get_room(room)
        room.join()

        self._client = client
        self._room = room
        self._hooks = []

        def callback(event, client):
            if isinstance(event, ce.events.MessagePosted):
                user, text = event.user.id, event.content
                logging.info("Received '{}' from {}".format(text, user))
                if text.startswith("!!"):
                    text = text[3:].strip()
                    for index, f in enumerate(self._hooks):
                        if f:
                            try:
                                ret = f(user, text)
                                if ret:
                                    event.message.reply(ret)
                            except KeyboardInterrupt:
                                raise
                            except Exception as e:
                                e = "Exception raised while executing hook {}"\
                                        .format(index)
                                logging.warn(e)
                                logging.warn("Stack trace: {}".format(e))

        self._room.watch(callback)

    def send(self, stuff):
        """Sends a message to the chat room"""

        self._room.send_message(stuff)

    def add_hook(self, hook):
        """Adds `hook` to the list of hooks fired on message receive

           `hook` must be such that `callable(hook)` is True.
           Returns a numeric ID that can later invalidate said hook."
        """
        if not callable(hook):
            raise ValueError("hook must be a callable")

        # This will serve as the ID
        cur_length = len(self._hooks)

        self._hooks.append(hook)
        return cur_length

    def delete_hook(self, hook_id):
        """Takes the ID of a hook and removes it from the list of hooks

        Raises a ValueError if no such hook is found, or if said hook
        has already been removed.
        """

        if hook_id >= len(self._hooks) or hook_id < 0:
            raise ValueError("hook does not exist")
        else:
            said_hook = self._hooks[hook_id]
            if said_hook:
                self._hooks[hook_id] = None
            else:
                raise ValueError("hook has already been removed")
