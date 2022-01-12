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
    
    def main(self):
        while True:
            comando = self.menu_principal()
    
            if comando == "Adicionar tarefa":
                self.adicionar_tarefa()
            elif comando == "Alterar status da tarefa":
                self.alterar_status_tarefa()


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
        
        opcoes = [
            inquirer.List(
                "comando",
                message="Escolha um comando:",
                choices=["Adicionar tarefa", "Alterar status da tarefa", "Remover tarefa", "Visualizar tarefa", "Fechar"],
            ),
        ]

        comando = inquirer.prompt(opcoes)
        self._clear()
      
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
        self._clear()

    @staticmethod
    def _clear():
        os.system('cls' if os.name=='nt' else 'clear')

    
interface = InterfaceUsuario(TarefasAPI("tarefas.csv"))

interface.main()