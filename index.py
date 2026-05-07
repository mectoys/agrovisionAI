from flask import Flask, flash, redirect, render_template, request, session, url_for

from config import AppConfig

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")
@app.route("/")
def index():
    return render_template(
        "index.html",        use_datatables=False
    )


if __name__ == "__main__":
    app.run(host=AppConfig.HOST, port=AppConfig.PORT, debug=AppConfig.DEBUG)