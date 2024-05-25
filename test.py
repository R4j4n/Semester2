import streamlit as st
from streamlit_pdf_viewer import pdf_viewer


if "pdf_upload" not in st.session_state:
    st.session_state.pdf_upload = None

if "view_pdf" not in st.session_state:
    st.session_state.view_pdf = None


if "pdf_file" not in st.session_state:
    st.session_state.pdf_file = None

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 500px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    messages = st.container(height=450)
    if prompt := st.chat_input("What would you like to do? upload or view"):
        messages.chat_message("user").write(prompt)
        if prompt == "upload":
            st.session_state.pdf_upload = True

            if st.session_state.pdf_file:
                messages.chat_message("assistant").write(
                    f"Thank you for uploading the pdf."
                )
        elif prompt == "view":
            if st.session_state.pdf_upload:
                st.session_state.view_pdf = True
                messages.chat_message("assistant").write(f"Ok, here is your PDF.")
            else:
                messages.chat_message("assistant").write(
                    f"Please Upload file before viewing."
                )

        else:
            messages.chat_message("assistant").write(f"Please Type 1")


if st.session_state.pdf_upload:
    st.session_state.pdf_file = st.file_uploader("Upload PDF file", type=("pdf"))


if st.session_state.pdf_upload and st.session_state.view_pdf:
    if st.session_state.pdf_file:
        binary_data = st.session_state.pdf_file.getvalue()
        pdf_viewer(input=binary_data, width=700)
