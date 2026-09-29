"""Website and API routes."""

from flask import Flask, Response, jsonify, request

from hello_web.greeting import greeting


def create_app() -> Flask:
    app = Flask(__name__, static_folder="public", static_url_path="/static")

    @app.get("/")
    def index():
        return app.send_static_file("index.html")

    @app.get("/style.css")
    def stylesheet():
        return app.send_static_file("style.css")

    @app.get("/app.js")
    def browser_script():
        return app.send_static_file("app.js")

    @app.get("/health")
    def health():
        return jsonify(status="ok", stack="python")

    @app.get("/api/greet")
    def greet():
        try:
            return Response(greeting(request.args.get("name", "")), mimetype="text/plain")
        except ValueError as error:
            return Response(str(error), status=400, mimetype="text/plain")

    @app.after_request
    def add_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    return app
