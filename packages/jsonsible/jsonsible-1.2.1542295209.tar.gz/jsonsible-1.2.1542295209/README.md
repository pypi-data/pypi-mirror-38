# Jsonsible
Python package to run an ansible-playbook and return the information from the recap in a json file

## Use
Install the python package
`pip install jsonsible`

```
from jsonsible import jsonsible_create

jsonsible_create(playbook='/Path/to/playbook.yml', stdout=False, fails=False, json=True, options={}, fail_finder=False)
```

## Parameters
**playbook**: *String* path the the playbook to run (./playbook.yml by defualt)

**stdout**: *Bool* keep a copy of the stdout from the ansible playbook (False by default)

**fails**: *Bool* create a file listing all ips that had a failure (False by default)

**json**: *Bool* create a json file containing the information described in the recap (True by default)

**options**: *Dict* a dict of flags and their parameters to be passed to the ansible playbook, flags that take no input should have a value of `""` in the dict (empty dict by default)
   ```
   options = {'--step': '', '--forks', '9'}

   jsonsible_create(options=options)
   ```

   runs: `ansible-playbook --step --forks 9 playbook.yml`

   * If you pass `options='input'` you will be prompted to enter the flags in the console

   ```
   jsonsible_create(options='input')
   Enter flags:
   --step --fork 9
   ```

   runs: `ansible-playbook --step --forks 9 playbook.yml`

**fail_finder**: *Bool* parse the entire stdout of the playbook run in order to add a list of the failed tasks under the key `FailedTasksId` to the recap dict and json (False by default)


## Output
By default, if you do not provide a path to a playbook this will look for a file called `playbook.yml` in the current directory.
  * `jsonsible_create` will do four things:
    * return a list of dicts of the information from the ansible recap
    * create a file called `recap.json` containing all information form the ansible recap if `json` is set to `True` (default)
    * create a file called `ansibleOutput.txt` containing the entire stdout of the ansible-playbook, removed at finish if stdout is set to `False` (default)
    * create a file called `fails.txt` that contains a list of ips that failed any ansible tasks if `fails` is set to  `True` (False by default)
