import nox


@nox.session
def tests(session):
    session.install("pytest", "coverage")
    session.install(".")
    session.run("make", external=True)


@nox.session
def doc(session: nox.Session) -> None:
    create_env_for_docs_build(session)
    session.run("pip", "install", ".")
    outdir = session.cache_dir / "docs_out"
    session.run("sphinx-build", "./docs/source",
                str(outdir), "--color", "-b", "html")
    index = (outdir / "index.html").resolve().as_uri()
    session.log(f"Documentation is available at {index}")


def create_env_for_docs_build(session: nox.Session) -> None:
    # session.run(
    #     "pip", "install", "docs/_vendor/domaintools"
    # )  # not done in requirements.txt due to the way relative paths are handled in that file (gh-pypa/pip#8765)
    session.run("pip", "install", "-r", "docs/requirements.txt")


@nox.session
def docs_preview(session: nox.Session) -> None:
    """Build a live preview of the documentation"""
    create_env_for_docs_build(session)
    # Editable install allows editing cocotb_bus source and seing it updated in the live preview
    session.run("pip", "install", "-e", ".")
    session.run("pip", "install", "sphinx-autobuild")
    outdir = session.cache_dir / "docs_out"
    session.run(
        "sphinx-autobuild",
        # Ignore directories which cause a rebuild loop.
        "--ignore",
        "*/source/master-notes.rst",
        "--ignore",
        "*/doxygen/*",
        # Also watch the cocotb source directory to rebuild the API docs on
        # changes to cocotb code.
        "--watch",
        "cocotb_bus",
        "./docs/source",
        str(outdir),
    )


@nox.session
def docs_linkcheck(session: nox.Session) -> None:
    """invoke sphinx-build to linkcheck the docs"""
    create_env_for_docs_build(session)
    session.run("pip", "install", ".")
    outdir = session.cache_dir / "docs_out"
    session.run(
        "sphinx-build",
        "./docs/source",
        str(outdir),
        "--color",
        "-b",
        "linkcheck",
    )


@nox.session
def docs_spelling(session: nox.Session) -> None:
    """invoke sphinx-build to spellcheck the docs"""
    create_env_for_docs_build(session)
    session.run("pip", "install", ".")
    outdir = session.cache_dir / "docs_out"
    session.run(
        "sphinx-build",
        "./docs/source",
        str(outdir),
        "--color",
        "-b",
        "spelling",
    )
