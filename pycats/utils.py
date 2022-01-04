import subprocess

def execute(cmd, env_vars=None):
    popen = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
        universal_newlines=True,
        env=env_vars,
        shell=True
    )
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    # popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        _, stderr = popen.communicate()
        print(stderr)
        raise subprocess.CalledProcessError(return_code, cmd)