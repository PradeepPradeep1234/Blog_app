from flask import Flask,request,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from wtforms import  StringField, PasswordField, SubmitField,SelectField,TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length

app=Flask(__name__)
app.secret_key = "11223344@p"
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

#Models
class Blog(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Blog_name=db.Column(db.String(100),nullable=True,unique=True)
    Blog_content=db.Column(db.String(100),nullable=True,unique=True)


#Forms
class BlogForm(FlaskForm):
    name= StringField('Blog Name', validators=[DataRequired(), Length(min=3, max=25)],render_kw={"placeholder": "Enter your blog name"})
    content=TextAreaField('Blog Content',validators=[DataRequired(),Length(min=10,max=100)],render_kw={"placeholder": "Enter blog content"})
    Submit=SubmitField('Add Blog')



@app.route('/')
@app.route('/view_books',methods=['GET','POST'])
def view_books():
    data=Blog.query.all()
    return render_template('view_blogs.html',data=data)
    

@app.route('/add_blog',methods=['GET','POST'])
def Add_Blog():
    obj=BlogForm()
    if request.method=='POST':
        new_blog=Blog(Blog_name=obj.name.data,Blog_content=obj.content.data)
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('view_books'))
    return render_template('index.html',data=obj)

@app.route('/update_blogs/<int:id>',methods=['GET','POST'])
def update_blogs(id):
    obj=BlogForm()
    data=Blog.query.get_or_404(id)
    if request.method=='POST':
        data.Blog_name=request.form.get('name')
        data.Blog_content=request.form.get('content')
        db.session.commit()
        return redirect(url_for('view_books'))
    return render_template('update_blog.html',data=data)

@app.route('/delete_blogs/<int:id>',methods=['GET','POST'])
def del_blogs(id):
    data=Blog.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('view_books'))

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)