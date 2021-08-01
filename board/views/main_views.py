from flask import Blueprint, request
import json
from board import db, create_app
# from board import db, socketio, create_app
from board.models import Post, Comment, NestedComment, LastComment, OpenGraph
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import threading
import time


bp = Blueprint('main', __name__, url_prefix='/')
app = create_app()


# @socketio.on('post-create')
# def handle_my_custom_event(json):
#     print('received my event: ' + str(json))
#     socketio.emit('my response', json)


# 백그라운드 작업
def background_task(title, content):
    post = Post(title=title, content=content, created_at=datetime.now().replace(microsecond=0))
    with app.app_context():
        db.session.add(post)
        db.session.commit()

        # open graph 데이터 추출 및 테이블에 저장
        content = post.content
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
        for href in urls:
            try:
                response = requests.get(href)
                soup = BeautifulSoup(response.text, 'html.parser')
                if soup.find(attrs={'property': 'og:title'}):
                    title = soup.find(attrs={'property': 'og:title'})["content"]
                else:
                    title = soup.find('title').text
                if soup.find(attrs={'property': 'og:description'}):
                    description = soup.find(attrs={'property': 'og:description'})["content"]
                else:
                    description = "설명 없음"
                if soup.find(attrs={'property': 'og:image'}):
                    image = soup.find(attrs={'property': 'og:image'})["content"]
                else:
                    image = "https://cdn.imweb.me/thumbnail/20210617/2eafc488ee3a3.png"
                if href[:5] == "https":
                    url = href[8:]
                else:
                    url = href[7:]
                open_graph = OpenGraph(post=post, title=title, description=description, img=image, url=url, href=href)
                db.session.add(open_graph)
                db.session.commit()
            except Exception as ex:
                print(ex)

        # socketio로 보내기 (emit)
        # post = {
        #     'id': post.id,
        #     'title': post.title,
        #     'content': post.content,
        #     'created_at': str(post.created_at),
        # }


@bp.route('/api/post/create', methods=['GET', 'POST'])
def post_create():
    if request.method == "POST":
        content = request.get_json()["content"]
        title = request.get_json()["title"]
        threading.Thread(target=background_task, args=(title, content)).start()
        return ""


@bp.route('/api/post/list')
def get_post_list():
    posts = Post.query.order_by(Post.id.desc())
    post_list = []
    for i in posts:
        post = {
            'id': i.id,
            'title': i.title,
            'content': i.content,
            'created_at': str(i.created_at),
        }
        post_list.append(post)
    return json.dumps(post_list)

@bp.route('/api/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get(post_id)
    post.views += 1
    db.session.commit()

    post = Post.query.get(post_id)
    comments = Comment.query.filter_by(post_id=post.id).all()

    comment_list = []
    for i in comments:
        nestedComments = NestedComment.query.filter_by(comment=i).all()
        nestedComment_list = []
        for j in nestedComments:
            lastComments = LastComment.query.filter_by(nestedComment=j).all()
            lastComment_list = []
            for k in lastComments:
                lastComment = {
                    'id': k.id,
                    'content': k.content,
                    'created_at': str(k.created_at)
                }
                lastComment_list.append(lastComment)
            nestedComment = {
                'id': j.id,
                'content': j.content,
                'created_at': str(j.created_at),
                'lastComments': lastComment_list
            }
            nestedComment_list.append(nestedComment)
        comment = {
            'id': i.id,
            'content': i.content,
            'created_at': str(i.created_at),
            'nestedComments': nestedComment_list
        }
        comment_list.append(comment)

    openGraphs = OpenGraph.query.filter_by(post_id=post_id).all()

    openGraph_list = []
    for og in openGraphs:
        open_graph = {
            'title': og.title,
            'url': og.url,
            'description': og.description,
            'img': og.img,
            'href': og.href
        }
        openGraph_list.append(open_graph)

    post = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'created_at': str(post.created_at),
        'views': post.views,
        'comments': comment_list,
        'open_graphs': openGraph_list

    }
    return json.dumps(post)

@bp.route('/api/post/delete/<int:post_id>', methods=["DELETE"])
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return ""


@bp.route('/api/comment/create/<int:post_id>', methods=['GET', 'POST'])
def comment_create(post_id):
    post = Post.query.get(post_id)
    if request.method == "POST":
        comment = Comment(post_id=post_id, post=post, content=request.get_json()["content"], created_at=datetime.now().replace(microsecond=0))

        db.session.add(comment)
        db.session.commit()

        comments = Comment.query.filter_by(post_id=post.id).all()
        comment_list = []
        for i in comments:
            nestedComments = NestedComment.query.filter_by(comment=i).all()
            nestedComment_list = []
            for j in nestedComments:
                lastComments = LastComment.query.filter_by(nestedComment=j).all()
                lastComment_list = []
                for k in lastComments:
                    lastComment = {
                        'id': k.id,
                        'content': k.content,
                        'created_at': str(k.created_at)
                    }
                    lastComment_list.append(lastComment)
                nestedComment = {
                    'id': j.id,
                    'content': j.content,
                    'created_at': str(j.created_at),
                    'lastComments': lastComment_list
                }
                nestedComment_list.append(nestedComment)
            comment = {
                'id': i.id,
                'content': i.content,
                'created_at': str(i.created_at),
                'nestedComments': nestedComment_list
            }
            comment_list.append(comment)
        return json.dumps(comment_list)

@bp.route('/api/nestedComment/create/<int:comment_id>', methods=['GET', 'POST'])
def nested_comment_create(comment_id):
    comment = Comment.query.get(comment_id)
    if request.method == "POST":
        nestedComment = NestedComment(comment_id=comment_id, comment=comment, content=request.get_json()["content"], created_at=datetime.now().replace(microsecond=0))
        db.session.add(nestedComment)
        db.session.commit()

        comments = Comment.query.filter_by(post_id=comment.post_id).all()

        comment_list = []
        for i in comments:
            nestedComments = NestedComment.query.filter_by(comment=i).all()
            nestedComment_list = []
            for j in nestedComments:
                lastComments = LastComment.query.filter_by(nestedComment=j).all()
                lastComment_list = []
                for k in lastComments:
                    lastComment = {
                        'id': k.id,
                        'content': k.content,
                        'created_at': str(k.created_at)
                    }
                    lastComment_list.append(lastComment)
                nestedComment = {
                    'id': j.id,
                    'content': j.content,
                    'created_at': str(j.created_at),
                    'lastComments': lastComment_list
                }
                nestedComment_list.append(nestedComment)
            comment = {
                'id': i.id,
                'content': i.content,
                'created_at': str(i.created_at),
                'nestedComments': nestedComment_list
            }
            comment_list.append(comment)
        return json.dumps(comment_list)


@bp.route('/api/lastComment/create/<int:nestedComment_id>', methods=['GET', 'POST'])
def last_comment_create(nestedComment_id):
    nestedComment = NestedComment.query.get(nestedComment_id)
    if request.method == "POST":
        lastComment = LastComment(nestedComment=nestedComment, content=request.get_json()["content"], created_at=datetime.now().replace(microsecond=0))
        db.session.add(lastComment)
        db.session.commit()

        comment_id = nestedComment.comment_id
        comment = Comment.query.filter_by(id=comment_id).first()
        comments = Comment.query.filter_by(post_id=comment.post_id).all()

        comment_list = []
        for i in comments:
            nestedComments = NestedComment.query.filter_by(comment=i).all()
            nestedComment_list = []
            for j in nestedComments:
                lastComments = LastComment.query.filter_by(nestedComment=j).all()
                lastComment_list = []
                for k in lastComments:
                    lastComment = {
                        'id': k.id,
                        'content': k.content,
                        'created_at': str(k.created_at)
                    }
                    lastComment_list.append(lastComment)
                nestedComment = {
                    'id': j.id,
                    'content': j.content,
                    'created_at': str(j.created_at),
                    'lastComments': lastComment_list
                }
                nestedComment_list.append(nestedComment)
            comment = {
                'id': i.id,
                'content': i.content,
                'created_at': str(i.created_at),
                'nestedComments': nestedComment_list
            }
            comment_list.append(comment)
        return json.dumps(comment_list)
