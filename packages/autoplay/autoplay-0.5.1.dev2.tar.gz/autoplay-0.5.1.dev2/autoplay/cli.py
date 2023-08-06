'''
Bash orchestrator for yaml.

Lets you show, run a job or dryrun it.

Autoplay usage::

    autoplay
    autoplay show job
    autoplay dryrun job1 [jobN]
    autoplay run job1 [jobN] [envvar=value]

Example autoplay.yml::

    ---
    env:
      bar: foo
    ---
    name: test
    env:
      foo: bar
    script:
    - echo $foo
    - echo $bar
'''
import yaml

from autoplay import schema
from autoplay import executor

import clitoo

import colored


def _clitoo_setup():
    clitoo.context.schema = schema.Schema.cli()


def show(*jobs):
    '''
    Display job sources.
    '''
    for job in jobs if jobs else []:
        print(
            yaml.dump(
                clitoo.context.schema[job],
                default_flow_style=False,
            ),
        )


def run(*jobs, **kwargs):
    '''
    Execute commands for job.
    '''
    strategy = executor.get_executor(
        kwargs.pop('executor', 'linux')
    )(clitoo.context.schema, **kwargs)

    for name in jobs:
        strategy.load_job(name)

    strategy()
    return strategy.wait()


def ls():
    clitoo.help('autoplay.cli')
    print('')
    print(f'\n{colored.fg(208)}Found jobs in autoplay.yml:{colored.attr(0)}')
    print('')
    for i in clitoo.context.schema.keys():
        print(' -', i)
    print(f'\n{colored.fg(208)}Try autoplay show job_name{colored.attr(0)}')
    return


def _cli(*args):
    ''''''
    clitoo.context.default_module = 'autoplay.cli'
    clitoo.main(default_path='autoplay.cli.ls')
