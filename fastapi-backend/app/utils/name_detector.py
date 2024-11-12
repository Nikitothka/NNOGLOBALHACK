import requests
from settings import headers, main_url

def get_user_id_by_name(user_name):
    response = requests.request("GET", main_url + 'users', headers=headers)
    user_id = next((user['id'] for user in response.json()['content'] if user['realName'] == user_name), None)
    print(user_id)

    return user_id

def get_column_id_by_name(column_name):
    response = requests.request("GET", main_url + 'columns', headers=headers)

    column_id = next((column['id'] for column in response.json()['content'] if column['title'] == column_name), None)
    print(column_id)
    return column_id

def get_task_id_by_name(task_name):
    response = requests.request("GET", main_url + 'tasks', headers=headers)

    task_id = next((column['id'] for column in response.json()['content'] if column['title'] == task_name), None)
    print(task_id)
    return task_id
