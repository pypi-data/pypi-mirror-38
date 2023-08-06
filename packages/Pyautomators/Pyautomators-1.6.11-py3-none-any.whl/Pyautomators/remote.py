# -*- coding: utf-8 -*-
'''
Created on 12 de set de 2018

@author: koliveirab
'''
import http.server
import socketserver
import socket
from Runner_Pyautomators import orquestrador
from Pyautomators.Dados import pegarConteudoYAML
import shutil
''' Esta modulo tem o intuito de trabalhar em conjunto comunica��o entre sistemas e gera��o de Threads, 
trabalhando com cloud, processos e sistemas provedores de servi�os de nuvem e docker'''


def servidor_http(endereco:str,porta:int):
    '''Esta fun��o tem como principio gerar um servidor http'''
    #criando um objeto servidor
    Handler = http.server.SimpleHTTPRequestHandler
    #criando o objeto para servidor socket tcp
    httpd = socketserver.TCPServer((endereco, porta), Handler)
    #subindo o servidor e rodando com while==true
    httpd.serve_forever()
    
class Runner_Master():
    def __init__(self,file_yaml):
        self.file=pegarConteudoYAML(file_yaml)
        
    def execute(self):
        lista=[]
        for execute in self.file:
            self.Client=socket.socket()
            host,port=self.file[execute]['Remote'],9000
            self.Client.connect((host,port))
            self.Client.sendall(str(execute).encode(encoding='utf_8'))
            if(self.Client.recv(1024).decode('utf-8')=="Finalizado"):
                self.Client.sendall(str("ok").encode(encoding='utf_8'))
                teste=self.Client.recv(1024).decode('utf-8')
                with open('docs/docs{}.zip'.format(str(host).replace(".", "")),'wb') as file:
                    file.write(teste)
                    file.close()
                teste=self.Client.recv(1024).decode('utf-8')
                with open('docs/logs{}.zip'.format(str(host).replace(".", "")),'wb') as file:
                    file.write(teste)
                    file.close()
            else: 
                self.Client.close()

class Runner_Client():
    def __init__(self,file_yaml):
        #abrindo um objeto socket
        self.Server=socket.socket()
        #recebendo todos os os parametros
        #pegando o tamanho de todos os testes para rodar 
        self.Endereco=(socket.gethostbyname(socket.gethostname()),9000)
        self.Server.bind(self.Endereco)
        #abrindo o numero de usuarios simultaneos igual ao tamanho de testes que iram rodar
        self.Server.listen(1)
        self.yaml=file_yaml
    def execute(self):  
        #criando uma lista para receber informações de todos os servidores  
        c,addr =self.Server.accept()          
        #adicionando o client na lista de registro
        self.instancia=c.recv(1024).decode('utf-8')
        try:
            orquestrador(self.yaml,self.instancia)
            self.Server.sendall("Finalizado".encode())
            if(self.Server.recv(1024).decode('utf-8')=="ok"):
                shutil.make_archive("docs/docs", "zip",  base_dir="docs")
                shutil.make_archive('docs/logs',"zip",base_dir="log")
                with open('docs/docs.zip','rb') as file:
                    self.Server.sendall(file.read())
                    file.close()
                with open('docs/logs.zip','rb') as file:
                    self.Server.sendall(file.read())
                    file.close()
        except:
            c.sendall("Error".encode('utf-8'))
        finally:
            c.close()