import os
import re
import sys
import json
import stat
from subprocess import call
from datetime import datetime

def jsonsible_create(playbook='./playbook.yml', stdout = False, fails = False, json = True, options={}, fail_finder=False):

    info = {}
    info['playbook'] = playbook
    info['stdout'] = stdout
    info['fails'] = fails
    info['json'] = json
    info['options'] = options
    info['fail_finder'] = fail_finder
    jsonsible = Jsonsible(info)
    ansible_dict = jsonsible.create_jsonsible()

    return ansible_dict


class Jsonsible(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, info):
        for key in info.keys():
            self[key] = info[key]
        self.failedIPs = []
        self.infoDicts = []
        self.time = None

    # create a json file from self.infoDicts and return self.infoDicts
    def create_jsonsible(self):

        # create script to run anisble-playbook and pipe stdout to text file
        bashScript = open('ansible.sh', 'w+')
        if self.options == 'input':
            print('Enter the flags for this ansible-playbook: ')
            flags = input()
            script = self.script_builder_with_input(flags)
            bashScript.write(script)
        elif self.options != {}:
            script = self.script_builder()
            bashScript.write(script)
        else:
            bashScript.write('#!/bin/bash\nansible-playbook $1 | tee ansibleOutput.txt')
        bashScript.close()
        os.chmod('ansible.sh', 0o777)
        call(['./ansible.sh', self.playbook])

        # open the stdout file
        ansibleOutput = open('ansibleOutput.txt', 'r')

        # parse the ansible recap
        self.parse_recap(ansibleOutput)

        if self.fail_finder:
            self.failed_task_finder(ansibleOutput)

        # close file
        ansibleOutput.close()

        self.time = datetime.now()

        # put all ips with failures in a list
        if self.fails:
            self.create_fails()

        # json of the playbook recap information
        if self.json:
            recap = open('recap_%0.2d:%0.2d:%0.2d.json' % (self.time.hour, self.time.minute, self.time.second), 'w+')
            recap.write(json.dumps(self.infoDicts))
            recap.close
        
        # delete stdout unless specified
        if not self.stdout:
            os.remove('ansibleOutput.txt')
        else:
            os.rename('ansibleOutput.txt', 'ansibleOutput_%0.2d:%0.2d:%0.2d.txt' % (self.time.hour, self.time.minute, self.time.second))

        # delete script
        os.remove('ansible.sh')

        return self.infoDicts


    # parse the stdout of an ansible-playbook and add dicts to self.infoDicts
    def parse_recap(self, ansibleOutput):
        # open stdout text file and go to first line
        line = ansibleOutput.readline()

        # get cursor down to the play recap
        while 'PLAY RECAP' not in line:
            line = ansibleOutput.readline()

        # got to the first recap line
        line = ansibleOutput.readline()

        # go through all recap lines
        while line != '\n':
            words = line.split()
            for word in words:
                if 'ok' in word:
                    ok = word.split('=')
                if 'changed' in word:
                    changed = word.split('=')
                if 'unreachable' in word:
                    unreachable = word.split('=')
                if 'failed' in word:
                    failed = word.split('=')

            # add ip to list for failures
            if failed[1] != '0' or unreachable[1] != '0': 
                self.failedIPs.append(words[0])
            
            infodict = dict([('IP', words[0]), ('OK', ok[1]), ('CHANGED', changed[1]), ('UNREACHABLE', unreachable[1]), ('FAILED', failed[1])])

            self.infoDicts.append(infodict)
            line = ansibleOutput.readline()

    # create a text file with list of failed or unreachable IPs
    def create_fails(self):
        fails = open('fails_%0.2d:%0.2d:%0.2d.txt' % (self.time.hour, self.time.minute, self.time.second), 'w+')
        if len(self.failedIPs) > 0:
            for fail in self.failedIPs:
                fails.write(str(fail) + '\n')
        else:
            fails.write("no failures")
        fails.close

    # create ansible-playbook call with self.options
    def script_builder(self):
        script = "#!/bin/bash\nansible-playbook "
        for key in self.options.keys():
                script += str(key) + " " +str(self.options[key])
                if self.options[key] != '':
                    script += " "
        script += "$1 | tee ansibleOutput.txt"
        return script

    # create ansible-playbook call with user provided input for self.options
    def script_builder_with_input(self, flags):
        script = "#!/bin/bash\nansible-playbook " + flags + " $1 | tee ansibleOutput.txt"
        print(script)
        return script

    # add key to dictionary about the task that has been failed
    def failed_task_finder(self, ansibleOutput):
        print('######### Parsing for Failures ############')
        ansibleOutput.seek(0, 0)
        line = ansibleOutput.readline()

        for host in self.infoDicts:
            host['FailedTasksId'] = []

        task_num = 0
        while 'RECAP' not in line:
            line = ansibleOutput.readline()
            if 'TASK' in line:
                task_num += 1
            while 'TASK' not in line:
                if 'fatal' in line and 'FAILED' in line:
                    ip = self.parse_line_ip(line)
                    for host in self.infoDicts:
                        if host['IP'] == ip:
                            host['FailedTasksId'].append(task_num)
                    break
                else:
                    break

    def parse_line_ip(self, line):
        ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )
        return ip[0]