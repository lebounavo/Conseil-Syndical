# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  GenererEcritures.py

# from __future__ import unicode_literals
from os import system, name
from decimal import Decimal

Annee="2099"
MontantBudget="234315"


def ChargerDicoComptes():
	fichierCpte=open('HierarchieComptes.txt','r')
	fc=fichierCpte.read()
	l3=fc.split('\n')
	
	for i,ligne in enumerate(l3):
		l4=ligne.split(";")
		if len(l4)==2:
			DicoComptes[l4[0]]=l4[1]

	fichierCpte.close

fichierCles=open('ClesRepartition.txt','r')
fk=fichierCles.read()
l6=fk.split('\n')
fichierCles.close
print(l6)

fichier=open("Depenses_"+Annee+".txt",'r')
f=fichier.read()
l1=f.split('\n')
fichier.close

fichier2=open("Ecritures_"+Annee+".txt",'w')
Compte=""
Montant=""
MontantNeg=""
MontantCumul=0.00
MontantCumulPrecedent=0.00
Commentaire=""
FlagCompte=0
Cle=""

DicoComptes={}
ChargerDicoComptes()

#Ecriture du budget total pour l'année
fichier2.write(Annee+"/01/01 Budget voté \n")
fichier2.write("	[Ecart]						€ "+MontantBudget+"\n")
fichier2.write("	[Budget]					€ -"+MontantBudget+"\n")
fichier2.write("\n")

for i,ligne in enumerate(l1):
	ligne=ligne.replace("	","  ")
	while ('   ' in ligne):
		ligne=ligne.replace("   ","  ")
	if ((ligne.replace(" ","")<>"") & (i>7) & (len(ligne)!=0)):
		if (ligne[2:] in l6):
			Cle=ligne[2:]
			print("-----------------------")
			print ("Cle :"+ligne)
			if (Cle[:2] in ("01","07","70","83")):
				Cle="REPARTITIONS COMMUNES:"+Cle
			else:
				Cle="REPARTITIONS SPECIFIQUES:"+Cle	
		if ((len(ligne)>5) & (ligne[0]!=" ")):
			if (ligne[:5]!="Total"):
				l2=ligne.split("(")
				if len(l2)==2:                          # Ligne de définition du Compte
					Compte=l2[1].replace(" ","")
					Compte=Compte.replace(")","")
					#print(Compte)
					#print(len(Compte))
					if (Compte in DicoComptes):
						Compte=DicoComptes[Compte]
					else:	
						Compte=Compte+" - "+l2[0]
					FlagCompte=1
					MontantCumulPrecedent=0.00
				else:
					l3=ligne.split("  ")               # Traitement écriture
					#fichier2.write(ligne+"\n")
					Montant=l3[len(l3)-2]
					MontantCumul=Decimal(l3[len(l3)-1].replace(" ",""))
					print("-----------------------")
					print(MontantCumulPrecedent)
					print(MontantCumul)
					Commentaire=ligne.replace(Montant,"")
					Commentaire=Commentaire.replace("-"," ")
					Commentaire=Commentaire.replace('\\\E9',"é")
					Commentaire.strip()
					l5=Commentaire.split(" ")
					DateEcriture=l5[0]
					#print(DateEcriture)
					l5=DateEcriture.split("/")
					#print(len(l5))
					if len(l5)==3:
						if len(Cle)>0:
							Commentaire=Commentaire.replace(DateEcriture,l5[2]+"/"+l5[1]+"/"+l5[0])+" - "+Cle
						else:
							Commentaire=Commentaire.replace(DateEcriture,l5[2]+"/"+l5[1]+"/"+l5[0])
					Montant=l3[len(l3)-2].replace(" ","")
					if (MontantCumul<MontantCumulPrecedent):
						FlagSigneNegatif=True
					else:
						FlagSigneNegatif=False
					print(FlagSigneNegatif)
					print(Montant)
					if (Montant[0]=="-"):
						FlagSigneNegatif=not(FlagSigneNegatif)
					print(FlagSigneNegatif)
					if not ('Total' in ligne) & (FlagCompte==0):
						fichier2.write(Commentaire.replace("  "," ")+"\n")
						MontantNeg="-"+Montant
						MontantNeg=MontantNeg.replace("--","")
						if FlagSigneNegatif:
							fichier2.write("	"+Compte+"			€  -"+Montant+"		; Cle: "+Cle+"\n")
							fichier2.write("	Dépenses					€ "+Montant+"\n")
							fichier2.write("	[Dépenses]					€ "+MontantNeg+"\n")
							fichier2.write("	[Ecart]						€ "+Montant+"\n")
						else:
							fichier2.write("	"+Compte+"			€  "+Montant+"		; Cle: "+Cle+"\n")
							fichier2.write("	Dépenses					€ "+MontantNeg+"\n")
							fichier2.write("	[Dépenses]					€ "+Montant+"\n")
							fichier2.write("	[Ecart]						€ "+MontantNeg+"\n")
						MontantCumulPrecedent=MontantCumul
						fichier2.write("\n")
						FlagCompte=0


fichier2.close
