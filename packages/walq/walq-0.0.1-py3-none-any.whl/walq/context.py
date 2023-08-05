#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Future: json context could look like { 'persistent_items': {...}, 'volatile_items': {...} }
persistent_items: should be passed back and forth in all interactions. ex: user_responses
volatile_items: Only make sense for a given, particular interaction. ex: current_question, next_question, message, input_type, input
"""


class Context:
    # TODO: After receiving user input, should send next question in the response
    def __init__(self, **data):
        self.data=data
        if self.data.get('responses') is None:
            self.data['responses']={}

    @classmethod
    def from_json_data(cls, datadict):
        return cls(**datadict) 
    
    def get_current_question(self):
        return self.data.get('current_question')

    def get_user_input(self):
        return self.data.get('user_input','')

    def set_user_input(self,user_input):
        self.data['user_input']=user_input

    def set_current_question(self, current_question):
        self.data['current_question']=current_question

    def clear_user_input(self):
        self.data['user_input']=''

    def update(self, data):
        self.data.update(data)

