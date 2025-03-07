from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

todos = []

@app.route('/')
def index():
    remaining_items = len([todo for todo in todos if not todo['completed']])
    return render_template('index.html', todos=todos, remaining_items=remaining_items)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        todos.append({'task': task, 'completed': False})
    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    del todos[task_id]
    return redirect(url_for('index'))

@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    todos[task_id]['completed'] = not todos[task_id]['completed']
    return redirect(url_for('index'))

@app.route('/clear_completed')
def clear_completed():
    global todos
    todos = [todo for todo in todos if not todo['completed']]
    return redirect(url_for('index'))

@app.route('/edit_task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    new_task = request.json.get('task')  
    if new_task:
        todos[task_id]['task'] = new_task  
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
