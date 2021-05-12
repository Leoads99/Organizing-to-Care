from database import db


class Medicamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_medicamento = db.Column(db.String(50))
    data_validade = db.Column(db.String(11))
    quantidade = db.Column(db.Integer)
    peso = db.Column(db.String(50))

    def cadastrar(self):
        db.session.add(self)
        db.session.commit()      

