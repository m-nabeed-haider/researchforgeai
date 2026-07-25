from enum import StrEnum


class ResearchStrategy(StrEnum):
    """
    Available research execution strategies.
    """

    DIRECT_LLM = "direct_llm"
    WEB_SEARCH = "web_search"