from invoke import task


@task
def start(ctx):
    ctx.run("poetry run python3 src/index.py")


@task
def argstart(ctx, amount=5, room_min_size=2, room_max_size=4, room_exact_size=0, can_overlap=False, map_size_x=20, map_size_y=20):
    if can_overlap:
        can_overlap = "--can-overlap"
    else:
        can_overlap = ""
    ctx.run(
        f"poetry run python3 src/index.py \
        --amount={amount} \
        --room-min-size={room_min_size} \
        --room-max-size={room_max_size} \
        --room-exact-size={room_exact_size} \
        {can_overlap} \
        --map-size-x={map_size_x} \
        --map-size-y={map_size_y}")


@task
def lint(ctx):
    ctx.run("poetry run python -m pylint src", pty=True)


@task
def test(ctx):
    ctx.run("poetry run pytest src/tests/test_dijkstra.py -vv", pty=True)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest && coverage report -m")
