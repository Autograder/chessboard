from app import db
from datetime import datetime
from user import User


class NewsFeedPost(db.Model):
    """
    The news_feed_post model in the data base.\n
    Fields:\n
    id --> The id of the ticket_feedback, unique primary key.\n
    created_at --> The time that it is created.\n
    is_deleted --> Whether this news is deleted.\n
    last_edited_at --> The last time that this news feed post is edited.\n
    subject --> The subject of the news feed post.\n
    body --> The actual body of this news feed post.\n
    owner_id --> The id of the owner of this news feed post.\n
    queue_id --> The queue_id of this news feed post belongs to.\n
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created_at = db.Column(db.Datetime, nullable=False, default=datetime.now())
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    last_edited_at = db.Column(db.Datetime, nullable=False,
                               default=datetime.now())
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(255), nullable=False, default="")
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                         nullable=False)
    queue_id = db.Column(db.Datetime, db.ForeignKey('queue.id'),
                         nullable=False)

    def __init__(self, **kwargs):
        """
        The constructor of a NewsFeedPost object.
        Inputs:\n
        create_at(Optional) --> The time that is created, default now.\n
        is_deleted(Optional) --> Whether this is deleted, default False.\n
        last_edited_at(Optional) --> The last edit time, default now.\n
        subject --> The subject of the news feed post.\n
        body --> The actual body of the news feed post.\n
        owner_id --> The id of the user who creat it.\n
        queue_id --> The id of the queue that this news feed post is in.\n
        """
        super(NewsFeedPost, self).__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Save the object into database.
        """
        db.session.commit()

    def archive(self):
        """
        Archive the newsfeedpost.
        """
        self.is_deleted = True
        self.save()

    def unarchive(self):
        """
        Unarchive the newsfeedpost.
        """
        self.is_deleted = False
        self.save()

    def edit(self, editor: User, subject: str, body: str):
        self.subject = subject
        self.owner_id = editor.id
        self.body = body
        self.last_edited_at = datetime.now()
        self.save()
