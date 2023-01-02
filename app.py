# from db import DB
from data import *
import streamlit as st
from functions import *

# database = DB("creds.json","Data")

#hide_element("footer", "class", "css-1lsmgbg egzxvld0")


st.set_page_config(
    page_title="Arena Stats",
    layout="centered",
    page_icon=":crossed_swords:"
)
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def big_spacer(): st.markdown("#")
def small_spacer(): st.markdown("##")


if 'arena_data' not in st.session_state:
    st.session_state.arena_data = None


# ---------------------------------------------------------------------- #




st.markdown("# Arena Stats")
st.markdown("---")
small_spacer()

latest_button = st.button("Latest")
if latest_button:
    arena_data = format_latest_data(LATEST_DATA)
    arena_data = arena_data.replace(' ', '\n')
    data = cleanup_data(parse_csv(arena_data))
    st.session_state.arena_data = data
    st.success("Latest data loaded successfully.")


with st.form(key='import_form'):
    arena_data = st.text_input("Import string")
    submit_button = st.form_submit_button("Submit")
    if submit_button:
        st.success("Successfully imported data.")
        arena_data = arena_data.replace(' ', '\n')
        data = cleanup_data(parse_csv(arena_data))
        st.session_state.arena_data = data
        # database.push(data)
        # data_3v3 = get_3v3_matches(data)
        # st.write(data)



# big_spacer()


if st.session_state.arena_data is not None:
    big_spacer()
    st.write(st.session_state.arena_data)
    small_spacer()
    st.markdown("---")
    
    st.markdown("## Rating over time")
    small_spacer()
    st.markdown("### 2v2")
    small_spacer()
    st.pyplot(plot_rating(get_2v2_matches(st.session_state.arena_data), showEnemy=False))
    small_spacer()
    big_spacer()
    small_spacer()
    st.markdown("### 3v3")
    small_spacer()
    st.pyplot(plot_rating(get_3v3_matches(st.session_state.arena_data), showEnemy=False))

    
    small_spacer()
    st.markdown("---")
    big_spacer()
    
    
    
    st.markdown("## Comp win rates")
    small_spacer()
    st.markdown("### 2v2")
    small_spacer()
    
    data_2v2 = get_2v2_matches(st.session_state.arena_data)
    comps_2v2 = get_2v2_comps(data_2v2)
    winrates_2v2 = get_2v2_comps_winrates(data_2v2)
    for comp in winrates_2v2:
        classes = comp.split(',')
        for i in range(len(classes)):
            classes[i] = classes[i].title()
        col1a,col2a = st.columns(2)
        with col1a:
            st.write(f"{', '.join(classes)} - {winrates_2v2[comp]*100:.1f}%")
        with col2a:
            st.progress(winrates_2v2[comp])
    
    small_spacer()
    big_spacer()
    st.markdown("### 3v3")
    small_spacer()
    data_3v3 = get_3v3_matches(st.session_state.arena_data)
    comps = get_3v3_comps(data_3v3)
    winrates = get_3v3_comps_winrates(data_3v3)
    # st.write(get_3v3_comps_data(data_3v3))
    # st.write(winrates)
    # add a progress bar for each comp
    for comp in winrates:
        classes = comp.split(',')
        for i in range(len(classes)):
            classes[i] = classes[i].title()
        col1,col2 = st.columns(2)
        with col1:
            st.write(f"{', '.join(classes)} - {winrates[comp]*100:.1f}%")
        with col2:
            st.progress(winrates[comp])
        # st.write(f"{', '.join(classes)} - {winrates[comp]*100:.1f}%")
        # st.progress(winrates[comp])
