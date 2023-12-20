import subprocess
import sys


def executeCMD(cmd):
    def execute(x):
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, x)

    for path in execute(cmd):
        print(path, end="")


# def executeCMDtfpy(cmd, *args, **kwargs):
#     capture_output = kwargs.pop('capture_output', True)
#     raise_on_error = kwargs.pop('raise_on_error', False)
#     if capture_output is True:
#         stderr = subprocess.PIPE
#         stdout = subprocess.PIPE
#     else:
#         stderr = sys.stderr
#         stdout = sys.stdout
#
#     cmds = self.generate_cmd_string(cmd, *args, **kwargs)
#     log.debug('command: {c}'.format(c=' '.join(cmds)))
#
#     working_folder = self.working_dir if self.working_dir else None
#
#     environ_vars = {}
#     if self.is_env_vars_included:
#         environ_vars = os.environ.copy()
#
#     p = subprocess.Popen(cmds, stdout=stdout, stderr=stderr,
#                          cwd=working_folder, env=environ_vars)
#
#     for stdout_line in iter(p.stdout.readline, ""):
#         yield stdout_line
#     p.stdout.close()
#     return_code = p.wait()
#     if return_code:
#         raise subprocess.CalledProcessError(return_code, cmds)