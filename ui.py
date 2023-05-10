import streamlit as st

from inference import infer, _setup

st.set_page_config(page_title="ViLT")


@st.cache_resource(show_spinner=True)
def setup():
    return _setup()


model, tokenizer, id2ans = setup()

st.title("ViLT - Visual Question Answering")
st.sidebar.title("Upload Image")

css = '''
<style>
    [data-testid="stSidebar"]{
        min-width: 600px;
        max-width: 800px;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

image = st.sidebar.file_uploader(
    "Choose an image", type=["jpg", "jpeg", "png"])
if image is not None:
    st.sidebar.image(image, use_column_width=False)

question = st.sidebar.text_input("Enter Question")

if st.sidebar.button("Submit"):
    result = infer(model, tokenizer, id2ans, question, image.read())

    if result:
        _, answer = result
        if image is not None:
            st.image(
                image, caption=f"Answer: {answer}", use_column_width=False)
