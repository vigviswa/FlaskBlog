from flaskblog import app, db

db.init_app(app)
db.create_all()

if __name__ == "__main__":

    app.run()
