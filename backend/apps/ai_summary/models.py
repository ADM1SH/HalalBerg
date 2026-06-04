"""
AI Summary app — no database model needed.
This app only provides the POST /api/ai/summarise/ endpoint
that pipes text to LM Studio's OpenAI-compatible API.
The summarised result is stored in NewsArticle.summary_ai by the caller.
"""
