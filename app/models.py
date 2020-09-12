from app import db


class Iam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False)
    folderid = db.Column(db.String(13), unique=False)
    said = db.Column(db.String(64), unique=False)
    keyid = db.Column(db.String(120), unique=True)
    key = db.Column(db.String(128))
    date = db.Column(db.Date())

    def __repr__(self):
        return [{self.name: self.id}]

    def getkey(self, accoountid):
        return self.key(accoountid), self.folderid(accoountid)


class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    said = db.Column(db.String(64), db.ForeignKey('iam.id'))
    time = db.Column(db.Time, unique=False)
    reqid = db.Column(db.String(64), index=True, unique=True)
    type = db.Column(db.String(64), index=True, unique=False)
    params = db.Column(db.JSON, unique=False)


class Operations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operid = db.Column(db.String(64), unique=False)
    starttime = db.Column(db.Time, unique=False)
    deadline = db.Column(db.Time, unique=False)
    said = db.Column(db.String(64), db.ForeignKey('iam.id'))