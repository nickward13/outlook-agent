import auth
import asyncio, datetime
from msgraph.generated.users.users_request_builder import UsersRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from dateutil import parser

class ToDo:

    def __init__(self):
        self.scopes = ["User.Read", "Tasks.ReadWrite"]
        self.client = auth.get_graph_client(self.scopes)

    def __str__(self):
        return f"{self.title} ({self.status})"

    def is_today(self):
        if self.due_date_time:
            due_date = parser.parse(self.due_date_time)
            return due_date.date() == datetime.date.today()
        return False
    
    async def get_task_lists(self):
        lists = await self.client.me.todo.lists.get()
        return lists.value

    async def get_all_tasks(self, list_id):
        tasks = await self.client.me.todo.lists.by_todo_task_list_id(list_id).tasks.get()
        return tasks.value

    async def get_current_tasks(self, list_id):
        query_params = UsersRequestBuilder.UsersRequestBuilderGetQueryParameters(
            filter=f"status eq 'notStarted' or status eq 'inProgress'",
        )
        request_configuration = RequestConfiguration(
            query_parameters=query_params,
        )
        tasks = await self.client.me.todo.lists.by_todo_task_list_id(list_id).tasks.get(
            request_configuration=request_configuration,
        )
        return tasks.value

    async def get_current_tasks_for_default_list(self):
        lists = await self.get_task_lists()
        tasks = await self.get_current_tasks(lists[0].id)
        return tasks


async def main():
    todo = ToDo()
    lists = await todo.get_task_lists()
    #tasks = await todo.get_all_tasks(lists[0].id)
    #print(f"Tasks in list {lists[0].display_name}: {len(tasks)}")
    current_tasks = await todo.get_current_tasks(lists[0].id)
    print(f"Current tasks in list {lists[0].display_name}: {len(current_tasks)}")
    
asyncio.run(main())
