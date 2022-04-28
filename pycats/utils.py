import sys, subprocess


def subproc_stout(cmd):
    with open(f'/tmp/cat.log', 'wb') as f:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            sys.stdout.write(line.decode('utf-8'))
            f.write(line)
    f.close()


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


# For Project CI/CD
def build_software():
    build_block = f"""
    pip3 install -r requirements.txt
    python3 setup.py sdist bdist_wheel
    pip3 install dist/pycats-0.0.0-py3-none-any.whl --force-reinstall
    venv-pack -o venv.tar.gz --force
    """
    build_cmds = [i for i in build_block.split("\n") if i]
    for cmd in build_cmds:
        for path in execute(cmd):
            print(path, end="")
    return build_cmds