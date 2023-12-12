#hf
from transformers import AutoTokenizer
from huggingface_hub import InferenceClient

from chat2Vis import format_response

def setup_codellama(endpoint_url=None,HF_API_KEY=None):
    # Streaming Client
    # ** warning - do no call the hf client, 'client' or it will inferfere with the openai client
    hf_inf = InferenceClient(endpoint_url, token=HF_API_KEY)

    # generation parameter
    gen_kwargs = dict(
        max_new_tokens=512,
        top_k=30,
        top_p=0.9,
        temperature=0.2,
        repetition_penalty=1.02,
    )

    return hf_inf, gen_kwargs

def format_prompt(convo,HF_API_KEY=None, primer = None):

    if(primer is not None):
        #need to remind code llama to write out
        #code each time :/
        idx = len(convo)-1 #appy to most recent utterance
        convo[idx]['content'] = f"{primer}\n{convo[idx]['content']}"
        
    #preping the prompt for Code LLama
    tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-Instruct-hf",token=HF_API_KEY)
    tokenizer.use_default_system_prompt = False
    prompt = tokenizer.apply_chat_template(convo, tokenize=False)

    return prompt

def call_codellama(convo,
                   hf_inf,
                   gen_kwargs,
                   primer=None,
                   primer_code=None):
    #calling Code LLama
    prompt = format_prompt(convo,primer)
    stream = hf_inf.text_generation(prompt, stream=False, details=True, **gen_kwargs)
    response = primer_code + format_response(stream.generated_text.strip())
    
    return response