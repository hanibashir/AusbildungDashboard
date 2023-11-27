
from app import create_app

app = create_app()

# override jsonify sorting
app.json.sort_keys = False

if __name__ == "__main__":
    app.run()
