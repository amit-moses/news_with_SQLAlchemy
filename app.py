from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_HOST')

db = SQLAlchemy(app)


class Article(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(80), unique=True, nullable=False)
   content = db.Column(db.String(800))
   image = db.Column(db.String(100))
   category = db.Column(db.String(50), nullable=False)

class Categorey(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   cat = db.Column(db.String(80), unique=True, nullable=False)

@app.route("/")
@app.route("/<pg>")
def news(pg = ''):
   pks = Categorey.query.filter(Categorey.cat.ilike(pg)).all()
   if len(pks) > 0:
      articles = Article.query.filter(Article.category.ilike(str(pks[0].id))).all()
      pks = pks[0]
   else:
      articles = Article.query.all()
      pks = Categorey(cat='All Articles',id='-1')
   return render_template("article.html", news=articles, cat=Categorey.query.all(), pg = pks)

@app.route("/get/<id>", methods=["GET","POST"])
def get(id):
   arc = Article.query.get(id)
   print(arc)
   if arc: return 'ok'
   else: return 'oo'


@app.route("/delete/<id>", methods=["GET","POST"])
def delete(id):
   goto=''
   res = Article.query.get(id)
   if res:
      goto = Categorey.query.get(res.category).cat
      db.session.delete(res)
      db.session.commit()
   return redirect(f'/{goto}')

@app.route("/add_article", methods=["GET","POST"])
@app.route("/article/<id>", methods=["GET","POST"])
def add_article(id = 0):
   if request.method == "POST":
      title = request.form.get("title")
      content = request.form.get("content")
      image_url = request.form.get("image-url") 
      category = request.form.get("category")
      if id == "0":
         article = Article(title=title,content=content,image=image_url, category=category)
         db.session.add(article)
         db.session.commit()
      else: 
         res = Article.query.get(id)
         if res:
            res.title, res.content, res.image, res.category = title, content, image_url, category
         db.session.commit()
      return redirect(f'/{Categorey.query.get(category).cat}')
   else:
      id_k = 0
      res = Article.query.get(id)
      pks = Categorey(cat='Add new Article',id='0')
      if id != 0 and res:
         id_k = res.id
         pks = Categorey(cat=f'Edit {res.title}',id='-1')
      elif id != 0 and len(res) == 0: return redirect(f'/')
      return render_template("add_article.html", cat=Categorey.query.all(), values=res, id_k = id_k, pg = pks)
   
   
   

with app.app_context():
   db.create_all()

if __name__ == '__main__':
   app.run(debug=True)