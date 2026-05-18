from flask import Flask, jsonify, request

app = Flask(__name__)

todos = [
    {"id": 1, "task":"Learn Flask", "done":False},
    {"id": 2, "task":"Build a API", "done":False}
]


@app.route("/")
def home():
    return "Todo API is running!"

@app.route("/todos", methods=["GET"])
def gettodo():
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def create_todo():

    data = request.json

    new_todo = {
        "id": len(todos) + 1,
        "task": data["task"],
        "done": False
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201

@app.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):
    
    data = request.json

    for todo in todos:
        if todo["id"] == id:
            todo["task"] = data.get("task", todo["task"])
            todo["done"] = data.get("done", todo["done"])
            return jsonify(todo), 200
    return jsonify({"error": "Todo not found"}), 404

@app.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):

    for todo in todos:
        if todo["id"] == id:
            todos.remove(todo)
            return jsonify({"message": "Todo deleted"}), 200
    return jsonify({"error": "Todo not found"}), 404




if __name__ == "__main__":
    app.run(debug=True)
