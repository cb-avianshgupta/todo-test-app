<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Todos</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.todo-modal>Add Todo </button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Id</th>
              <th scope="col">Task</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="todo in todos" :key="todo.id">
              <td>{{todo.id}}</td>
              <td>{{todo.task}}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    v-b-modal.todo-update-modal
                    @click="editTodo(todo)">
                    Update
                  </button>
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="onDeleteTodo(todo)">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addTodoModal"
         id="todo-modal"
         title="Add a new todo"
         hide-footer>
  <b-form @submit="onSubmit" @reset="onReset" class="w-100">
    <b-form-group id="form-task-group"
                  label="Task:"
                  label-for="form-task-input">
        <b-form-input id="form-task-input"
                      type="text"
                      v-model="addTodoForm.task"
                      required
                      placeholder="Enter task description">
        </b-form-input>
      </b-form-group>
    <b-button type="submit" variant="primary">Submit</b-button>
    <b-button type="reset" variant="danger">Reset</b-button>
  </b-form>
</b-modal>
<b-modal ref="editTodoModal"
         id="todo-update-modal"
         title="Update"
         hide-footer>
  <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
    <b-form-group id="form-task-edit-group"
                  label="Task:"
                  label-for="form-task-edit-input">
        <b-form-input id="form-task-edit-input"
                      type="text"
                      v-model="editForm.task"
                      required
                      placeholder="Enter task description">
        </b-form-input>
      </b-form-group>
    <b-button-group>
      <b-button type="submit" variant="primary">Update</b-button>
      <b-button type="reset" variant="danger">Cancel</b-button>
    </b-button-group>
  </b-form>
</b-modal>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      todos: [],
      addTodoForm: {
        id: 0,
        task: '',
      },
      editForm: {
        id: '',
        task: '',
      },
    };
  },
  methods: {
    getTodos() {
      const path = 'http://127.0.0.1:5000/todos';
      axios.get(path)
        .then((res) => {
        //   console.log(res);
          this.todos = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addTodo(payload) {
      const path = 'http://127.0.0.1:5000/todos/';
      axios.post(path, payload)
        .then(() => {
          this.getTodos();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getTodos();
        });
    },
    initForm() {
      this.addTodoForm.id = 0;
      this.addTodoForm.task = '';
      this.editForm.id = 0;
      this.editForm.task = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addTodoModal.hide();
      //   let read = false;
      //   if (this.addTodoForm.read[0]) read = true;
      const payload = {
        id: this.addTodoForm.id,
        task: this.addTodoForm.task,
      };
      this.addTodo(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addTodoModal.hide();
      this.initForm();
    },
    editTodo(todo) {
      this.editForm = todo;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editTodoModal.hide();
      //   let read = false;
      //   if (this.editForm.read[0]) read = true;
      const payload = {
        id: this.editForm.id,
        task: this.editForm.task,
      };
      this.updateTodo(payload, this.editForm.id);
    },
    updateTodo(payload, TodoID) {
      const path = `http://127.0.0.1:5000/todos/${TodoID}`;
      axios.put(path, payload)
        .then(() => {
          this.getTodos();
        })
        .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
          this.getTodos();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editTodoModal.hide();
      this.initForm();
      this.getTodos();
    },
    removeTodo(todoID) {
      const path = `http://127.0.0.1:5000/todos/${todoID}`;
      axios.delete(path)
        .then(() => {
          this.getTodos();
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
          this.getTodos();
        });
    },
    onDeleteTodo(todo) {
      this.removeTodo(todo.id);
    },
  },
  created() {
    this.getTodos();
  },
};
</script>
