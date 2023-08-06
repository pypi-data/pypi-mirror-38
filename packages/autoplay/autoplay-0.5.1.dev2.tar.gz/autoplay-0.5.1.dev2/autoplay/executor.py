import pkg_resources

from clitoo import context


def get_executor(executor_name):
    executors = pkg_resources.iter_entry_points('autoplay_executors')
    for entry in executors:
        if entry.name == executor_name:
            return entry.load()


class Executor:
    modes = ['run', 'dryrun']

    def __init__(self, schema, **options):
        self.command_count = 0
        self.job_count = 0
        self.exit_status = None
        self.mode = options.pop('mode', 'run')
        self.schema = schema
        self.stages = options.pop('stages', 'setup,script,clean').split(',')
        self.environment = options
        self.jobs = []
        self.job_names = []

    def load_job(self, name):
        self.job_names.append(name)
        self.jobs.append(self.get_commands(name))

    def get_commands_initial(self):
        dst_cmds = []
        for key, value in self.environment.items():
            dst_cmds.append(f'export {key}="{value}"')

        for key, value in self.schema.environment.items():
            if key in self.environment:
                continue
            dst_cmds.append(f'export {key}="{value}"')

        for key, value in self.doc.get('env', {}).items():
            dst_cmds.append(f'export {key}="{value}"')

        dst_cmds.append(f'export posargs="{" ".join(context.argv)}"')
        return dst_cmds

    def get_commands(self, name):
        deps = self.schema[name].get('requires', [])
        dst_cmds = self.get_commands_initial()
        for dep in deps:
            for stage in self.stages:
                cmds = self.schema[dep].get(stage, [])
                if not isinstance(cmds, list):
                    cmds = [cmds]

                dst_cmds += cmds

        for stage in self.stages:
            cmds = self.schema[name].get(stage, [])
            if not isinstance(cmds, list):
                cmds = [cmds]
            dst_cmds += cmds

        return dst_cmds

    def __call__(self):
        if self.job_count < len(self.jobs):
            self.job = self.jobs[self.job_count]
            getattr(self, self.mode)()
        else:
            self.clean()
        return self.return_value

    def wait(self):
        return True
