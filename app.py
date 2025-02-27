from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, template_folder='template')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///music.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Song Model
class Song(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), unique = True, nullable = False)
    artist = db.Column(db.String(50), unique = False, nullable = False)

    def __repr__(self):
        return f"{self.title} {self.artist}"



@app.route("/")
def index():
    songs = Song.query.all()
    return render_template("index.html", music=songs)



@app.route("/add_song", methods=["GET", "POST"])
def add_song():
    if request.method == "POST":
        title = request.form.get("title")
        artist = request.form.get("artist")
        new_song = Song(title = title, artist = artist)
        db.session.add(new_song)
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:del_id>")
def delete(del_id):
    delete_item = Song.query.get(del_id)
    db.session.delete(delete_item)
    db.session.commit()

    return redirect(url_for('index'))



@app.route("/edit/<int:edit_id>", methods=["GET", "POST"])
def edit(edit_id):
    edit_song = Song.query.get(edit_id)
    if request.method == "POST":
        if edit_song:
            edit_song.title = request.form.get("title")
            edit_song.artist = request.form.get("artist")
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return f"Song with id {edit_id} does not exist"
    return render_template("edit.html", music=edit_song)



@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)