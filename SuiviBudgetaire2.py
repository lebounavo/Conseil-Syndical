# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  PreparerBudget.py

# from __future__ import unicode_literals
from os import system, name
from decimal import Decimal

def ChargerDicoComptes():
	fichierCpte=open('HierarchieComptes.txt','r')
	fc=fichierCpte.read()
	l3=fc.split('\n')
	for i,ligne in enumerate(l3):
		l4=ligne.split(";")
		if len(l4)==2:
			DicoComptes[l4[0]]=l4[1]
	fichierCpte.close

fichier=open("2022-12-10_Budget_Copro.txt",'r')
fichier2=open("Budget_Ecart.csv",'w')

DicoComptes={}
ChargerDicoComptes()

i=0
fichier2.write("Compte1;Compte2;Compte3;Budget;Réalisé")
while(True):
	#read next line
	line = fichier.readline()
	#if line is empty, you are done with all lines in the file
	if not line:
		break
	#you can access the line
	ligne=line.strip()
	if ligne!="":
		if (ligne in DicoComptes):
			Compte=DicoComptes[ligne]
			Compte=Compte.replace(":",";")
			#fichier csv
			fichier2.write(Compte)
			i=0
		else:
			Compte=""
			i=i+1
		#print(str(i)+"--"+ligne)
		if i==4:
			TmpTexte=ligne.replace(" ","")
			try:
				MontantBudgete=float(TmpTexte)
			except ValueError:
				MontantBudgete=-1
			fichier2.write(";"+TmpTexte.replace(".",","))
		if i==5:
			TmpTexte=ligne.replace(" ","")
			if MontantBudgete>=0:
				MontantRealise=float(TmpTexte)
				MontantEcart=MontantRealise-MontantBudgete
			fichier2.write(";"+TmpTexte.replace(".",","))
			if MontantBudgete>=0:
				fichier2.write(";"+str(MontantEcart).replace(".",","))
				if MontantBudgete>0:
					fichier2.write(";"+str(MontantRealise/MontantBudgete).replace(".",","))
				else:
					fichier2.write(";0,00")
			fichier2.write("\n")

#close file
fichier.close
fichier2.close

# traitement hledger
fichier2=open("Budget_Ecart.csv",'r')
fichier3=open("Budget_hledger.txt",'w')

fk=fichier2.read()
l1=fk.split('\n')
fichier2.close
#print(l1)
fichier3.write('commodity € 999.999,99\n')

Montant=""
MontantBudget=0.0
fichier3.write("\n")
fichier3.write("2022/01/01 Budget voté\n")

for i,ligne in enumerate(l1):
	print(str(i)+"--"+ligne)
	l2=ligne.split(";")
	if len(l2)==7 and i>0:
		Montant=l2[3].replace(",",".")
		MontantBudget=MontantBudget+float(Montant)
		if float(Montant)!=0:
			fichier3.write("	Ecart:"+l2[0]+":"+l2[1]+":"+l2[2]+"		€ "+Montant+"\n")
fichier3.write("	Budget		€ -"+str(MontantBudget)+"\n")

for i,ligne in enumerate(l1):
	l2=ligne.split(";")
	#print(str(i)+"--"+str(len(l2))+"--"+ligne)
	if len(l2)==7 and i>0:
		Montant=l2[4].replace(",",".")
		if float(Montant)!=0:
			MontantNeg="-"+ Montant
			MontantNeg=MontantNeg.replace("--","")
			fichier3.write("\n")
			fichier3.write("2022/01/01 Dépense "+l2[2]+"\n")
			fichier3.write("	Dépense		€ "+Montant+"\n")
			#print l2[4].replace(",",".")+ "->" + str(Montant)+" ->"+str(Montant>0)+" ->"+str(l2[4].find('-'))
			#if l2[4].find('-')>=0:
			fichier3.write("	Ecart:"+l2[0]+":"+l2[1]+":"+l2[2]+"		€ "+MontantNeg+"\n")
			#else:
				#l2[4]=l2[4].replace("-","")
				#fichier3.write("  Ecart:"+l2[0]+":"+l2[1]+":"+l2[2]+" €  "+(l2[4].replace(",","."))+"\n")

fichier3.close
