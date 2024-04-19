from invoke import task


@task
def start(ctx):
    ctx.run("poetry run python3 src/index.py")


@task
def lint(ctx):
    ctx.run("poetry run python -m pylint src", pty=True)


@task
def test(ctx):
    ctx.run("poetry run pytest -vv", pty=True)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest && coverage report -m")
