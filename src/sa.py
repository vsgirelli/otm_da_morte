#!/usr/bin/python3

from random import *
import numpy as np
import sys, getopt
import _thread
from time import gmtime, strftime
from queue import Queue,PriorityQueue
import time
import math
import glob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import hashlib

def test_sat_old(it):
	r = np.logical_not(np.bitwise_xor(cla,it))
	valid = True;
	for i in range(int(r.size/3)):
		x = r[i] or r[i+1] or r[i+2]
		if(not x):
			valid = False
			break
	return valid


def test(it,cla):

	valid = True;
	tests = []
	for i in range(len(cla)):
		if cla[i]<0 :
			a = it[-int(cla[i])]
			tests.append(a)
		else:
			a = it[int(cla[i])]
			tests.append(a)
	ponto = 0
	for i in range(int(len(tests)/3)):
		x = tests[i] or tests[i+1] or tests[i+2]
		if(not x):
			ponto+=1

	return ponto

def pertubation(poss,percent,tmax):
	final = np.copy(poss)
	for i in range(percent):
		x = randint(0,tmax-1)
		if(final[x]==0):
			final[x]=1
		else:
			final[x]=0
	return final


def cool0(i,N,T0,TN):
	return (T0-i*((T0-TN)/N))

def cool1(i,N,T0,TN):
	return (T0*((TN/T0)**(i/N)))

def cool2(i,N,T0,TN):
	A=(T0-TN)*(N+1)/(N)+N/2
	B=10#T0-A
	return A/(i+1)+B

def cool3(i,N,T0,TN):
	A=math.log(T0,N)
	return T0-i**A

def cool4(i,N,T0,TN):
	exxx = ((25/N)*(i-N/2))
	exx = math.exp(exxx)
	return (T0-TN)/(1+exx)+TN

def cool5(i,N,T0,TN):
	return .5*(T0-TN)*(1+math.cos(i*math.pi/N))+TN

def cool6(i,N,T0,TN):
	return 0.5*(T0-TN)*(1-math.tanh(10*i/N-5))+TN

def cool7(i,N,T0,TN):
	return (T0-TN)/math.cosh(10*i/N)+TN

def cool8(i,N,T0,TN):
	A = (1/N)*math.log(T0/TN)
	return T0*(math.e**(-A*i))

def cool9(i,N,T0,TN):
	A = (1/(N**2))*math.log(T0/TN)
	return T0*(math.e**(-A*(i**2)))

def calc_temp(i,N,T0,TN,tipo):
	if(tipo==0):
		return cool0(i,N,T0,TN)
	elif(tipo==1):
		return cool1(i,N,T0,TN)
	elif(tipo==2):
		return cool2(i,N,T0,TN)
	elif(tipo==3):
		return cool3(i,N,T0,TN)
	elif(tipo==4):
		return cool4(i,N,T0,TN)
	elif(tipo==5):
		return cool5(i,N,T0,TN)
	elif(tipo==6):
		return cool6(i,N,T0,TN)
	elif(tipo==7):
		return cool7(i,N,T0,TN)
	elif(tipo==8):
		return cool8(i,N,T0,TN)
	elif(tipo==9):
		return cool9(i,N,T0,TN)
	else:
		return cool0(i,N,T0,TN)

def main(argv):
	mat = []
	files = glob.glob("TestesSAT/*.cnf")

	for mfile in files:
		print("File Atual: "+mfile)
		lines = open(mfile).readlines()
		vas = lines[7].split()
		nvar = int(vas[2])
		ncla = int(vas[3])
		clau = []
		for y in range(ncla):
			a = list(map(float, lines[8+y].split()))
			clau.append(a[0])
			clau.append(a[1])
			clau.append(a[2])

		ite0 = 50000
		T0 = 100.0
		t = np.arange(0., ite0, 1)
		TN = 1.0
		N_V = 30


		for tipo in range(0,10):
			T=T0
			list_pontos = np.zeros((N_V,ite0))
			list_temp = np.zeros((ite0))
			list_tempos = np.zeros((N_V))
			for ixi in range(N_V):
				ite = 0

				poss_atual = np.zeros(ncla)
				ponto_atual = test(poss_atual,clau)
				print("Execucao:"+str(ixi) + " Funcao:"+str(tipo))
				start_time = time.time()
				while(ite<ite0):
					T=calc_temp(ite,ite0,T0,TN,tipo)-1
					if(T<0):
						T=0
					poss = pertubation(poss_atual,1, ncla)
					ponto = test(poss,clau)
					list_pontos[ixi][ite]= (ncla-ponto)/ncla
					list_temp[ite]=(T/T0)
					delta = ponto - ponto_atual
					ite+=1
					if(delta<=0):
						ponto_atual = ponto
						poss_atual = poss
					else:
						if(T>0 and math.exp(-delta/T) > uniform(0, 1)):
							ponto_atual = ponto
							poss_atual = poss
				list_tempos[ixi]=(time.time() - start_time)

			real_final = list_pontos.mean(axis=0)
			listamenos = list_pontos.max(axis=1)

			print("Min:"+str(listamenos.min())+" Max:"+str(listamenos.max())+" Mean:"+str(listamenos.mean())+" Srd:"+str(listamenos.std()));
			plt.clf()
			plt.xlim([0,ite0])
			plt.ylim([0,1])
			plt.plot(t,real_final.tolist(),'r-',t,list_temp,'b-')
			plt.savefig(mfile+"_"+str(tipo)+"_Media_"+str(N_V)+".png",dpi=300)
			plt.clf()
			plt.xlim([0,ite0])
			plt.ylim([0.8,1])
			plt.plot(t,real_final.tolist(),'r-')
			plt.savefig(mfile+"_"+str(tipo)+"_Media_"+str(N_V)+"_08.png",dpi=300)

		#break

	print('Encerrado')

if __name__ == "__main__":
	main(sys.argv[1:])

