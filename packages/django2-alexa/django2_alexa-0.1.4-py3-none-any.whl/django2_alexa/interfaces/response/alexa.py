import json

from django.http import HttpResponse

from django2_alexa.interfaces.response.output_speech import OutputSpeech
from django2_alexa.interfaces.response.cards import Card
from django2_alexa.utils import Directive


class AlexaResponse(HttpResponse):
    def __init__(self, output_speech: OutputSpeech = None, card: Card = None, reprompt: OutputSpeech = None,
                 end_session=True, directives: [Directive] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._output_speech = output_speech
        self._card = card
        self._reprompt = reprompt
        self._should_session_end = end_session
        self.directives = directives

        self.refresh_content()
        self["Content-Type"] = "application/json;charset=UTF-8"

    def refresh_content(self):
        d = {
            'version': "1.0",
            # TODO: 'sessionAttributes': None,
            'response': {
                'shouldEndSession': self._should_session_end,
                'directives': []
            }
        }
        if self._output_speech:
            d['response']['outputSpeech'] = self._output_speech.to_dict()
        if self._card:
            d['response']['card'] = self._card.to_dict()
        if self._reprompt:
            d['response']['reprompt'] = self._reprompt.to_dict()
        for directive in self.directives:
            d['response']['directives'].append(directive.to_dict())
        self.content = json.dumps(d).encode()

    @property
    def output_speech(self):
        return self._output_speech

    @output_speech.setter
    def output_speech(self, value):
        self._output_speech = value
        self.refresh_content()

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, value):
        self._card = value
        self.refresh_content()

    @property
    def reprompt(self):
        return self._reprompt

    @reprompt.setter
    def reprompt(self, value):
        self._reprompt = value
        self.refresh_content()

    @property
    def should_session_end(self):
        return self._should_session_end

    @should_session_end.setter
    def should_session_end(self, value):
        self._should_session_end = value
        self.refresh_content()
