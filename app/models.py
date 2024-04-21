from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Email(db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(255))
    subject = db.Column(db.String(255))
    body = db.Column(db.Text)
    summary = db.Column(db.Text)
    read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Email {self.id}>'

