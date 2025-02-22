from flask import Blueprint,render_template,request,flash,redirect,url_for,jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db 

views = Blueprint("views", __name__) 


@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.join(User, Post.author == User.id).all()
    return render_template("home.html",user=current_user,posts=posts)

@views.route("/create-post",methods=["GET","POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get("content")


        if not text:
            flash("Post cannot be empty",category="error")
        else:
            post = Post(text=text,author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created",category="success")
            return redirect(url_for("views.home"))
    return render_template("createpost.html",user=current_user)

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category="error")
    elif current_user.id != post.author:
        flash("You do not have permission to delete this post.", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted.", category="success")

    return redirect(url_for("views.home"))

@views.route("/post/<username>")
@login_required
def post(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User does not exist.", category="error")
        return redirect(url_for("views.home"))

    posts = user.posts
    return render_template("post.html", user=current_user, posts=posts, username=username)

@views.route("/create-comment/<post_id>",methods=["GET","POST"])
@login_required
def create_comment(post_id):
    text = request.form.get("text")

    if not text:
        flash("Comment cannot be empty",category="error")
    else:
        post= Post.query.filter_by(id=post_id).first()
        if post:
            comment = Comment(text=text,author=current_user.id,post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash("Post does not exist.", category="error")
    return redirect(url_for("views.post",username=current_user.username))

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash("Comment does not exist.", category="error")

    elif current_user.id != comment.author:
        flash("You do not have permission to delete this comment.", category="error")

    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for("views.post",username=current_user.username))

@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    
    if not post:
        return jsonify({'error': 'Post does not exist.'}), 400
    
    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'liked': False, 'likes': len(post.likes)})
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return jsonify({'liked': True, 'likes': len(post.likes)})