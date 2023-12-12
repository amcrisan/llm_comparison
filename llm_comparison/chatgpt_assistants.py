from time import sleep

def add_assistant_msg(client, 
                      message, 
                      thread_id):
    
    #assumes that message is a dictionary containing the role and content
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role=message['role'],
        content=message['content']
    )
    return(message)

def get_run_steps(client,
                  thread_id,
                  run_id,
                  OAI_FILE=None,
                  DATA_FILE='./workspace/Titanic-Dataset.csv'):
    
    #getting the code steps from the run
    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread_id,
        run_id=run_id
    )

    #stitching it together
    code=''
    for step in run_steps.data[::-1]:
        try:
            s = step.step_details.tool_calls[0].code_interpreter.input
            s = s.replace(OAI_FILE,DATA_FILE)
            code = code + "\n\n" + s
        except:        
            pass

    return code

def run_openai_assistant(client,
                         message,
                         thread_id,
                         a_id,
                         primer,
                         OAI_FILE = None,
                         code_only=True):
  
    #add new message to thread
    message = add_assistant_msg(client,message,thread_id)

    #create the run
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=a_id,
        instructions=primer
        )

    #get the response
    complete = False
    while not complete:
        run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run.id
        )
        if run.status == "completed":
            complete = True
        elif run.status not in ["in_progress","queued"]:
            raise Exception("Response failed to return")       
        else:
            sleep(5)

    #now that it is complete, get the message responses:
    messages = client.beta.threads.messages.list(thread_id=thread_id)  

    #code interpreter will provide an image file (latest file is always index 0)
    try:
        image=client.files.content(messages.data[0].content[0].image_file.file_id) 
    except:
        #if there is no image, return the messages
        #the most recent message is just text
        return messages, run 

    if code_only:
        return get_run_steps(client,thread_id,run.id,OAI_FILE)
    
    #return the message history and the content
    return messages, image.content, run