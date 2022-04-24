import os

''''
def pip_install():
    """Automatically install requirements"""

    with cd(env.path):
        with prefix('source venv/bin/activate'):
            run('pip install -r requirements.txt')
'''

out = os.popen("pip install -r requirements.txt")

print(out.read())
