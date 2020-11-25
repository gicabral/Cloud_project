#!/usr/bin/env python3

import click
import requests
import sys
import json


@click.command()
@click.option('--listar', default=None, help='Coloque o DNS do load balancer para listar todas as tarefas')

def listar(listar):
    r = requests.get('http://'+listar+':8080/tasks/listar')
    print(r.text)

@click.command()
@click.option('-a','--adicionar', default=None, help='Coloque o DNS do load balancer para adicionar uma tarefa')
@click.option('-t', '--title', prompt=True, default=None, help='Coloque o titulo da tarefa')
@click.option('-p', '--pub_date', prompt=True, default=None, help='Coloque a data da tarefa')
@click.option('-d', '--description', prompt=True, default=None, help='Coloque a descrição da tarefa')


def adicionar(adicionar, title, pub_date, description):
    data = {
        "title": title,
        "pub_date": pub_date,
        "description": description
    }
    r = requests.post('http://'+adicionar+':8080/tasks/adicionar', json=data)
    print(r.text) 

@click.command()
@click.option('--deletar', default=None, help='Coloque o DNS do load balancer para deletar uma tarefa')
@click.option('--id', prompt=True, default=None, help='Coloque o id da tarefa que quer deletar')

def deletar(deletar, id):
    r = requests.delete('http://'+deletar+':8080/tasks/deletar/'+id)
    print(r.text)  

@click.command()
@click.option('--atualizar', default=None, help='Coloque o DNS do load balancer para deletar uma tarefa')
@click.option('--id', prompt=True, default=None, help='Coloque o id da tarefa que quer alterar')
@click.option('--title', prompt=True, default=" ", help='Coloque o titulo da tarefa')
@click.option('--pub_date', prompt=True, default=" ", help='Coloque a data da tarefa')
@click.option('--description', prompt=True, default=" ", help='Coloque a descrição da tarefa')

def atualizar(atualizar, id, title, pub_date, description):
    if title!= "" and pub_date != "" and description != "":
        data = {
            "title": title,
            "pub_date": pub_date,
            "description": description
        }
    r = requests.put('http://'+atualizar+':8080/tasks/atualizar/'+id, json=data)
    print(r.text)            

if __name__ == '__main__':
    if sys.argv[1] == '--listar':
        listar()
    if sys.argv[1] == '--adicionar':    
        adicionar()
    if sys.argv[1] == '--deletar':
        deletar()
    if sys.argv[1] == '--atualizar':
        atualizar()
    if sys.argv[1] == '--help':    
        print("Digite --listar DNS_load_balancer para listar todas as tarefas. \n",
        "Digite --adicionar DNS_load_balancer para adicionar uma tarefa \n ", 
        "Digite --deletar DNS_load_balancer --id ID para deletar uma tarefa \n",
        "Digite --atualizar DNS_load_balancer --id ID para atualizar uma tarefa \n")





