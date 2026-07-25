from fastapi import Request

from backend.app.core.container.container import Container


def get_container(
    request: Request,
) -> Container:

    return request.app.state.container