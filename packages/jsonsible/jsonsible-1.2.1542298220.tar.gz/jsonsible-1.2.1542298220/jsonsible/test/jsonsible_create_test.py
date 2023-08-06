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

    assert recapDict[0]['UNREACHABLE'] == '1'
    assert recapDict[0]['OK' ] == '0'

    assert recapDict[1]['UNREACHABLE'] == '1'
    assert recapDict[1]['OK' ] == '0'

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
