from board import db



class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    views = db.Column(db.Integer, default=0)

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    post = db.relationship('Post', backref=db.backref('comment_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

class NestedComment(db.Model):
    __tablename__ = 'nestedComment'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id', ondelete='CASCADE'), nullable=False)
    comment = db.relationship('Comment', backref=db.backref('nestedComment_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

class LastComment(db.Model):
    __tablename__ = 'lastComment'
    id = db.Column(db.Integer, primary_key=True)
    nestedComment_id = db.Column(db.Integer, db.ForeignKey('nestedComment.id', ondelete='CASCADE'), nullable=False)
    nestedComment = db.relationship('NestedComment', backref=db.backref('lastComment_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

class OpenGraph(db.Model):
    __tablename__ = 'open_graph'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))
    post = db.relationship('Post', backref=db.backref('openGraph_set', cascade='all, delete-orphan'))
    title = db.Column(db.String(80), nullable=True)
    img = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=True)
    href = db.Column(db.Text, nullable=True)
