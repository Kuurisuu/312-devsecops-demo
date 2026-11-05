from flask import Flask

# Crea la aplicación web
app = Flask(__name__)


# Define la respuesta a una petición HTTP GET a la dirección principal
@app.get("/")
def home():
    return "Hola desde el pipeline de Jenkins!" # Mensaje desde el navegador


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) # Conexión desde cualquier lado | Escucha el puerto 5000