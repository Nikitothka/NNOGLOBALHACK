from team_actions.src.utils.action_router import ActionRouter

# Import actions module for new system here
from team_actions.src.actions.YouGile import actions as yougile_actions
from team_actions.src.actions.LLM import actions as llm_actions


ActionRouter.add_actions_for_module(yougile_actions)
ActionRouter.add_actions_for_module(llm_actions)

# Keep it as is
action_router = ActionRouter()