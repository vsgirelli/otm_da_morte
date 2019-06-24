/*
 * PFSP
 * Permutational Flowshop Scheduling Problem
 *
* 
*	Conjuntos e parâmetros:
*	• N tarefas a serem processadas
*	• M máquinas disponíveis para processamento
*	• Tempos de processamento Tri > 0, para 1 <= i <= N, 1 <= r <= M 
*	Variáveis:
*	• Cri tempo de completude da tarefa i na máquina r
*	• Dik 1 se a tarefa i precede a tarefa k, 0 caso contrário
*	• P Constante imensa	
*	Restrições:
*	• Tarefas devem ser processadas em sequência
*	• Cada tarefa deve ser processada em todas as máquinas
*	• Processamento sem preempção
*	Objetivo: Minimizar o makespan 
*	Função objetiva: Min Cmax
*	Solução: Ordem alocação das tarefas às máquinas
*/

# Conjunto das tarefas
set N;

# Conjunto das maquinas
set M;

# Conjunto do tempo de processamento das tarefas nas maquinas
set T within (N cross M);

# Parametro de tempo de processamento da tarefa i na maquina r
param time{T};

# Parametro big M
param P := 1e6;

param m;

var c{(i,j) in T} >= 0;
var Cmax >= 0;
var d{(i,k) in N cross N: i < k } binary;

minimize obj_makespan: Cmax;

# Assegura que o tempo de completude de uma tarefa na máquina 1 será pelo menos igual ao seu tempo req para execução
s.t. COMP_M1 {i in N}:  c[i,1] >= time[i,1]; # Cuidado: primeiro índice é da tarefa, segundo é da máquina

# Assegura que uma tarefa nao vá rodar na proxima máquina antes de estar completa na máq anterior
s.t. COMP_M {i in N, r in M: r >= 2}: c[i,r] - c[i, r - 1] >= time[i,r];

# JOB_O1 e JOB_O2 asseguram que uma mesma tarefa vai ser executada antes ou após a outra
s.t. JOB_O1 { i in N, k in N, r in M: k > i}: c[i,r] - c[k,r] + P * d[i,k] >= time[i,r];

s.t. JOB_O2 { i in N, k in N, r in M: k > i}: c[i,r] - c[k,r] + P * d[i,k] <= P - time[k,r];

# O tempo de completude da tarefa vai ser igual ao makespan
s.t. MKSPAN {i in N}: Cmax >= c[i,m];

end;

