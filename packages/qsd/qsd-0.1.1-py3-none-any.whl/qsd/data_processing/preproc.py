#!/usr/bin/env python
"""
Method to upload data to remote machine
"""
from subprocess import call

class PreProc:
    """
    Preprocessing methods
    """
    def upload_data(self):
        """
        Upload data to remote machine
        """
        rc = call("./upload_data")

