from flask import Flask, jsonify

app = Flask(__name__)


def add(a: int, b: int) -> int:
    return a + b


@app.get("/")
def index():
    return jsonify(message="Hello from CI/CD!", status="ok")


@app.get("/health")
def health():
    return jsonify(status="healthy")


@app.get("/add/<int:a>/<int:b>")
def add_route(a: int, b: int):
    return jsonify(result=add(a, b))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
