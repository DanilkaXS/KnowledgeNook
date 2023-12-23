import base64
import datetime

from flask import Flask, render_template, request, redirect, session
from sqlalchemy import create_engine, Column, Integer, String, BLOB, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = "my_secret_key=)"

# создаем соединение с базой данных
engine = create_engine('sqlite:///knowledgenook.db')

# создаем базовый класс для определения моделей таблиц
Base = declarative_base()


# определяем модели
class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    date = Column(String, nullable=False)
    img = Column(BLOB, nullable=False)
    text = Column(String, nullable=False)
    tag = Column(String, nullable=False)


# определяем модели
class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Integer, nullable=False)
    raiting = Column(Integer, nullable=False)
    user_icon = Column(BLOB, nullable=False)


# определяем модели
class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, nullable=False)
    post_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    user_icon = Column(BLOB, nullable=False)
    user_raiting = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    time = Column(String, nullable=False)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    Session = sessionmaker(bind=engine)
    session_db = Session()
    all_posts = session_db.query(Posts).all()
    all_posts.reverse()
    for i in all_posts:
        i.img = base64.b64encode(i.img).decode('utf-8')
    if "userkey" in session:
        user_cookie = session["userkey"].split("$")
        print(user_cookie)
        session_db.close()
        user_data = session_db.query(Users).filter_by(id=user_cookie[1]).first()
        user_data.user_icon = base64.b64encode(user_data.user_icon).decode('utf-8')
        print(user_data)
        return render_template("main_page.html", all_posts=all_posts, user_data=user_data)
    else:
        return render_template("main_page.html", all_posts=all_posts)


@app.route("/login", methods=["GET", "POST"])
def login_task():
    if "userkey" in session:
        return redirect("/")
    else:
        if request.method == "POST":
            Session = sessionmaker(bind=engine)
            session_db = Session()
            login = request.form["username"]
            password = request.form["password"]
            user = session_db.query(Users).filter_by(login=login, password=password).first()
            if user is not None:
                session["userkey"] = f"{user.role}${user.id}"
                session_db.close()
                return redirect("/")
            else:
                return render_template("login.html")
        else:
            return render_template("login.html")


@app.route("/registr", methods=["GET", "POST"])
def registr_task():
    if "userkey" in session:
        return redirect("/")
    else:
        if request.method == "POST":
            Session = sessionmaker(bind=engine)
            session_db = Session()
            name = request.form["name"]
            login = request.form["username"]
            password = request.form["password"]

            with open('static/img/default_user_logo.png', 'rb') as f:
                default_user_logo = f.read()

            user_id = session_db.query(Users).order_by(Users.id.desc()).first().id

            new_user = Users(id=user_id + 1,
                             name=name,
                             login=login,
                             password=password,
                             role=1,
                             raiting=0,
                             user_icon=default_user_logo)
            session_db.add(new_user)
            session_db.commit()
            return render_template("login.html")
        else:
            return render_template("registr.html")


@app.route("/logout")
def logout():
    session.pop("userkey", None)
    return redirect("/")


@app.route('/create', methods=['GET', 'POST'])
def create_post():
    Session = sessionmaker(bind=engine)
    session_db = Session()
    if "userkey" in session:
        if request.method == "POST":
            request.files["image"].save("static/temp/test.png")
            with open("static/temp/test.png", "rb") as f:
                img = f.read()
                f.close()
            new_post_raw = [
                request.form['postName'],
                request.form['autor'],
                img,
                request.form['text'],
                request.form['tags']]
            name, autor, img, text, tags = new_post_raw

            new_post = Posts(name=name, autor=autor, date=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                             img=img, text=text, tag=tags)
            session_db.add(new_post)
            session_db.commit()
            return redirect("/")
        else:
            user_cookie = session["userkey"].split("$")
            print(user_cookie)
            session_db.close()
            user_data = session_db.query(Users).filter_by(id=user_cookie[1]).first()
            user_data.user_icon = base64.b64encode(user_data.user_icon).decode('utf-8')
            print(user_data)
            return render_template("create_page.html", user_data=user_data)
    else:
        return redirect("/")


@app.route('/view', methods=['GET', 'POST'])
def view_post():
    Session = sessionmaker(bind=engine)
    session_db = Session()
    post = session_db.query(Posts).filter_by(id=request.args["id"]).all()
    session_db.close()
    for i in post:
        i.img = base64.b64encode(i.img).decode('utf-8')
    comments = session_db.query(Comments).filter_by(post_id=request.args["id"]).all()
    comments.reverse()
    session_db.close()
    for j in comments:
        j.user_icon = base64.b64encode(j.user_icon).decode('utf-8')
    if request.method == "POST":
        user_cookie = session["userkey"].split("$")
        user_data = session_db.query(Users).filter_by(id=user_cookie[1]).first()
        name = user_data.name
        icon = user_data.user_icon
        message = request.form['message']
        post_id = request.url.split("=")[1]
        time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        raiting = user_data.raiting
        new_comment = Comments(post_id=post_id, username=name, user_icon=icon, user_raiting=raiting, text=message,
                               time=time)
        session_db.add(new_comment)
        session_db.commit()
        return redirect(f"/view?name={post_id}")

    else:
        if "userkey" in session:
            user_cookie = session["userkey"].split("$")
            print(user_cookie)
            session_db.close()
            user_data = session_db.query(Users).filter_by(id=user_cookie[1]).first()
            user_data.user_icon = base64.b64encode(user_data.user_icon).decode('utf-8')
            print(user_data)
            return render_template("view_page.html", post=post, user_data=user_data, comments=comments)
        else:
            return render_template("view_page.html", post=post, comments=comments)


@app.route('/user', methods=['GET', 'POST'])
def view_user_page():
    Session = sessionmaker(bind=engine)
    session_db = Session()
    if "userkey" in session:
        if request.method == "POST":
            if 'file' not in request.files:
                return redirect("/user")

            file = request.files['file']
            if file.filename == '':
                return redirect("/user")

            if file:
                file.save("static/temp/test.png")

                with open("static/temp/test.png", "rb") as f:
                    img = f.read()
                    f.close()
                print(img)
                user_cookie = session["userkey"].split("$")
                user_data = session_db.query(Users).filter_by(id=user_cookie[1]).first()
                user_data.user_icon = img
                session_db.commit()
                session_db.close()
                user_data = session_db.query(Users).filter_by(id=user_cookie[1]).first()
                user_data.user_icon = base64.b64encode(user_data.user_icon).decode('utf-8')
                session_db.close()

                num_articles = len(session_db.query(Posts).filter_by(autor=user_data.name).all())
                print(num_articles)
                return render_template("user_page.html", user_data=user_data, num_articles=num_articles)

        else:
            user_cookie = session["userkey"].split("$")
            session_db.close()
            user_data = session_db.query(Users).filter_by(id=user_cookie[1]).first()
            user_data.user_icon = base64.b64encode(user_data.user_icon).decode('utf-8')
            session_db.close()

            num_articles = len(session_db.query(Posts).filter_by(autor=user_data.name).all())
            level_of_accses = session["userkey"].split("$")[0]
            return render_template("user_page.html", user_data=user_data, num_articles=num_articles, level_of_accses=level_of_accses)
    else:
        return redirect("/")

@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    Session = sessionmaker(bind=engine)
    session_db = Session()
    all_posts = session_db.query(Posts).all()
    all_posts.reverse()
    session_db.close()
    if request.method == "POST":
        print(request.form["json"].split(":")[1][:-1])
        post_id = request.form["json"].split(":")[1][:-1]
        delete_post = session_db.query(Posts).filter_by(id=post_id).delete()
        session_db.commit()
        session_db.close()

        return redirect("/admin")
    else:
        for i in all_posts:
            i.img = base64.b64encode(i.img).decode('utf-8')
        if "userkey" in session:
            if session["userkey"].split("$")[0] == "0":
                user_cookie = session["userkey"].split("$")
                print(user_cookie)
                user_data = session_db.query(Users).filter_by(id=user_cookie[1]).first()
                user_data.user_icon = base64.b64encode(user_data.user_icon).decode('utf-8')
                session_db.close()
                print(user_data)
                all_users = session_db.query(Users).all()
                for i in all_users:
                    i.user_icon = base64.b64encode(i.user_icon).decode('utf-8')
                return render_template("admin.html", all_posts=all_posts, user_data=user_data, all_users=all_users)
            else:
                return redirect("/")
        else:
            return redirect("/")


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
