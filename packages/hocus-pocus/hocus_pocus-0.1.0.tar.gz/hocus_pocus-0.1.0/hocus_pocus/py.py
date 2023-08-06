from invoke import task

from .util import safe_checkout


@task
def upload(ctx):
    # from twine.commands import upload
    print(
        "twine upload --repository-url https://$PYPI_SERVER --username $PYPI_USER --password $PYPI_SERVER_PW --skip-existing $WHEELHOUSE/*"
    )


@task(post=[upload])
def build(ctx):
    ctx.run("python setup.py sdist bdist_wheel")


@task(post=[upload])
def build_all_tags(ctx, repo):
    for tag in repo.tags:
        print(f"Building {tag}")
        with safe_checkout(tag):
            build(ctx)
