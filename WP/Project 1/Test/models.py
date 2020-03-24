from application import db


class User(db.Model):
    """Model for user accounts."""

    __tablename__ = 'users'
    
    email = db.Column(db.String(80),
                      index=True,
                      unique=False,
                      nullable=False)
    password = db.Column(db.String(80),
                        index=False,
                        unique=False,
                        nullable=False)
    def __init__(self, mail, pwd):
        self.email = mail
        self.password = pwd
        

    def __repr__(self):
        return '<User {}>'.format(self.email)