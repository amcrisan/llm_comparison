def cohere_query(client,
                 message = None,
                 preamble_override = None,
                 chat_history = []):
    response = client.chat(
        chat_history=chat_history,
        message=message,
        preamble_override=preamble_override,
        stream=False,
        return_chat_history=True)
    
    return(response)