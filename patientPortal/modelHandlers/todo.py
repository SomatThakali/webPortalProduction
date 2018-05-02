from patientPortal.models import Todo
def fetch_todos(therapist_user):
    todo_list = therapist_user.todo_set.all();
    todos = todo_list.values()
    return todos;

def delete_todo(Unique_ID):
    t = fetch_todo(Unique_ID)
    t.delete()

def fetch_todo(Unique_ID):
    t = Todo.objects.get(Unique_ID=Unique_ID)
    return t;
