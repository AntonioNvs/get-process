# GetProcess

📜 Projeto com o foco de detectar se as tarefas desejadas estão ativas e cadastrar suas informações em um banco de dados.

<p align="center">
<img src="https://i.ibb.co/FBrh5Hg/h.gif" alt="Review pequeno do que o projeto faz" border="0">
</p>

💡 O objetivo da aplicação é conseguir adquirir dados sobre o uso pessoal de programas previamentes selecionados (tempo de utilização, RAM e CPU), com o intuito de gerar insights a partir desses dados, como os gastos de hardware de cada programa e os horários de maior utilização.

## 📈 Funcionalidades

#### Arquivo de tarefas desejadas

O Windows possui, por si só, diversas tarefas rodando simultaneamente, em que a maioria vai ser de nenhum interesse para a análise pessoal dos dados. Portanto, tendo em vista que a biblioteca nos entrega todas as tarefas que estão em execução naquele momento, foi implementado uma mecânica de selecionar as tarefas pelo nome de execução em um arquivo de texto, pois:
* _Torna mais dinâmico o acesso a adição ou remoção de tarefas_
* _Não interferirá nos dados do banco_
* _Na próxima execução do programa, o arquivo acrescentado já será executado_
* _Basta apertar a tecla 'E' que abrirá a parte de edição_

<p align="center">
<img src="https://i.ibb.co/nnP7GRL/open.gif" alt="Abrindo o arquivo de lista de tarefas" border="0">
</p>

#### Salvar os dados em um banco de dados SQLite

Ao detectar as tarefas, o programa salva os dados recebidos em um banco de dados automaticamente, de forma dinâmica, e com atualizações a cada período de tempo pré-definido. Ou seja, quando um programa é iniciado, a cada X segundos uma atualização de seus dados (CPU e RAM) é salva no banco.


## 💻 Configuração para Desenvolvimento

A única dependência do projeto é o [psutil](https://psutil.readthedocs.io/en/latest/), portanto, necessita-se somente instalar ela.

```sh
pip install psutil
python interface.py
```

## 📋 Metas

* Realizar uma interface gráfica com os dados em tempo real
* Colocar dados de temperatura de hardware, GPU e bateria
* Otimizar o gasto de processamento do programa
* Conseguir realizar modelos de Machine Learning a partir dos dados gerados.


Antônio Caetano Neves Neto – [Linkedin](https://www.linkedin.com/in/ant%C3%B4nio-neves-88b7b01b8/) – an.caetano.neves@gmail.com
