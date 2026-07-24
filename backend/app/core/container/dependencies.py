from backend.app.core.container.container import Container


container = Container()


def get_container() -> Container:
    return container