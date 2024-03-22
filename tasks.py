from invoke import task


@task
def start(ctx):
    ctx.run("poetry run python3 src/index.py")


@task
def test(ctx):
    ctx.run("pytest src/tests -v", pty=True)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src/tests && coverage report -m")
