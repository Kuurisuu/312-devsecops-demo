from flask import Flask, request

app = Flask(__name__)


@app.get("/")
def home():
    return "Hola desde el pipeline de Jenkins!"


# Vulnerabilidad intencional para el laboratorio: XSS reflejado.
@app.get("/hello")
def hello():
    name = request.args.get("name", "visitante")
    return f"<h1>Hola, {name}!</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)