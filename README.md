python -m ipykernel install --user --name=my-virtualenv-name


Install github libraries inside the shell
pip install git+https://github.com/huggingface/transformers.git@main accelerate



'''
for chunk in convo:   
    for msg in chunk['utterances']:
        with st.chat_message('user'):
                    st.markdown(f"""<strong>Message Chunk : {chunk['chunk']}</strong>""",unsafe_allow_html=True)
                    st.markdown(msg)

        #response by each model type
        #GPT4, GPT3.5, CODE LLAMA, 

        with st.chat_message('assistant'):
            #tst = js.loads(execute_code_test())
            tst=execute_code_test()
            print(exec(tst['code']))
'''