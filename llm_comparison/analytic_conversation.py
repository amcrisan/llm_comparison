from pandas import DataFrame

class analytic_conversation:
    def __init__(self,pid,history=[]):
        self.pid = pid
        self.history = history
    
    def add_utterance(self,utterance,utt_id):
        utterance = [{'role':'user','model': '', 'content':utterance,'utt_id':utt_id}]
        self.history+= utterance

    
    def add_response(self,utt_id,responses):
        '''
        responses should be a dictionary object where:
        * each key is a model containing
        * the code it executed 
        '''        
        assistant_resp = []

        for key in responses.keys():
            tmp = [{'role':'assistant','model': key, 'content':responses[key],'utt_id':utt_id}]
            assistant_resp +=tmp
            
        self.history+= assistant_resp
    
    def return_filtered_history(self, model_type='',include_system=True):
        ''' return the chat history filtered by a specific model'''

        if model_type == '':
            return(self.history)
        
        filtered_conversation = []
        for item in self.history:
            if item['role'] in ['user','system']:
                if include_system:
                    #some APIs like to have the system command handled separtely
                    filtered_conversation+=[{'role':item['role'],'content':item['content']}]
                elif item['role'] == 'user':
                    #if skipping the system command, then only add the user role
                    filtered_conversation+=[{'role':item['role'],'content':item['content']}]

            elif item['role'] == 'assistant':
                if item['model'] == model_type:
                    filtered_conversation+=[{'role':item['role'],'content':item['content']}]

        return(filtered_conversation)
    
    def to_df(self):
        return(DataFrame(self.history))
    
    def __repr__(self):
        return(f"Analytic Conversation for PID: {self.pid}")