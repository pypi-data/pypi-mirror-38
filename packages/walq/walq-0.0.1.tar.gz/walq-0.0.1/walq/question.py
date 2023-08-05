class Question:
    def __init__(self, name, **attr):
        self.name=name
        self.attr=attr
        
        self.prompt = attr.get("prompt")
        self.options = attr.get("options")
        self.options_text = attr.get("options_text")
        self.next = attr.get("next")
        self.user_input_type = attr.get("input_type")
        self.response = None

    def __repr__(self):
        return str({self.name: {'prompt':self.prompt,
                            'options':self.options,
                            'options_text':self.options_text,
                            'next': self.next,
                            'user_input_type': self.user_input_type}
                })
        
        
    def getOptions(self):
        """
        Returns a dictionary mapping choices (int) to their respective texts.
        """
        if self.options is None: return None
        return { o:t for o,t in zip(self.options, self.options_text) }
    
        
    def isFinalQuestion(self):
        return True if self.next is None else False
    
        
    def respond(self, context):
        """
        Returns the response message (associated to the respective Response object)
        """

        if self.response is None:
            return None
        
        user_input=context.data['responses'][self.name]
        return self.response.getResponse(user_input)

    
    def getNextQuestionName(self, user_input):
        """
        Checks user input to determine the next question in the graph.
        """
        if self.next is None:
            return None
        
        if len(self.next)>1:
            return self.next[ self.options.index(user_input) ]
        else:
            return self.next[0]
        
    def promptMessage(self):
        """
        Properly formats a message to be prompted to the user.
        """
        if self.user_input_type=='choice':
            return f"{self.prompt} {self.getOptions()}"
        else:
            return self.prompt

    def parseUserInput(self, user_input):
        return { 
            'text':str, 
            'number':float, 
            'choice':int }[self.user_input_type]( user_input )
