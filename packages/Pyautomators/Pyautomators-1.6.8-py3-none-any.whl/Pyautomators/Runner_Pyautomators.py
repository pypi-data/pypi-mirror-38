# -*- coding: utf-8 -*-

'''
Created on 26 de set de 2018

@author: koliveirab
'''
import argparse
from Pyautomators.BDT.__main__ import main as home
import threading
import ast
from Pyautomators import Dados
from Pyautomators.Error import Ambiente_erro
from Pyautomators.Dados import pegarConteudoYAML
from Pyautomators import Ambiente  
import os
class Modelador_Funcional_Web():
    
    @staticmethod
    def Run_Pyautomators(dicionario_yaml,navegador):
        
        lista_de_execucao=['--summary','--no-logcapture','--no-capture-stderr','--no-capture']
        for item in dicionario_yaml:
            if(item=='tags'):
                for arg in dicionario_yaml[item]:
                    tag_string=str(",").join(dicionario_yaml[item])
                lista_de_execucao.append("--tags="+tag_string)
            if(item=='args'):
                for arg in dicionario_yaml[item]:
                    lista_de_execucao.append('-D'+str(arg)+'='+str(dicionario_yaml[item][arg]))
            if(item=='saida'):
                dir=os.path.join(Ambiente.path_atual(),"docs/reports/")
                lista_de_execucao.append('--junit')
                lista_de_execucao.append('--junit-directory='+dir)                        
                lista_de_execucao.append('--format=json.pretty')
                lista_de_execucao.append('-o='+dir+str(navegador).upper()+dicionario_yaml[item])
                lista_de_execucao.append('--format=sphinx.steps')
                lista_de_execucao.append('-o=log/'+str(navegador).upper())
                lista_de_execucao.append('--format=steps.doc')
                lista_de_execucao.append('-o='+"log/"+"location-steps.log")
                lista_de_execucao.append('--format=steps.usage')
                lista_de_execucao.append('-o='+"log/"+"location-features.log")
            if(item=='navegador'):
                for options in dicionario_yaml[item]:
                    for opcao in dicionario_yaml[item][options]:
                        lista_de_execucao.append('-D{}={}'.format(opcao,dicionario_yaml[item][options][opcao]))

        lista_de_execucao.append('-Dnavegador='+navegador)
        return lista_de_execucao
    
class Modelador_Funcional_Mobile():
    
    @staticmethod
    def Run_Pyautomators(dicionario_yaml,Device):
        
        lista_de_execucao=['--summary','--no-logcapture','--no-capture-stderr','--no-capture']
        for item in dicionario_yaml:
            print(item)
            if(item=='tags'):
                for arg in dicionario_yaml[item]:
                    tag_string=str(",").join(dicionario_yaml[item])
                lista_de_execucao.append("--tags="+tag_string)
            elif(item=='args'):
                for arg in dicionario_yaml[item]:
                    lista_de_execucao.append('-D'+str(arg)+'='+str(dicionario_yaml[item][arg]))
            elif(item=='saida'):
                dir=os.path.join(Ambiente.path_atual(),"docs/reports/")
                lista_de_execucao.append('--junit')
                lista_de_execucao.append('--junit-directory='+dir)                        
                lista_de_execucao.append('--format=json.pretty')
                lista_de_execucao.append('-o='+dir+str(Device).upper()+dicionario_yaml[item])
                lista_de_execucao.append('--format=sphinx.steps')
                lista_de_execucao.append('-o=log/'+str(Device).upper())
                lista_de_execucao.append('--format=steps.doc')
                lista_de_execucao.append('-o='+"log/"+"location-steps.log")
                lista_de_execucao.append('--format=steps.usage')
                lista_de_execucao.append('-o='+"log/"+"location-features.log")
            elif(item=='devices'):
                for options in dicionario_yaml[item]:
                    for opcao in dicionario_yaml[item][options]:
                        lista_de_execucao.append('-D{}={}'.format(opcao,dicionario_yaml[item][options][opcao]))
        lista_de_execucao.append('-Ddevice='+Device)
        return lista_de_execucao
    
class Modelador_Funcional_Desktop():
    
    @staticmethod
    def Run_Pyautomators(dicionario_yaml):
        
        lista_de_execucao=['--summary','--no-logcapture','--no-capture-stderr','--no-capture']
        for item in dicionario_yaml:
            if(item=='tags'):
                for arg in dicionario_yaml[item]:
                    tag_string=str(",").join(dicionario_yaml[item])
                lista_de_execucao.append("--tags="+tag_string)
            if(item=='args'):
                for arg in dicionario_yaml[item]:
                    lista_de_execucao.append('-D'+str(arg)+'='+str(dicionario_yaml[item][arg]))
            if(item=='saida'):
                dir=os.path.join(Ambiente.path_atual(),"docs/reports/")
                lista_de_execucao.append('--junit')
                lista_de_execucao.append('--junit-directory='+dir)                        
                lista_de_execucao.append('--format=json.pretty')
                lista_de_execucao.append('-o='+dir+dicionario_yaml["name"]+dicionario_yaml[item])
                lista_de_execucao.append('--format=sphinx.steps')
                lista_de_execucao.append('-o=log/'+str(dicionario_yaml["name"]).upper())
                lista_de_execucao.append('--format=steps.doc')
                lista_de_execucao.append('-o='+"log/"+"location-steps.log")
                lista_de_execucao.append('--format=steps.usage')
                lista_de_execucao.append('-o='+"log/"+"location-features.log")
        
        return lista_de_execucao
    
class Thread_Run(threading.Thread):
    def __init__(self,list_exec,Item=None):
        threading.Thread.__init__(self)
        self.Item=Item
        self.list_exec=list_exec
    def run(self):  
        valor=None 
        if(self.list_exec['Tipo']=='Web'):
            valor=Modelador_Funcional_Web.Run_Pyautomators(self.list_exec, self.Item) 
        elif(self.list_exec['Tipo']=='Mobile'):
            valor=Modelador_Funcional_Mobile.Run_Pyautomators(self.list_exec, self.Item)
        elif(self.list_exec['Tipo']=='Desktop'):
            valor=Modelador_Funcional_Desktop.Run_Pyautomators(self.list_exec) 
        home(valor)
        
def runner(dicionario_de_execucao):
    if(dicionario_de_execucao['Tipo']=='Web'):
        for Navegador in dicionario_de_execucao['navegadores']:
            Thread_Run(dicionario_de_execucao,Navegador).start()
    elif(dicionario_de_execucao['Tipo']=='Mobile'):
        for Device in dicionario_de_execucao['devices']:
            Thread_Run(dicionario_de_execucao,Device).start()
    elif(dicionario_de_execucao['Tipo']=='Desktop'):
        Thread_Run(dicionario_de_execucao).start()
            
        

def orquestrador(arquivo_yaml):
    
    testes=pegarConteudoYAML(arquivo_yaml)
    for teste in testes: 
        runner(testes[teste])



def _main(arquivo_yaml):
    dicionario_de_execucao=pegarConteudoYAML(arquivo_yaml)
    runner(dicionario_de_execucao)
    
if('__main__'==__name__):

    ARG=argparse.ArgumentParser()
    ARG.add_argument("-P",'--path_yaml',required=True,help="Arquivo Yaml")
    ARG.add_argument("-I",'--indice',required=True,help="Indice de execucao")
    
    valores=dict(vars(ARG.parse_args()))
    
    dicionario_de_execucao=ast.literal_eval(valores["Dict_valor"])
    
    Folder=Dados.pegarConteudoYAML(dicionario_de_execucao['path_yaml'])
    indice=1
    executavel=None
    for Teste in Folder:
        if(indice==dicionario_de_execucao['indice']):
            executavel=Teste
            break
        indice+=1
    if executavel==None:
        Error='''
                Não Existe este Indice para a execução'''
        raise Ambiente_erro(Error)
    runner(dicionario_de_execucao)