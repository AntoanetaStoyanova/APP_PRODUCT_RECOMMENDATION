from app import create_app

from app.models import user_db

app = create_app()
with app.app_context():
    user_db.create_all()
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
