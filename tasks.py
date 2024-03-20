from invoke import task

@task
def test(ctx):
    ctx.run("pytest src/tests/test.py", pty=True)
 