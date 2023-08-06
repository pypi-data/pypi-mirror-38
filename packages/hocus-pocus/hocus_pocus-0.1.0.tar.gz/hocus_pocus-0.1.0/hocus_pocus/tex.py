import os
import pathlib

from invoke import task

LATEX = "latexmk -pdf"


def needs_compile(target, sources):
    if not os.path.exists(target):
        return True

    return any(os.path.getmtime(target) < os.path.getmtime(s) for s in sources if s.is_file())


@task
def compile_latex(ctx, texfile=None, sources=(), latex=LATEX):
    if texfile is None:
        texfile = ctx.compile_latex.texfile
    texfile = pathlib.Path(texfile)
    # https://github.com/pyinvoke/invoke/issues/454
    with ctx.cd(str(texfile.parent)):
        target = texfile.with_suffix(".pdf")
        if needs_compile(target, (texfile,) + tuple(sources)):
            print(f"Compiling {texfile}")
            ctx.run(f"{latex} {texfile.name}")
    return target
