#!/usr/bin/env python
import subprocess


def run_file(fileName, fileLocation):
    try:
        with open(fileName+".txt", "w+") as output:
            subprocess.call(["python", fileLocation],
                            stdout=output, stderr=output, timeout=2)
            return True
    except:
        return False


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'py'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
