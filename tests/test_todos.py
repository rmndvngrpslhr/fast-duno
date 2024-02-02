from fast_duno.models import ToDoState
from tests.factories import ToDoFactory


def test_create_todo(client, token):
    response = client.post(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test To Do',
            'description': 'Test To Do description',
            'state': 'draft',
        },
    )

    assert response.json() == {
        'id': 1,
        'title': 'Test To Do',
        'description': 'Test To Do description',
        'state': 'draft',
    }


def test_list_todos(session, client, user, token):
    session.bulk_save_objects(ToDoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['todos']) == 5


def test_list_todos_pagination(session, user, client, token):
    session.bulk_save_objects(ToDoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 2


def test_list_todos_filter_title(session, user, client, token):
    session.bulk_save_objects(
        ToDoFactory.create_batch(5, user_id=user.id, title='Test To Do 1')
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test To Do 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 5


def test_list_todos_filter_description(session, user, client, token):
    session.bulk_save_objects(
        ToDoFactory.create_batch(
            5,
            user_id=user.id,
            description='Test description',
        )
    )
    session.commit()

    response = client.get(
        '/todos/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 5


def test_list_todos_filter_state(session, user, client, token):
    session.bulk_save_objects(
        ToDoFactory.create_batch(5, user_id=user.id, state=ToDoState.draft)
    )
    session.commit()

    response = client.get(
        '/todos/?state=draft', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['todos']) == 5


def test_list_todos_filter_combined(client, session, user, token):
    session.bulk_save_objects(
        ToDoFactory.create_batch(
            5,
            user_id=user.id,
            title='Test ToDo combined 1',
            description='combined test description',
            state=ToDoState.done,
        )
    )

    session.bulk_save_objects(
        ToDoFactory.create_batch(
            3,
            user_id=user.id,
            title='Test ToDo combined 2',
            description='combined test description',
            state=ToDoState.todo,
        )
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test ToDo combined 1&description=combined test description&status=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 5


def test_patch_todo_error(client, token):
    response = client.patch(
        '/todos/10', json={}, headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}


def test_patch_todo(session, client, user, token):
    todo = ToDoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'teste para o "patch"!'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json()['title'] == 'teste para o "patch"!'


def test_delete_todo(session, client, user, token):
    todo = ToDoFactory(id=1, user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert response.json() == {'detail': 'Task has been deleted successfully.'}


def test_delete_todo_error(client, token):
    response = client.delete(
        f'/todos/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found.'}
