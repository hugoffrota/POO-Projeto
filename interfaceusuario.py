from csv import excel
from inquirer.errors import ValidationError
from tarefasapi import TarefasAPI
import os
import sys
from pprint import pprint
import inquirer  
from datetime import datetime
from time import sleep
sys.path.append(os.path.realpath("."))


class InterfaceUsuario:

    def __init__(self, api):
        self.api = api
        self.ativo = True
    
    def main(self):
        while self.ativo:
            comando = self.menu_principal()
    
            if comando == "Adicionar tarefa":
                self.adicionar_tarefa()
            elif comando == "Alterar status da tarefa":
                self.alterar_status_tarefa()
            elif comando == "Remover tarefa":
                self.excluir_tarefa()
            elif comando == "Visualizar tarefa":
                self.visualizar_tarefas_data()
            else:
                self.parar_programa()
    
    def parar_programa(self):
        self.ativo = False
        


    def adicionar_tarefa(self):

        def _valida_titulo_tarefa(answers, current):
            if not current:
                raise inquirer.error.ValidationError("Insira um título para a tarefa!", reason="Insira um título para a tarefa!")
            return True
        
        def _valida_prazo_tarefa(answers, current):
            if current:
                try:
                    prazo = datetime.strptime(current, '%d/%m/%Y')
                except:
                    raise inquirer.error.ValidationError("Insira uma data válida", reason="Insira uma data válida")
            return True
        
        def _valida_status_tarefa(answers, current):
            if not current.lower() in ['pendente', 'concluída', 'concluida', '']:
                raise inquirer.error.ValidationError("Insira um status válido", reason="Insira um status válido")
            return True
        
        questoes = [
            inquirer.Text("titulo", message="Insira o título da tarefa", validate=_valida_titulo_tarefa),
            inquirer.Text("prazo", message="Qual o prazo de realização da tarefa {titulo}? (DD/MM/AAAA) (Opcional)", validate=_valida_prazo_tarefa),
            inquirer.Text("categoria", message="Qual a categoria da tarefa? (Opcional)"),
            inquirer.Text("status", message="Qual o status da tarefa? ([pendente]/concluida)", validate=_valida_status_tarefa)
        ]

        print("ADICIONAR TAREFA\n")

        dados = inquirer.prompt(questoes)

        self.api.salvar_tarefa(
            titulo=dados['titulo'],
            data=dados['prazo'] if dados['prazo'] else None,
            categoria=dados['categoria'] if dados['categoria'] else None,
            status=dados['status'].lower() if dados['status'] else 'pendente'
        )
        
        self._clear()

    def menu_principal(self):
        self._clear()
        opcoes = [
            inquirer.List(
                "comando",
                message="Escolha um comando:",
                choices=["Adicionar tarefa", "Alterar status da tarefa", "Remover tarefa", "Visualizar tarefa", "Fechar"],
            ),
        ]

        comando = inquirer.prompt(opcoes)
      
        return comando['comando']

    def alterar_status_tarefa(self):
        print("ALTERAR TAREFA\n")
        
        titulo_tarefa = inquirer.prompt(
            [inquirer.Text("titulo", message="Qual o título da tarefa?")]
        )

        tarefa = self.api.busca_tarefas_titulo(titulo_tarefa['titulo'])

        if tarefa is None:
            print("Tarefa não encontrada.")
            sleep(2)
            self._clear()
            return
        

        opcoes = [
            inquirer.List(
                "status",
                message="Escolha o status:",
                choices=["concluida", "pendente"]
            ),
        ]

        status = inquirer.prompt(opcoes)
        
        self.api.alterar_status(tarefa[0], status['status'])

    def excluir_tarefa(self):
        print("EXCLUIR TAREFA\n")
        
        titulo_tarefa = inquirer.prompt(
            [inquirer.Text("titulo", message="Qual o título da tarefa a ser excluída?")]
        )

        tarefa = self.api.busca_tarefas_titulo(titulo_tarefa['titulo'])

        if tarefa is None:
            print("Tarefa não encontrada.")
            sleep(2)
            self._clear()
            return
                
        confirmacao = [
            inquirer.Confirm("excluir", message=f"Tem certeza que quer excluir a tarefa {tarefa[0]} | y-confirmar n-cancelar", default=False),
        ]

        confirmar = inquirer.prompt(confirmacao)
        
        if confirmar['excluir']:
            self.api.excluir_tarefa(tarefa[0])

    def visualizar_tarefas_data(self):
        def _valida_prazo_tarefa(answers, current):
            if current:
                try:
                    prazo = datetime.strptime(current, '%d/%m/%Y')
                except:
                    raise inquirer.error.ValidationError("Insira uma data válida", reason="Insira uma data válida")
            return True
        
        questoes = [
            inquirer.Text("data", message="De qual dia você deseja visualizar as tarefas? (DD/MM/AAAA) (Opcional)", validate=_valida_prazo_tarefa),
        ]

        print("VISUALIZAR TAREFAS\n")

        dados = inquirer.prompt(questoes)
    
        tarefas = self.api.buscar_tarefas(dados['data'])
        print("Dia:", dados['data'] if dados['data'] else "Não especificado")
        for tarefa in tarefas:
            print("Título:", tarefa[0])
            print("Categoria:", tarefa[2] if tarefa[2] else "Sem categoria")
            print("Status:", tarefa[3])
            print("\n")


        input("Pressione Enter para continuar...")


    @staticmethod
    def _clear():
        os.system('cls' if os.name=='nt' else 'clear')

    
interface = InterfaceUsuario(TarefasAPI("tarefas.csv"))

interface.main()