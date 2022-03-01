# Program to merge pdfs
# Noah Rubin - October 2021

import glob
import PyPDF2


def create_merged_pdf(absolute_path, result_name, exclusion_files):
    """
    - Places all pdf files in one large pdf

    - Assumes the files you wish to place in a joint pdf are in alphabetical order
     e.g. '01_test.pdf' would come first in the joint pdf, then '02_test.pdf' then '03_test.pdf'

     - Assumes that pdfs you pass into `exclusion_files` are actually in that particular directory
     e.g. if you wish to exclude the files ['01_test.pdf', '02_test.pdf'], they must both exist in the directory you
     refer to

    Parameter: absolute_path (string)
    - The absolute path of where all the pdf documents are located

    Parameter: result_name (string)
    - The name of the final joint pdf

    Parameter: exclusion_files (list of strings)
    - A list of strings with the files not to include when joining. Specify `None` if you don't want to exclude anything
    """

    to_exclude = [] if exclusion_files is None else exclusion_files

    try:
        # Sort the files in ascending order, removing the ones you wish to exclude
        # But first accommodate for the fact that the user might include a '/' at the end of the absolute path
        if absolute_path.endswith('/'):
            all_files = sorted(glob.glob(f'{absolute_path}*.pdf'))
        else:
            all_files = sorted(glob.glob(f'{absolute_path}/*.pdf'))
        for exclusion_file in to_exclude:
            for file in all_files:
                if exclusion_file in file:
                    all_files.remove(file)

        # Create a result instance to apply methods to eventually
        result = PyPDF2.PdfFileMerger()

        # Loop through all files, appending each pdf to our result object
        for pdf in all_files:
            result.append(pdf)

        result.write(f'{absolute_path}/{result_name}')  # '//' is fine in the case where absolute_path[-1] == '/'.
        result.close()

    except (NotADirectoryError, FileNotFoundError):
        print('Please ensure the absolute path is specified correctly')


# This directory has ['SVM Part 1.pdf', 'SVM Part 2.pdf', 'SVM Part 3.pdf', 'SVM Part 4.pdf', 'SVM Part 5.pdf' etc.]
# ...which I will merge into a big pdf called 'Support_Vector_Machines.pdf'

create_merged_pdf('/Users/noahrubin/Desktop/test/',
                  'MATH2871 NOTES.pdf',
                  exclusion_files=None)