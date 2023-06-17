from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
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
      articles = Article.query.filter(Article.category.ilike(pks[0].id)).all()
      return render_template("article.html", news=articles, cat=Categorey.query.all(), pg = pks[0].id)
   else:
      articles = Article.query.all()
      return render_template("article.html", news=articles, cat=Categorey.query.all(), pg = -1)

@app.route("/delete/<id>", methods=["GET","POST"])
def delete(id):
   goto=''
   res = Article.query.filter(Article.id.ilike(id)).all()
   if len(res)>0:
      goto = Categorey.query.filter(Categorey.id.ilike(res[0].category)).all()[0].cat
      db.session.delete(res[0])
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
         res = Article.query.filter(Article.id.ilike(id)).all()
         if len(res)>0:
            res[0].title, res[0].content, res[0].image, res[0].category = title, content, image_url, category
         db.session.commit()
      return redirect(f'/{Categorey.query.filter(Categorey.id.ilike(category)).all()[0].cat}')
   else:
      id_k = 0
      res = Article.query.filter(Article.id.ilike(id)).all()
      if id != 0 and len(res) > 0:
         res = res[0]
         id_k = res.id
         return render_template("add_article.html", cat=Categorey.query.all(), values=res, id_k = id_k, pg = -1)
      else: return render_template("add_article.html", cat=Categorey.query.all(), values=res, id_k = id_k, pg = 0)
   

with app.app_context():
   db.create_all()

if __name__ == '__main__':
   app.run(debug=True)