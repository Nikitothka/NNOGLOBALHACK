from pydantic_settings import BaseSettings


class BaseHackathonSettings(BaseSettings):
    user_token_from_tg_bot: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMWI0YTdiNzgtMTQwMi00NzEyLTkwYWYtMGE1NTQzYzE1YmUyIiwiZXhwIjoxNzMwNTg1NzE3Ljk1MzE1OSwiaXNzIjoiYmFja2VuZDphY2Nlc3MtdG9rZW4ifQ._8N8_IKre64K2I8VEQHH1IF23a2x2n4kb_B5vJxcPHY"
    save_auth_data_endpoint: str = "https://aes-agniachallenge-case.olymp.innopolis.university/save-authorization-data"


class TodoistAuthSettings(BaseSettings):
    todoist_oauth_api_url: str = "https://todoist.com/oauth/authorize/"
    todoist_token_exchange_api_url: str = "https://todoist.com/oauth/access_token/"
    todoist_redirect_url: str = "http://localhost:9000"
    todoist_client_id: str = "a8f77c90645a49d2a8a494d82054b344"
    todoist_scope: str = "task:add,data:read,data:read_write,data:delete"
    todoist_state: str = "some_secret_state"
    todoist_client_secret: str = "e0b2c69e4f1043df8cd5ea6052721420"


base_hackathon_settings = BaseHackathonSettings()
todoist_auth_settings = TodoistAuthSettings()