import json
import uuid
import weakref

from flask import current_app, _app_ctx_stack, request, make_response, abort


class Event(object):
    def __init__(self, app, domain):
        self.app = app  # slack/discord/etc
        self.domain = domain  # team/server

    def __str__(self):
        return "<Event from %s>" % self.app


class Command(Event):
    def __init__(self, name, data, app, domain):
        super().__init__(app, domain)
        self.name = name
        self.data = data

    def __str__(self):
        return "<%s Command from %s>" % (self.name, self.app)


class Cacophony(object):
    def __init__(self, app=None):
        self.commands = {}
        self.app = app
        if app is not None:
            self.init_app(app)

    def command(self, name):
        def decorator(f):
            self.commands[name] = weakref.ref(f)
            print(f)
            return f
        return decorator

    def event(self, view):
        if isinstance(view, Command):
            command = self.commands.get(view.name, None)
            if command:
                command = command()
                if command:
                    return command(view)
        return abort(404)

    @staticmethod
    def init_app(app):
        app.config.setdefault('CACOPHONY_EMBED_RAW_EVENT', False)
