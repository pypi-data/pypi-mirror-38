import os
import re
import shlex
import shutil
import yaml

from processcontroller import ProcessController


def _find_config_file():
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f == 'clilabs-auto.yml' or \
               f == 'clilabs-auto.yaml':
                return os.path.join(root, f)


def _parse_file():
    file_path = _find_config_file()
    if not file_path:
        print('# Could not find any clilabs-auto configuration file')
        return None, None
    else:
        with open(file_path, 'r') as f:
            return file_path, yaml.load(f.read())


def _get_script(content, kwargs):
    if content and 'script' in content:
        script = content['script']
        if not script:
            return None
        for i, s in enumerate(script):
            for key, val in kwargs.items():
                script[i] = script[i].replace('${' + key + ':}', val)
            script[i] = re.sub('\$\{[^\${:}]*\:}', '', script[i])
            script[i] = shlex.split(script[i])
            script[i] = ' '.join(script[i])
        return script


def _run(script):
    proc = ProcessController()
    for shell in ['bash', 'sh']:
        shell_path = shutil.which(shell)
        if shell_path:
            return proc.run([shell_path, '-c', script])


def _execute(jobs, kwargs):
    path, content = _parse_file()
    if not content:
        if path:
            print(f'# No jobs found in {path}')
        return 1
    if not jobs:
        if len(content.keys()):
            print(f'# Jobs found in {path}:')
            for j in content.keys():
                print(f'#\t{j}')
        return 0
    for j in jobs.split(','):
        if j in content:
            print(f'# Running {j} job from {path}')
            script = _get_script(content[j], kwargs)
            if not script:
                print(f'# No script found for job {j}, ..aborting')
                return 1
            for s in script:
                print(s)
                if not _execute.debug:
                    retcode = _run(s)
                    if retcode:
                        return retcode
        else:
            print(f'# Job {j} not found, ..aborting')
            return 1
        print()
    return 0


def play(jobs=None, **kwargs):
    """Play automation Jobs

    This function will walk in current tree, looking for a file called
    'clilabs-auto.yml' or 'clilabs-auto.yaml'.
    The walk will stop at the first matching file.

    It will then parse it looking for jobs matching with the first param

    If no job is specified, it will print the list of jobs found in the
    clilabs-auto config file

    :param jobs: a coma separated list of jobs
    :param **kwargs: a list of variables to dynamically assign to job vars

    The variables must be in the form ${name:} in the config file
    They will be replaced by the value of the kwarg name=value

    Variables are optional and will be replaced by an empty string if
    they are not specified in the command line without throwing any errors

    Examples:

    clilabs auto:play   # list jobs
    clilabs auto:play flake8    # play job flake8
    clilabs auto:play flake8,pytest pip_opt=--user  # play jobs flake8 and
                                                    # pytest setting var
                                                    # pip_opt to '--user'
    """
    _execute.debug = False
    _execute(jobs, kwargs)


def debug(jobs=None, **kwargs):
    """Dry run of auto:play

    This function will only show what would have been done by the play function
    See play for more information:

    clilabs help auto:play
    """
    _execute.debug = True
    _execute(jobs, kwargs)
