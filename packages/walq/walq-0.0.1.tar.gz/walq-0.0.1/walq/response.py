class Response:
    def __init__(self, **attr):
        
        self.message=attr.get('message')
        self.condition=attr.get('condition')
        
        
    def getResponse(self, user_input):       
        if self.condition:
            return self.condition(user_input)
        else:
            return self.message
