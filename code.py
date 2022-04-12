import json
import numpy as np
from sentence_transformers import SentenceTransformer 

from scipy.spatial.distance import cdist
import streamlit as st
import random
class Model():
    def process_intents(self,intent):
        for key in intent:
            if type(intent[key])!=type([]):
                intent[key]=[intent[key]]
        return intent
    def __init__(self,intents):
        self.intents=self.process_intents(json.load(open(intents)))
        self.model=SentenceTransformer('all-MiniLM-L6-v2') 
    def train(self):
        print("Generating features this may take a few moments depending on how big the intents file is")
        self.encodings=np.array(list(map(self.model.encode,list(self.intents.keys()))))
        print("features were successfully generated")
    
    def predict(self,input):
        encoding=self.model.encode(input)
        try:
            scores=1-cdist(self.encodings,encoding[np.newaxis,...])
        except:
            print("model was not trained")
            return
        return random.choice(list(self.intents.values())[np.argmax(scores)]),np.max(scores) 
@st.cache(suppress_st_warning=True)
def train():
    m=Model("intents.json")
    m.train()
    return m
model=train()  
def predict(x):
    return model.predict(x)[0]

import requests
#set title in streamlit
from googlesearch import search
import streamlit.components.v1 as components 
import random  
from quote import quote
from random_word import RandomWords 
r = RandomWords() 
@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def set_counter():
    print("resetted")
    return {"counter":0}
l=set_counter() 

@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def set_default_q():
    print("resettedq")
    return {"previous":"-"}
prev=set_default_q() 
def wrap_by_word(s, n):
    '''returns a string where \n is inserted between every n words'''
    a = s.split()
    ret = ''
    for i in range(0, len(a), n):
        ret += ' '.join(a[i:i+n]) + '\n'

    return ret
def get_random_quote():
    result=quote(r.get_random_word(),1)[0] 
    return f"{wrap_by_word(result['quote'],7)} by {result['author']}"

  
     
st.title('AI ChatBot') 
def check(url):
    if "jpg" in url or "png" in url:
        return False
    headers=requests.head(url).headers 
    if "X-Frame-Options" in headers:
        if headers["X-Frame-Options"]=="DENY" or headers["X-Frame-Options"]=="SAMEORIGIN":
            return False 
        return True 
    return True

text = st.text_input('Enter your text here') 

st.text("you : {}".format(text)) 
result=predict(text) 
if text!=prev["previous"]:
    l["counter"]=0 
prev["previous"]=str(text)
if result=="query":
  
  urls=list(search(str(text), num=20, stop=10, pause=2))

  nex=st.button("next") 
  f=True
  
  if nex or f: 
  
      for _ in range(19-l["counter"]): 
          if check(urls[l["counter"]]):
              print(l["counter"])
              URL=urls[l["counter"]] 
              l["counter"]+=1
              break 
          l["counter"]+=1
          
      components.iframe(URL,height=10000,width=700) 
      f=False
      
          
#write a function to get the weather   
elif result=="<action joke>": 
    st.text("bot : {}".format(requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&format=txt").text))
elif result=="<random quote>": 
    while True:
        try:
            q=get_random_quote() 
            break
        except: 
            pass
    st.text("bot : {}".format(get_random_quote()))  
elif result=="<action weather>":
    components.iframe('https://www.ventusky.com/',height=1000,width=3000) 
elif result=="<action news>":
    components.iframe('https://globalnews.ca/',height=10000,width=700)

else:
 
  st.text("bot : {}".format(result))
