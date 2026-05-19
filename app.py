from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return{
            "id": self.id,
            "task": self.task,
            "done": self.done
        }
    
with app.app_context():
    db.create_all()
    print("Tables created!")


# todos = [
#     {"id": 1, "task":"Learn Flask", "done":False},
#     {"id": 2, "task":"Build a API", "done":False}
# ]


@app.route("/")
def home():
    return "Todo API is running!"


@app.route("/todos", methods=["GET"])
def get_todo():
    todos = Todo.query.all()
    todo = [todo.to_dict() for todo in todos]
    return jsonify(todo)


@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.json
    new_todo = Todo(task=data["task"])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201


@app.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    data = request.json
    todo.task = data.get("task", todo.task)
    todo.done = data.get("done", todo.done)
    db.session.commit()
    return jsonify(todo.to_dict()), 200


@app.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Todo deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
