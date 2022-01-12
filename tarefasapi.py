import csv

class TarefasAPI:

    colunas = ['titulo', 'prazo', 'categoria', 'status']

    def __init__(self, arquivo):

        self.arquivo = arquivo

        try:
            with open(self.arquivo, 'r', newline='') as f:
                reader = csv.reader(f)
        except FileNotFoundError:
            with open(self.arquivo, 'w', newline='') as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(TarefasAPI.colunas)
    
    def salvar_tarefa(self, titulo, data=None, categoria=None, status='pendente'):
        with open(self.arquivo, 'a', newline='') as f:
            data = [titulo, data, categoria, status]
            writer = csv.writer(f, delimiter=";")
            writer.writerow(data)
    
    def alterar_status(self, titulo, novo_status):
        with open(self.arquivo, newline='') as f:
            reader = csv.reader(f, delimiter=';', lineterminator='\n')
            conteudo = list(reader)
            for linha in conteudo:
                if linha[0] == titulo:
                    linha[3] = novo_status
                    break

        with open(self.arquivo, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';', lineterminator='\n')
            writer.writerows(conteudo)
    
    def excluir_tarefa(self, titulo):
        with open(self.arquivo, newline='') as f:
            reader = csv.reader(f, delimiter=';', lineterminator='\n')
            conteudo = list(reader)
            for index, linha in enumerate(conteudo[:]):
                if linha[0] == titulo:
                    conteudo.pop(index)
                    break

        with open(self.arquivo, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';', lineterminator='\n')
            writer.writerows(conteudo)

    def buscar_tarefas(self, data):
        with open(self.arquivo, newline='') as f:
            reader = csv.reader(f, delimiter=';', lineterminator='\n')
            conteudo = []
            for linha in reader:
                if linha[1] == data:
                    conteudo.append(linha)
        return conteudo
    
    def busca_tarefas_titulo(self, titulo):
        with open(self.arquivo, newline='') as f:
            reader = csv.reader(f, delimiter=';', lineterminator='\n')
            for linha in reader:
                if linha[0] == titulo:
                    return linha

            

    
