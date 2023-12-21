def cohere_query(client,
                 message = None,
                 preamble_override = None,
                 chat_history = [],
                prompt_truncation='AUTO'):
    response = client.chat(
        chat_history=chat_history,
        message=message,
        preamble_override=preamble_override,
        stream=False,
        return_chat_history=True,
        prompt_truncation=prompt_truncation)
    
    return(response)