from typing import Dict, Any

from team_actions.src.registration import fetch_available_actions


systems_info: Dict[str, Any] = {

    "task_tracker": {
        "description": "Manages tasks, issues, and projects (YouGile, Todoist).",
        "systems": {
            "YouGile": "YouGile - (eugene) is a task management app that organizes tasks into projects, "
                       "allows setting due dates, priorities, and creating sub-tasks. It supports collaboration, "
                       "custom filters, reminders, and tracks productivity across devices.",
            "Todoist": "кто этим вообще пользуется...",
        }
    },
    "llm_interaction": {
        "description": "Handles natural language requests to generate or transform text using various LLMs (Large "
                       "Language Models). This system processes user requests to create summaries, generate content, "
                       "answer questions, and perform other text-based tasks.",
        "systems": {
            "LLM": "A versatile language model that provides responses for a range of text generation tasks, "
                           "including summarization, content creation, question answering, and general assistance. It "
                           "adapts responses based on the user’s input and task requirements."
        }
    }
}

available_actions: Dict[str, Any] = fetch_available_actions()
