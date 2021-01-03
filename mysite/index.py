# A very simple Flask Hello World app for you to get started with...

from flask import Flask,render_template,request, session, url_for
import pickle
from peewee import *
import filter

#f = filter.DFAFilter()
#f.parse("/home/artsite/mysite/keywords")
#print(f.filter("hello sexy baby"))

db = SqliteDatabase('this.db')

class Chat(Model):
    massage = CharField()
    class Meta:
        database = db

class User(Model):
    name = CharField()
    password = CharField()
    type = CharField()
    class Meta:
        database = db

class Posts(Model):
    time = CharField()
    content = CharField()
    author = CharField()
    tag = CharField()
    title = CharField()
    class Meta:
        database = db

db.create_tables([Chat, Posts, User])

#p = Posts(tag='测试', time="2020-12-26", author = "测试", content = "#第一个Markdown测试文章",title = "测试MD文章")
#p.save()

#u = User(name="admin",password="123456",type="admin")
#u.save()

app = Flask(__name__, static_folder='static')

app.config['SECRET_KEY'] = 'XXXXX'

@app.route('/',methods=["POST", "GET"])
def hello_world():
    with open("./count.txt","rb") as f:
        count = pickle.load(f)
    with open("./count.txt","wb") as f:
        pickle.dump(count + 1,f)
    if request.method == "GET":
        if "log_in" in session:
            welcome = "欢迎，" + session["name"]
        else:
            welcome = "尚未登录！"
        return render_template("base.html",welcome = welcome,count = count,says = Chat.select())
    if request.method == "POST":
        f = filter.DFAFilter()
        f.parse("/home/artsite/mysite/keywords")
        word1 = request.form.get("word")
        word = f.filter(word1)
        if len(word) > 100:
            return "字数太多了！"
        else:
            new=Chat(massage=word)
            new.save()
        #users.append({"text": word})
        return render_template("base.html",count = count,says = Chat.select())


@app.route('/archive',methods=["POST", "GET"])
def archive():
    if request.method == "GET":
        return render_template("archive.html",posts = Posts.select())


@app.route("/post/<title>",methods= ["POST","GET"])
def post(title):
    if request.method == "GET":
        return render_template("post.html", posts = Posts.select().where(Posts.title == title))


@app.route("/new",methods= ["POST","GET"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        time = request.form.get("time")
        author = request.form.get("author")
        tag = request.form.get("tag")
        p = Posts(tag=tag, time=time, author = author, content = text,title = title)
        p.save()


@app.route('/menu',methods=["POST", "GET"])
def hello_menu():
    return render_template("menu.html")


@app.route("/help",methods=["POST","GET"])
def help():
    if request.method == "GET":
        return render_template("help.html")
    elif request.method == "POST":
        return "该功能正在开发！"

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        try:
            yes = User.get(User.name == name)
        except:
            return "登录错误"
        if yes.password == password:
            session["log_in"] = True
            session["name"] = name
            session["type"] = yes.type
            return "登录成功"
        else:
            return "密码错误"
    if request.method == "GET":
        return render_template("login.html")

@app.route('/blog')
def index():
    return render_template('welcome.html', title="Welcome")


@app.route('/home')
def home():
    return render_template('base.html', title="Home")
