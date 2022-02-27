# A GUI version of pdf_merger.py
# Used some of the functionality from pdf_merger.py but the majority of this program is different
# Noah Rubin - 2022

import streamlit as st
from PyPDF2 import PdfFileMerger


# ======================================================================================================================
# list of uploaded files, making sure the end result is sorted
# This ensures that if we have 'file1.pdf' 'file2.pdf' and 'file3.pdf', the final merged pdf merges them in order
# ======================================================================================================================
def get_ordered_files(files):
    """Orders a list of PDF files by name"""
    sorted_files = sorted(
        list(zip(files, [f.name for f in files])),
        key=lambda x: x[1]
    )
    return [f[0] for f in sorted_files]


def show_files_being_merged(sorted_files):
    """A simple function to list the files being merged together (in order)"""
    st.write('Files Being Merged:')
    filenames = [f.name for f in sorted_files]
    for f in filenames:
        st.write(f)


def merge_pdfs(all_uploaded_files):
    """Takes many individual pdfs and merges them into one big one, counting how many were added in the process"""
    files_added = 0
    result = PdfFileMerger()
    for f in all_uploaded_files:
        result.append(f)
        files_added += 1
    return result, files_added


def load_pdf_for_download(name):
    """This is the final PDF to be passed into `st.download()`"""
    with open(f"{name}", "rb") as f:
        return f.read()


# ======================================================================================================================
# Main program
# ======================================================================================================================
st.markdown('# PDF Merger - Noah Rubin')

files_uploaded = st.file_uploader("Choose PDF files to merge together", type=['pdf'], accept_multiple_files=True)
ordered_files = get_ordered_files(files=files_uploaded)
show_files_being_merged(ordered_files)

final_pdf, file_count = merge_pdfs(ordered_files)
if file_count > 0:
    filename = st.text_input(label='Enter the name of your new PDF (please do not add the .pdf part)')
    if filename:
        filename = f'{filename}.pdf'

        # Save file so that we can reload it and access the streamlit download button method
        final_pdf.write(filename)

        # Download the file
        st.download_button(label=f"Download '{filename}'",
                           data=load_pdf_for_download(filename),
                           file_name=f'{filename}',
                           mime='application/octet-stream')
