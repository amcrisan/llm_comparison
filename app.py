#app
import streamlit as st
import pandas as pd

#llms


#utils
import os
import sys
import io

#image handling
import io
import base64
from IPython import display
import matplotlib.pyplot as plt
from time import sleep

### variables
#list files in workspace/convos and extract the PIDs int o a list
pids = [file.split('_', 1)[0] for file in os.listdir('./workspace/convos')]
chunk_colors = ['#FFFF0050','#90ADC650','#9A463D60',"#FFAEBC80","#A0E7E550","#A0E7E5"]

df = pd.read_csv('./workspace/Titanic-Dataset.csv')



     
##################
# Main Chat
##################

st.set_page_config(layout="wide", page_title="LLM VA Agent Comparison")
st.set_option('deprecation.showPyplotGlobalUse', False)


with st.sidebar:
     st.title("LLM VA Agent Comparison")
     st.write("This tool visualizes visual analytic conversations between users and different Large Language Models (LLMs)")
     #streamlit create dropdown selector
     with st.expander("See Study Details"):
          st.write("The conversations being visualized in this chat are drawn from a prior Wizard of Oz study by Tory and Setlur (2019) entitled: Do What I Mean, Not What I Say! Design Considerations for Supporting Intent and Context in Analytical Conversation")
          st.markdown(f"Conversations are presented in the order that they occurred during the Wizard of Oz sessions. The particular conversational chunks are highlighted with a <span style='border:solid; border-radius:5px;margin-right:10px;background:#FFFF0050;padding:2px;'>Chunk</span> badge. Utterances within the same chunk represent a continuous conversational thread, usually refining a visualizations. Separate chunks are different conversational threads",unsafe_allow_html=True)

     pid = st.selectbox('Which conversation do you want to load?', pids)
     all_convo = st.toggle("Show full conversation", False)



     #display pandas df 
     convo = pd.read_pickle(f'./workspace/convos/{pid}_analytic_convo.pkl')
     #convo['revised'] = convo['content']


     #st.dataframe(convo)
     #display the conversation in turn

     if all_convo:
          show_convo = convo

     else:
          chunk_num = st.selectbox('Which chunk do you want to load?', convo['Chunk'].unique())
          show_convo = convo[convo['Chunk']==chunk_num]

#don't use grouping, it messes up the conversation order
#unique utterance ids
utterance_ids = show_convo['utt_id'].unique()

#keep context in chunk for Code Interpreter
#note that this doesn't work for all conversation option
if not all_convo:
     context = ''


# Display the conversation as is
view, edit = st.tabs(["View","Edit"])


with edit:
     #Edit errors and try to get the code running
     st.header("Welcome to edit mode!")
     st.caption("Here you can edit the code and see the results of your changes")

     # loading utterance and responses
     utterance_choice = st.selectbox('Which utterance do you want to load?', show_convo['Utterance'].unique())
     utt_id = show_convo[show_convo['Utterance']==utterance_choice]['utt_id'].values[0]

     #which model's reponse to you want to see?
     model_choice = st.selectbox('Which model\'s response do you want to see?', show_convo['model'].unique())
     
     #show the chat message
     with st.chat_message('user'):
          st.write(utterance_choice)
     
     col_view, col_execute = st.columns(2)

     idx = show_convo[(show_convo['model']==model_choice) & (show_convo['Utterance']==utterance_choice)].index

     with col_view:
          #st.code(show_convo['content'][idx].values[0])
          revised_code = st.text_area("Edit the code here", 
                       value=show_convo['revised'][idx].values[0],
                       height=750)
     with col_execute:
          try:
               st.pyplot(exec(revised_code))
               
               #automatically save code if it runs
               idx= convo[(convo['utt_id']==utt_id) & (convo['model']==model_choice)].index
               convo['revised'][idx] = revised_code
               convo.to_pickle(f'./workspace/convos/{pid}_analytic_convo.pkl')

          except:
               if revised_code.startswith("TEXT"):
                    st.write(revised_code)
               else:
                    #st.button("Save Revised Code",on_click = save_revised(convo,revised_code,utt_id,model_choice))
                    try:
                        st.code(exec(revised_code))
                    except:
                         st.error("failed to execute code")
                    

# Just view the conversation as is
with view:

     with st.spinner('Wait for it...'):
          st.cache_data.clear()
          sleep(3)
          st.empty()
          sleep(3)
           

     for utt_id in utterance_ids:
          utt = show_convo[show_convo['utt_id']==utt_id]
          user = utt[utt['role']=='user']
          assistants = utt[utt['role']=='assistant']
          
          with st.chat_message('user'):
               idx = user['Chunk'].values[0].item()-1
               st.markdown(f"<span style='border:solid; border-radius:5px;margin-right:10px;background:{chunk_colors[idx]};padding:2px;'>Chunk: {user['Chunk'].values[0]} </span>   {user['content'].values[0]}", unsafe_allow_html=True)
               
          with st.chat_message('assistant'):
               n_assistants = assistants.shape[0]
               st.write("Responses by model:")
               cols = st.columns(n_assistants)
               for i in range(n_assistants):
                    with cols[i]:
                         model = assistants['model'].values[i]
                         if model == "CI":
                              model = "🤖 Code Interpreter"
                         elif model == "gpt3":
                              model = "🤖 GPT-3"
                         elif model == "cohere":
                              model = "🤖 Cohere"
                         else:
                              model = "🦙 Code LLama"

                         st.markdown(f"<p style='text-align:center;'><strong>{model}</strong></p>", unsafe_allow_html=True)
                         
                         if assistants['content'].values[i].startswith("ERROR"):
                              st.write("Error Detected! Could not execute code")
                         elif assistants['content'].values[i].startswith("TEXT"):
                              st.write(assistants['content'].values[i])
                         else:

                              if model == "CI":
                                   try:
                                        st.pyplot(exec(assistants['content'].values[i]))
                                        context += assistants['content'].values[i]
                                   except:
                                        st.write("failed to executed CI code")
                              else:
                                   try: 
                                        st.pyplot(exec(assistants['revised'].values[i]))  
                                   except:
                                        st.code(assistants['revised'].values[i])





