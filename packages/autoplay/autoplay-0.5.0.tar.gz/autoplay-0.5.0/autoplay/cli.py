'''
Bash orchestrator for yaml.

Lets you run a job or dryrun it, or do just the setup/script/clean stage of
a job.

Autoplay usage:

    autoplay
    autoplay show job
    autoplay dryrun job1 [jobN]
    autoplay run job1 [jobN] [envvar=value]
'''
import pprint

from autoplay import schema
from autoplay import executor

import clitoo


def _clitoo_setup():
    clitoo.context.schema = schema.Schema.cli()


def show(*jobs):
    for job in jobs if jobs else []:
        pprint.pprint(clitoo.context.schema[job])


def run(*jobs, **kwargs):
    strategy = executor.get_executor(
        kwargs.pop('executor', 'linux')
    )(clitoo.context.schema, **kwargs)

    for name in jobs:
        strategy.load_job(name)

    strategy()
    return strategy.wait()


def ls():
    clitoo.help('autoplay.cli._cli')
    print('')
    print('# Found jobs in autoplay.yml:')
    print('')
    for i in clitoo.context.schema.keys():
        print(' -', i)
    return


def _cli(*args):
    clitoo.context.default_module = 'autoplay.cli'
    clitoo.main(default_path='autoplay.cli.ls')
