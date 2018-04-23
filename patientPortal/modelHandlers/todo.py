from patientPortal.models import Todo
def fetch_todos(therapist_user):
    todo_list = therapist_user.todo_set.all();
    todos = todo_list.values()
    return todos;
