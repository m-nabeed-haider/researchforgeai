from __future__ import annotations

from typing import Any

import httpx


class HttpClient:
    """
    Thin wrapper around httpx.AsyncClient.

    Centralizes HTTP configuration for all external APIs.
    """

    def __init__(
        self,
        client: httpx.AsyncClient,
    ) -> None:

        self._client = client

    async def get(
        self,
        url: str,
        **kwargs: Any,
    ) -> httpx.Response:

        response = await self._client.get(
            url,
            **kwargs,
        )

        response.raise_for_status()

        return response

    async def post(
        self,
        url: str,
        **kwargs: Any,
    ) -> httpx.Response:

        response = await self._client.post(
            url,
            **kwargs,
        )

        response.raise_for_status()

        return response