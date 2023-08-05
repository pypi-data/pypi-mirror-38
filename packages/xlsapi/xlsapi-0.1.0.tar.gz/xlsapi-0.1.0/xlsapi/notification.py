from queue import  Queue
from typing import Any

from flask import Response, request, abort


class Notification:
    def __init__(self, server=None):
        self.__queues = {}
        self.__cnt = 0
        if server is not None:
            self.add_url_rules(server.get_app())
            server.register_push(self.send)

    def add_url_rules(self, app):
        app.add_url_rule('/notification', 'notification', self.stream)
        app.add_url_rule('/push', 'push', self.push, methods=["POST"])

    def create_client(self):
        self.__cnt = self.__cnt + 1
        cnt = "client_" + str(self.__cnt)
        print("client {} connected.".format(cnt))

        queue = Queue(maxsize=10)
        queue.put("{\"info\": \"Connection established. You are client " + cnt + " \"}")
        self.__queues[cnt] = queue

        return queue

    def event_stream(self):
            queue = self.create_client()
            while True:
                yield 'data: {}\n\n'.format(queue.get())

    def stream(self):
        return Response(self.event_stream(), mimetype="text/event-stream")

    def send(self, message):
        to_remove = []
        for key in self.__queues:
            queue = self.__queues[key]
            if not queue.full():
                queue.put(message)
            else:
                to_remove.append(key)
        
        for key in to_remove:
            print("remove full queue - client " + key + " seems to be not available any longer.")
            del self.__queues[key]
            
        print(str(len(self.__queues)) + " clients connected.")

    def push(self):
        if request.json is not None:
            self.send(request.json)
            return "Message received."
        else:
            abort(400, "invalid message JSON expected")
