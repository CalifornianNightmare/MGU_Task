from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    file = 'main.html'
    return render_template(file, template_folder='templates')


if __name__ == "__main__":
    app.run()
