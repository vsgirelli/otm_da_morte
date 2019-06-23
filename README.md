Autores:
Leandro de Oliveira Pereira
Pedro Trindade
Valéria Soldera Girelli


Este trabalho busca resolver o Permutational Flowshop Scheduling Problem utilizando
Simulate Annealing como meta-heurística.

O código está escrito na linguagem Python3.
As bibliotecas necessárias para o funcionamento do código são:
numpy
random
pprint
time
math
os

A instalação das bibliotecas acima citadas pode ser feita da seguinte forma:
pip install numpy random pprint time math os

Intruções de execução:

O código já realiza as 10 execuções com as 10 seeds diferentes, sendo estas variadas
no intervalo de 1 a 10. Desse modo, não há necessidade de informar uma seed na
execução do código.

python3 main.py inputs/<input_file>
Sendo <input_file> o nome de um arquivo contendo uma instância.

Caso o usuário tenha interesse em informar uma seed diferente, o mesmo pode ser feito
como indicado a seguir:

python3 main.py inputs/<input_file> <seed>


Cada execução gera um arquivo de saída que fica disponível no diretório results.
O nome do arquivo de saída é dado por:
<input_file>_<number_of_seeds>

