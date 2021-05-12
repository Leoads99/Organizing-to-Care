from models.usuario import Usuario


class UsuarioRepository:
    def __init__(self, db):
        self.__db = db

    def get(self, id=None):
        cursor = self.__db.connection.cursor()
        if (id):
            sql_command = "SELECT id, nome, cpf from usuario WHERE id = %s"

            cursor.execute(sql_command, (id,))

            tupla = cursor.fetchone()

            usuarios = Usuario(tupla[1], tupla[2], id=tupla[0])
        else:
            sql_command = "SELECT id, nome, cpf from usuario"
            cursor.execute(sql_command)
            usuarios = self.transform_usuario(cursor.fetchall())

        return usuarios

    def save(self, usuario):
        cursor = self.__db.connection.cursor()

        if(usuario.id):
            sql_command = "UPDATE usuario SET nome=%s, cpf=%s where id=%s"
            cursor.execute(sql_command, (usuario.nome,
                                         usuario.cpf, usuario.id))
        else:
            sql_command = "INSERT INTO usuario(nome, cpf) VALUES (%s, %s)"
            cursor.execute(sql_command, (usuario.nome,
                                         usuario.cpf))

        self.__db.connection.commit()

        return usuario

    def delete(self, id):
        cursor = self.__db.connection.cursor()
        sql_command = "DELETE FROM usuario WHERE id = %s"
        cursor.execute(sql_command, (id,))

        self.__db.connection.commit()

    def transform_usuario(self, usuarios):
        def create_usuario_tuple(tupla):
            return Usuario(tupla[1], tupla[2], id=tupla[0])
        return list(map(create_usuario_tuple, usuarios))