from database import db


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    cpf = db.Column(db.String(11))
    email = db.Column(db.String(50))
    telefone = db.Column(db.String(11))
    cep = db.Column(db.String(8))
    logradouro = db.Column(db.String(80))
    username = db.Column(db.String(30))
    senha = db.Column(db.String(30))

    def cadastrar(self):
        db.session.add(self)
        db.session.commit()

    def login(self):
        login_correto = self.query.filter_by(
            username=self.username, senha=self.senha).first()

        return login_correto    

