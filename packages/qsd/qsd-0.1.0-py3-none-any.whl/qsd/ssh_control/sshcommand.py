#!/usr/bin/env python
"""
sshcommand includes all of the necessary functions to interface with remote machines via the ssh protocol
"""

from subprocess import call
import os
import stat

class SSHCommand:
    """
        SSHCommand contains the necessary functions to generate bash files which create the ssh interfaces to remote machines
    """
    def __init__(self,host,*args,**kwargs):
        """
            :type: host = str
            :param: host = name of the machine you want to connect to

            :type: host_network str
            :param: host_network = network address of the remote machine

            :type: full_host = str
            :param: full_host = full network address, including host

            :type: user = str
            :param: user = username 

            :type: model = str
            :param: model = COMSOL model name

            :type: paramfile = str
            :param: paramfile = file containing parameters for COMSOL simulation

        """
        self.host = host
        self.host_network = kwargs('host_network',None) 
        self.full_host = self.host + "@" + self.full_host
        self.user = kawrgs.get('user',None)
        self.model = kwargs.get('model','cpw_vacuum_calcs.mph')
        self.paramfile = kwargs.get('paramfile',None)
        return

    def add_remote_machine(self):
        """
            Add a new remote machine to your ssh config file, and gennerate a secure key to share bnetyween your computer and the host machine.
        """
        file = open("keygen","w")
        file.write("#!/bin/bash")
        file.write("cd ~/.ssh\n")
        file.write("ssh-keygen\n")
        file.write("scp id_rsa %s:/~/.ssh/authorized-keys\n" % self.full_host)
        file.write("cd -\n")
        file.close()
        self.call_bash('keygen')

        sshfile = os.getenv("HOME") + '/.ssh/config'
        file = open(sshfile,"a")
        file.write("\n")
        file.write("Host %s\n" % self.host)
        file.write("    HostName %s\n" % self.host_network)
        file.write("    User %s\n" % self.user)
        file.write("    IdentityFile ~/.ssh/id_rsa")
        file.close()
        self.call_bash(sshfile)

    def upload_data(self):
        """
            Upload data to the remote machine
        """
        print("Uploading data to remote machine")
        
        filename = "upload_data" 
        filedir = os.getcwd() + "/" + filename
        file = open(filename,"w")
        file.write("#!/bin/bash\n")
        file.write("\n")
        file.write('filename = "set_comsol_data"\n')
        file.close()
        self.call_bash(filename)

    def run_comsol(self):
        """
            Run COMSOL on the remote machine
        """
        print("Running COMSOL on remote machine...")
    
        filename = "run_comsol"
        filedir = os.getcwd() + "/" + filename
        file = open(filedir,"w")
        file.write("#!/bin/bash\n")
        file.write("\n")
        file.write('HOST="%s"\n' % self.host)
        file.write('echo "Running COMSOL on ${HOST}"\n')
        file.write("ssh ${HOST} 'cd COMSOL_files && ./job input/cpw_vacuum_calcs.mph'; exit\n")
        file.close()
        self.call_bash(filename)
   
    def check_host_machine(self):
        """
            Check the file structure of the host machine to make sure that the necessary structure is created. If it hasn;t been previously, this script will create the necessary files and folders.
        """
        print("Checking host machine file structure")

        filename = "check_host"
        filedir = os.getcwd() + "/" + filename
        file = open(filedir,"w")
        file.write("#!/bin/bash\n")
        file.write("\n")
        file.write('HOST="%s"\n' % self.host)
        file.write("ssh ${HOST} '[ ! -d \"COMSOL_files\" ] && echo \"Creating remote folder structire\"&& mkdir COMSOL_files COMSOL_files/input COMSOL_files/output COMSOL_files/exports COMSOL_files/parameter_files;  exit'\n")
        file.write("scp %s ${HOST}:~/COMSOL_files/input/\n'"  % self.model)
        file.close()
        self.call_bash(filename)

    def set_comsol_data(self):
        print("Uploading comsol parameter files...")
        filename = "set_comsol_data"
        filedir = os.getcwd() + "/" + filename

        file = open(filedir,"w")
        file.write("#!/bin/bash\n")
        file.write("\n")
        file.write('MODELNAME="%s"\n' % self.model)
        file.write('PARAMFILE="${MODELNAME}.txt"\n')
        file.write('cp "%s" ${PARAMFILE}\n' % self.paramfile)
        file.write('scp ${PARAMFILE} %s:~/COMSOL_files/parameter_files\n' % self.host) 
        #file.write('scp ${PARAMFILE} %s:/homes/gjones/COMSOL_files/parameter_files\n' % self.host)
        file.write("\n")
        file.write('rm ${PARAMFILE}\n')
        file.close()
        self.call_bash(filename)
    
    def get_comsol_data(self):
        """
            Retrieve exported data from remote machine
        """
        print("Retrieving comsol datafiles...")
        
        down_dir = os.path.join(os.getcwd(), "downloads")
        if not os.path.exists(down_dir):
            os.mkdir(down_dir)

        filename = "get_comsol_data"
        filedir = os.getcwd() + "/" + filename
        file = open(filename,"w")
        file.write("#!/bin/bash\n")
        file.write("\n")
        file.write('HOST="gade"\n')
        file.write('REMOTEDIR="COMSOL_files/exports"\n')
        file.write('DOWNLOADDIR="%s"\n' % down_dir)
        file.write('scp -r ${HOST}:${REMOTEDIR} ${DOWNLOADDIR}\n')
        file.close()
        self.call_bash(filename)

    def upload_job_script(self):
        """
            Upload the batch job script to the remote machine
        """
        self.job()
        print("Uploading job script....")
        filename = "upload_job"
        filedir = os.getcwd() + "/" + filename
        file = open(filename,"w")
        file.write("#!/bin/bash\n")
        file.write("\n")
        file.write("chmod +xu job\n")
        file.write('scp job %s:~/COMSOL_files\n' %self.host)
        file.close()
        self.call_bash(filename)
        os.remove('job')

    def job(self):
        """
            Creates a batch job script on the remote machine to run COMSOL
        """
        filename = "job"
        filedir = os.getcwd() + "/" + filename
        file = open(filename,"w")
        file.write("#!/bin/bash\n")
        file.write("\n")
        file.write("MODELTOCOMPUTE=$@\n")
        file.write("INPUTFILE=\"${HOME}/COMSOL_files/${MODELTOCOMPUTE}\"\n")
        file.write("PARAMFILE=\"${HOME}/COMSOL_files/parameter_files/${MODELTOCOMPUTE#'input/'}.txt\"\n")
        file.write("OUTPUTFILE=\"${HOME}/COMSOL_files/output/${MODELTOCOMPUTE#'input/'}\"\n")
        file.write("BATCHLOG=\"${HOME}/COMSOL_files/logs/${MODELTOCOMPUTE}.log\"\n")
        file.write("JOB=\"b1\"\n")
        file.write("\n")
        file.write("# Get the parameters from the text file\n")
        file.write("declare -a NAMEARRAY VALUEARRAY DESCARRAY\n")
        file.write("let i=0 \n")
        file.write("while IFS=\" \" read -r name value description \n")
        file.write("do\n")
        file.write("   NAMEARRAY[i]=\"${name}\"\n")
        file.write("   VALUEARRAY[i]=\"${value}\"\n")
        file.write("   DESCARRAY[i]=\"${description}\"\n")
        file.write("   ((++i))\n")
        file.write("done < ${PARAMFILE}\n") 
        file.write("\n")
        file.write("# Concatenate string to remove whitespace and add commas after each element\n")
        file.write("NAMES=$(IFS=, eval 'echo \"${NAMEARRAY[*]}\"')\n")
        file.write("VALUES=$(IFS=, eval 'echo \"${VALUEARRAY[*]}\"')\n")
        file.write("DESC=$(IFS=, eval 'echo \"&{DESCARRAY[*]}\"')\n")
        file.write("\n")
        file.write("# run comsol directly from the command line. requires a user input for the input file\n")
        file.write("comsol batch -inputfile ${INPUTFILE} -outputfile ${OPUTPUTFILE} -pname ${NAMES} -plist ${VALUES} -job ${JOB}\n")
        file.write("mv on.* output/\n")

    def call_bash(self,filename):
        """
            Method to call created bash scripts with the subprocess module
        """
        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IEXEC)
        callname = './'+filename
        rc = call(callname)
        os.remove(filename)
