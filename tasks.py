from invoke import task
from subprocess import call
from sys import platform

@task
def start(ctx):
    ctx.run("python src/index.py")

#@task
#def build(ctx):
#    ctx.run("python3 src/build.py", pty=True)

@task
def test(ctx):
    ctx.run("pytest src")

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src")

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")
    if platform != "win32":
        call(("xdg-open", "htmlcov/index.html"))

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src")

@task
def lint(ctx):
    ctx.run("pylint src")