from flask import Flask, request, jsonify

from marshmallow import validate, ValidationError  # noqa: E402
from marshmallow_jsonapi import fields  # noqa: E402
from marshmallow_jsonapi.flask import Relationship, Schema  # noqa: E402


class CommentSchema(Schema):

    uuid = fields.Str()
    reply_to = Relationship(
        type_='comments',
        related_view='comments_detail',
        related_view_kwargs={'comment_uuid': '<replyTo>', '_external': True},
        include_data=True,
    )
    reply_to = fields.Str(attribute='replyTo')

    authority = fields.Str()
    document_id = fields.Str(attribute='documentId')
    document_version = fields.Str(attribute='documentVersion')
    document_author_emails = fields.Str(attribute='documentAuthorEmails')

    text = fields.Str()
    annotations = fields.Str()

    author_email = fields.Str(attribute='authorEmail')
    author_name = fields.Str(attribute='authorName')
    author_avatar = fields.Str(attribute='authorAvatar')

    ts_created = fields.Int()
    ts_updated = fields.Int()

    is_resolved = fields.Bool()

    class Meta:
        type_ = 'comments'
        self_view = 'comment_detail'
        self_view_kwargs = {'comment_uuid': '<uuid>', '_external': True}
        self_view_many = 'comments_list'


class AuthorSchema(Schema):
    id = fields.Str(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    password = fields.Str(load_only=True, validate=validate.Length(6))
    twitter = fields.Str()

    class Meta:
        type_ = 'people'
        self_view = 'author_detail'
        self_view_kwargs = {'author_id': '<id>'}
        self_view_many = 'authors_list'


class PostSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str()

    author = Relationship(
        related_view='author_detail',
        related_view_kwargs={'author_id': '<author.id>', '_external': True},
        include_data=True,
        type_='people',
    )

    comments = Relationship(
        related_view='posts_comments',
        related_view_kwargs={'post_id': '<id>', '_external': True},
        many=True,
        include_data=True,
        type_='comments',
    )

    class Meta:
        type_ = 'posts'
        self_view = 'posts_detail'
        self_view_kwargs = {'post_id': '<id>'}
        self_view_many = 'posts_list'


### VIEWS ###

app = Flask(__name__)
app.config['DEBUG'] = True

def J(*args, **kwargs):
    """Wrapper around jsonify that sets the Content-Type of the response to
    application/vnd.api+json.
    """
    response = jsonify(*args, **kwargs)
    response.mimetype = 'application/vnd.api+json'
    return response

@app.route('/posts/', methods=['GET'])
def posts_list():
    posts = db['posts']
    data = PostSchema(many=True).dump(posts)
    return J(data)

@app.route('/posts/<int:post_id>')
def posts_detail(post_id):
    post = db['posts'][post_id - 1]
    data = PostSchema().dump(post)
    return J(data)

@app.route('/posts/<int:post_id>/comments/')
def posts_comments(post_id):
    post = db['posts'][post_id - 1]
    comments = post.comments
    data = CommentSchema(many=True).dump(comments)
    return J(data)

@app.route('/authors/')
def authors_list():
    author = db['authors']
    data = AuthorSchema(many=True).dump(author)
    return J(data)

@app.route('/authors/<int:author_id>')
def author_detail(author_id):
    author = db['authors'][author_id - 1]
    data = AuthorSchema().dump(author)
    return J(data)

@app.route('/authors/', methods=['POST'])
def author_create():
    schema = AuthorSchema()
    input_data = request.get_json() or {}
    try:
        data = schema.load(input_data)
    except ValidationError as err:
        return J(err.messages), 422
    id_ = len(db['authors'])
    author = Author(id=id_, **data)
    db['authors'].append(author)
    data = schema.dump(author)
    return J(data)

@app.route('/comments/')
def comments_list():
    comment = db['comments']
    data = CommentSchema(many=True).dump(comment)
    return J(data)

@app.route('/comments/<int:comment_id>')
def comment_detail(comment_id):
    comment = db['comments'][comment_id - 1]
    data = CommentSchema().dump(comment)
    return J(data)


if __name__ == '__main__':
    app.run()
