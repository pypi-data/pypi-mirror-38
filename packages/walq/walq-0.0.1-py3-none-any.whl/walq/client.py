from requests import put
import json

initial_question='q1'

class Client:
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint
        self.response=None

    
    def requestNextQuestion(self):
        if self.response is None:
            req_body_data = {'current_question':initial_question}

        else:
            req_body_data = self.response.json()
            nextQuestion = req_body_data.get('next_question')
            req_body_data.update({'current_question': nextQuestion })

        resp = put(self.api_endpoint, data=json.dumps( req_body_data ))
        if resp.status_code==200: 
            self.response=resp
        return resp

    def getMessage(self):
        return self.response.json().get('message')

    def send_input(self, inpt):
        req_body_data = self.response.json()
        req_body_data.update({'user_input':inpt}) 
        resp = put(self.api_endpoint, data=json.dumps( req_body_data ))   
        if resp.status_code==200: 
            self.response=resp
        return resp