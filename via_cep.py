import requests


class ViaCep():
    def busca_cep(self, cep):
        return requests.get(f"https://viacep.com.br/ws/{cep}/json/")
