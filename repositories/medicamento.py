from models.medicamento import Medicamento


class MedicamentoRepository:
    def __init__(self, db):
        self.__db = db

    def get(self, id=None):
        cursor = self.__db.connection.cursor()
        if (id):
            sql_command = "SELECT id, nome from medicamento WHERE id = %s"

            cursor.execute(sql_command, (id,))

            tupla = cursor.fetchone()

            medicamentos = Medicamento(tupla[1], tupla[2], id=tupla[0])
        else:
            sql_command = "SELECT id, nome from medicamento"
            cursor.execute(sql_command)
            medicamentos = self.transform_medicamento(cursor.fetchall())

        return medicamentos

    def save(self, medicamento):
        cursor = self.__db.connection.cursor()

        if(medicamento.id):
            sql_command = "UPDATE medicamento SET nome=%s  where id=%s"
            cursor.execute(sql_command, (medicamento.nome, medicamento.id))
        else:
            sql_command = "INSERT INTO medicamento(nome) VALUES (%s)"
            cursor.execute(sql_command, (medicamento.nome))

        self.__db.connection.commit()

        return medicamento

    def delete(self, id):
        cursor = self.__db.connection.cursor()
        sql_command = "DELETE FROM medicamento WHERE id = %s"
        cursor.execute(sql_command, (id,))

        self.__db.connection.commit()

    def transform_medicamento(self, medicamento):
        def create_medicamento_tuple(tupla):
            return Medicamento(tupla[1], tupla[2], id=tupla[0])
        return list(map(create_medicamento_tuple, medicamento))
