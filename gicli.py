import click
import requests
import sys
import json
from datetime import datetime

dns = "GI-lb-1768200546.us-west-2.elb.amazonaws.com" 

@click.group()
def cli(): 
    pass

@cli.command()

def listar():
    r = requests.get('http://'+dns+':8080/tasks/listar')
    print(r.text)

@cli.command()
@click.option('-t', '--title', prompt=True, default=None, help='Coloque o titulo da tarefa')
@click.option('-d', '--description', prompt=True, default=None, help='Coloque a descrição da tarefa')


def adicionar(title, description):
    pub_date = str(datetime.now())
    data = {
        "title": title,
        "pub_date": pub_date,
        "description": description
    }
    r = requests.post('http://'+dns+':8080/tasks/adicionar', json=data)
    print(r.text) 

@cli.command()
@click.option('--id', prompt=True, default=None, help='Coloque o id da tarefa que quer deletar')

def deletar(id):
    r = requests.delete('http://'+dns+':8080/tasks/deletar/'+id)
    print(r.text)  

@cli.command()
@click.option('--id', prompt=True, default=None, help='Coloque o id da tarefa que quer alterar')
@click.option('--title', prompt=True, default=" ", help='Coloque o titulo da tarefa')
@click.option('--description', prompt=True, default=" ", help='Coloque a descrição da tarefa')

def atualizar(id, title, description):
    pub_date = str(datetime.now())
    data = {
        "title": title,
        "pub_date": pub_date,
        "description": description
    }
    r = requests.put('http://'+dns+':8080/tasks/atualizar/'+id, json=data)
    print(r.text)            

if __name__ == '__main__':
    cli()





