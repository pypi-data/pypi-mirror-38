# import sqlite3
import json
import uuid
import weakref

from .Cacophony import Command

from flask import request, make_response, abort


class Cacophony(object):
    def __init__(self, cacophony, app=None):
        self.commands = {}
        self.app = app
        self.cacophony = cacophony
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('CACOPHONY_SLACK_TOKEN', str(uuid.uuid4()))
        app.config.setdefault('CACOPHONY_SLACK_EVENTS', '/slack/events')
        if app.config.get('CACOPHONY_SLACK_VERIFICATION_TOKEN') is None:
            raise ValueError('CACOPHONY_SLACK_VERIFICATION_TOKEN is not set')
        app.add_url_rule(app.config['CACOPHONY_SLACK_EVENTS'], view_func=self.incoming_event, methods=['POST', ])

    def command(self, name):
        def decorator(f):
            self.commands[name] = weakref.ref(f)
            print(f)
            return f
        return decorator

    def incoming_event(self):
        # Parse the request payload into JSON
        if not request.data:
            abort(404)
        event_data = json.loads(request.data.decode('utf-8'))

        # Echo the URL verification challenge code
        if "challenge" in event_data:
            return make_response(
                event_data.get("challenge"), 200, {"content_type": "application/json"}
            )

        # Parse the Event payload and emit the event to the event listener
        if "event" in event_data:
            # Verify the request token
            request_token = event_data.get("token")
            if self.app.config['CACOPHONY_SLACK_VERIFICATION_TOKEN'] != request_token:
                message = "Request contains invalid Slack verification token"
                return make_response(message, 403)

            event_type = event_data["event"]["type"]
            # request.environ["appenlight.username"] = event_data['team_id']
            if event_type == 'message' and event_data['event']['type'] == 'message':
                if 'subtype' in event_data["event"]:
                    return make_response("", 200)
                self.app.logger.info(event_data)
                command_data = event_data['event']['text'].strip()
                command_name = command_data.split(' ', 2)[0]
                command = Command(command_name, command_data, 'slack', event_data['team_id'])  # eh
                return self.cacophony.event(command)
            return make_response("", 200)
