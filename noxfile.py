import nox


@nox.session
def tests(session):
    session.install("pytest", "coverage")
    session.install(".")
    session.run("make", external=True)
