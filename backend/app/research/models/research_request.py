from pydantic import BaseModel

from backend.app.ai.llms.models import Message


class ResearchRequest(BaseModel):
    """
    Internal request model used by research workflows.
    """

    messages: list[Message]