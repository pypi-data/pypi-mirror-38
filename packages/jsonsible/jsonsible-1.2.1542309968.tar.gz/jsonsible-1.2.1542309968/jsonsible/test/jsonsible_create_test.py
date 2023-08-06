import pytest
import os
from jsonsible.jsonsible import Jsonsible

PATH = os.path.dirname(os.path.realpath(__file__))

def test_dict_len():
    jsonsibleObject = Jsonsible({})
    twoUreachable = open(str(PATH) + '/unreachable.txt', 'r')
    jsonsibleObject.parse_recap(twoUreachable)
    recapDict = jsonsibleObject.infoDicts

    # dict should have IP, OK, CHANGED, UNREACHABLE, FAILED
    assert len(recapDict[0]) == 5
    assert len(recapDict[1]) == 5

def test_dict_contents():
    jsonsibleObject = Jsonsible({})
    twoUreachable = open(str(PATH) + '/unreachable.txt', 'r')
    jsonsibleObject.parse_recap(twoUreachable)
    recapDict = jsonsibleObject.infoDicts

    assert recapDict[0]['unreachable'] == '1'
    assert recapDict[0]['ok' ] == '0'

    assert recapDict[1]['unreachable'] == '1'
    assert recapDict[1]['ok' ] == '0'

def test_script_builder():
    jsonsibleObject = Jsonsible({})
    jsonsibleObject.options = {'--step': '', '--forks': '8'}
    script = jsonsibleObject.script_builder()
    assert script == "#!/bin/bash\nansible-playbook --step --forks 8 $1 | tee ansibleOutput.txt"

def test_script_build_with_input():
    jsonsibleObject = Jsonsible({})
    flags = "--step --forks 8"
    script = jsonsibleObject.script_builder_with_input(flags)
    assert script == "#!/bin/bash\nansible-playbook --step --forks 8 $1 | tee ansibleOutput.txt"

def test_fail_finder_dict_len():

    jsonsibleObject = Jsonsible({'fail_finder': True})
    stdout = open(str(PATH) + '/large_fail_finder_output.txt')
    jsonsibleObject.parse_recap(stdout)
    jsonsibleObject.failed_task_finder(stdout)
    recapDicts = jsonsibleObject.infoDicts

    for recap in recapDicts:
        assert len(recap.keys()) == 6

def test_fail_finder_adding_to_failedTaskId():
    jsonsibleObject = Jsonsible({'fail_finder': True})
    stdout = open(str(PATH) + '/large_fail_finder_output.txt')
    jsonsibleObject.parse_recap(stdout)
    jsonsibleObject.failed_task_finder(stdout)
    recapDicts = jsonsibleObject.infoDicts

    for recap in recapDicts:
        if recap['failed'] != '0':
            assert len(recap['failedTasksId']) > 0
        else:
            assert len(recap['failedTasksId']) == 0

def test_parse_line_ip():
    jsonsibleObject = Jsonsible({})
    line = 'fatal: [10.228.181.151]: UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: ssh: connect to host 10.228.181.151 port 22: Connection timed out\r\n", "unreachable": true}'
    ip = jsonsibleObject.parse_line_ip(line)
    assert ip == '10.228.181.151'
