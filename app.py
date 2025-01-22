import os
from flask import Flask, render_template, send_from_directory

# Get the absolute path to the current directory
ROOT_DIR = os.getcwd()

app = Flask(__name__, 
    static_folder=os.path.join(ROOT_DIR, 'static'),
    template_folder=os.path.join(ROOT_DIR, 'templates')
)

# Enable debug mode
app.config['DEBUG'] = True

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)
