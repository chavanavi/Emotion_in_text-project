import streamlit as st
import altair as alt
import  numpy as np
import pandas as pd 

import pickle
from win32com.client import Dispatch

def speak(text):
	speak=Dispatch(("SAPI.SpVoice"))
	speak.Speak(text)

pipe_lr =pickle.load(open("emotion_classifier_lr.pkl","rb"))

def predict_emtions(docx):
    result= pipe_lr.predict([docx])
    return result[0]

def get_prediction_proba(docx):
    result= pipe_lr.predict_proba([docx])
    return result

emotions_emoji_dict = {"anger":"😠","disgust":"🤮", "fear":"😨😱", "happy":"🤗", "joy":"😂", "neutral":"😐", "sad":"😔", "sadness":"😔", "shame":"😳", "surprise":"😮"}




def main():
    st.title("Emotion text ")
    menu=["Home","About"]
    choice =st.sidebar.selectbox("Menu",menu)

    if choice=="Home":
        st.subheader("Home Emotion Text")
        speak("Type Here Emotion Text")

        with st.form(key="emotion_Clr_from"):
            row_text = st.text_area("Type Here")
            submit_text = st.form_submit_button(label="Submit")
            
        
        if submit_text:
            col1,col2 =st.columns(2)

            prediction = predict_emtions(row_text)
            probability= get_prediction_proba(row_text)
            with col1:
                st.success("Original Text ")
                speak(" predict the Original Text ")
                st.write(row_text)

                st.success("Pridection")
                speak("Pridiction the emoji_icon")
                emoji_icon = emotions_emoji_dict[prediction]
                st.write("{}:{}".format (prediction,emoji_icon))
                st.write("Confidence:{}".format(np.max(probability)))
            
            with col2:
                st.success("Pridect  probability " )
                speak("Pridect probability")
                #st.write(probability)
                proba_df =pd.DataFrame(probability,columns=pipe_lr.classes_)
                #st.write(proba_df.T)
                proba_df_clean= proba_df.T.reset_index()
                proba_df_clean.columns=["emotionds","probability"]

                fig =alt.Chart(proba_df_clean).mark_bar().encode(x="emotionds",y="probability",color="emotionds")
                st.altair_chart(fig,use_container_width=True)



  
        
    else:
        st.subheader("About")
    
if __name__ =="__main__":
    main()