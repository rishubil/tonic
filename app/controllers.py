from app import app

@app.route('/')
def index():
    return "Testing for flask"