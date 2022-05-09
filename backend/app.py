from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute)
from flask_cors import CORS


class TodoModel(Model):
    """
    A Todo task
    """
    class Meta:
        table_name = 'todo-list'
        host = "http://localhost:8000"
    id = NumberAttribute(hash_key=True)
    task = UnicodeAttribute()


if TodoModel.exists():
    TodoModel.delete_table()    
TodoModel.create_table(read_capacity_units=1, write_capacity_units=1)


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)

CORS(app)

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})


class TodoDAO(object):
    def __init__(self):
        self.counter = TodoModel.count()
        if not self.counter:
            self.todos = []
        else:
            self.todos = [TodoModel.get(id) for id in range(1, self.counter + 1)]

    def get(self, id):
        try:
            # print(TodoModel.get(id))
            return TodoModel.get(id)
        except Exception as e:
             api.abort(404, "Todo {} doesn't exist".format(id))

        # for todo in self.todos:
        #     if todo['id'] == id:
        #         return todo
        # api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        self.counter += 1
        todo = TodoModel(self.counter, task=data['task'])
        todo.save()

        # todo = data
        # todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        # print(self.todos)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(
            actions=[
                TodoModel.task.set(data['task'])
            ]
        )
        ind = 0
        for t in self.todos:
            if t.id == todo.id:
                self.todos[ind].task = todo.task
                break
            ind += 1
        return todo

    def delete(self, id):
        todo = self.get(id)
        # print(todo, self.todos)
        ind = 0
        for t in self.todos:
            if t.id == todo.id and t.task == todo.task:
                self.todos.pop(ind)
                break
            ind += 1
        # self.todos.remove(todo)
        todo.delete()
        


DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)