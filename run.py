from myapp.init import create_app, db
from myapp.models import parking_spot
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)