from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from extensions import db, bcrypt

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your-secret-key"

jwt = JWTManager(app)

db.init_app(app)
bcrypt.init_app(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def to_dict(self):
        return{
            "id": self.id,
            "task": self.task,
            "done": self.done,
            "user_id": self.user_id
        }

from auth import auth, User
app.register_blueprint(auth)

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
@jwt_required()
def get_todo():
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id=user_id).all()
    todo = [todo.to_dict() for todo in todos]
    return jsonify(todo)


@app.route("/todos", methods=["POST"])
@jwt_required()
def create_todo():
    data = request.json
    user_id = get_jwt_identity()
    new_todo = Todo(task=data["task"], user_id=user_id)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201


@app.route("/todos/<int:id>", methods=["PUT"])
@jwt_required()
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
@jwt_required()
def delete_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Todo deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
