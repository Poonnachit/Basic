#!/usr/bin/env python
import subprocess
import filecmp

def grading_system(input,output ,fileName, fileLocation):

    write_path = "/home/BUU/64160038/Basic/uploads/output/"+fileName+".txt"
    testcase_path = "/home/BUU/64160038/Basic/static/labs/testcase/"+input
    answer_path = "/home/BUU/64160038/Basic/static/labs/testcase/"+output
    with open(write_path, "w+") as output, open(testcase_path, "r") as testcase:
        subprocess.call(["python3", fileLocation], stdin=testcase, stdout=output, stderr=output, timeout=2)
    if (filecmp.cmp(write_path, answer_path)):
        return True
    else:
        return False



def allowed_file_pdf(filename):
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file_py(filename):
    ALLOWED_EXTENSIONS = {'py'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file_txt(filename):
    ALLOWED_EXTENSIONS = {'txt'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

