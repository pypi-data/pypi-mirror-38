from invoke import task


@task
def publish(ctx):
    ctx.run('python3 setup.py sdist upload')
