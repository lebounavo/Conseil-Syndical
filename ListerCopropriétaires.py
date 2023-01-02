#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ListerCopropriétaires.py
#  
#  Copyright 2022 Michoud <anmic@Anmic-THBK2-12-32B500>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from os import system, name

DateInversee="2022-10-28"

fichierCoprop=open('Copropriétaires '+DateInversee+'.txt','r')
fc=fichierCoprop.read()
lCoprop=fc.split('\n')
fichierCoprop.close

fichierListe=open('ListeCopropriétaires_'+DateInversee+'.csv','w')
fichierListe.write("DateExtraction;Copropriétaire;TypeAppartement;Bâtiment;Escalier;Etage\n")

fichierhledger=open('hledgerCopropriétaires.txt','w')
l2=[]
Nb=0

for i, ligne in enumerate(lCoprop):
	if ('Monsieur' in ligne) or ('Madame' in ligne) or ('Messieurs' in ligne) or ('Mademoiselle' in ligne) or ('Mlle' in ligne) or ('Mesdames' in ligne) or ('Indivision' in ligne):
		fichierListe.write(DateInversee+';'+ligne+';')
		TmpTexte=ligne
		Nb=Nb+i
	if ('F3' in ligne) or ('F4' in ligne):
		l1=ligne.split('	')
		l1[1]=l1[1].replace(' ','')
		l1[2]=l1[2].replace(' ','')
		l1[3]=l1[3].replace(' ','')
		l1[4]=l1[4].replace(' ','')
		fichierListe.write(l1[1]+';')
		fichierListe.write(l1[2]+';')
		fichierListe.write(l1[3]+';')
		fichierListe.write(l1[4]+'\n')
		l2.append(l1[2]+':'+l1[3]+':'+l1[4]+' - '+TmpTexte+' ('+l1[1]+')   1\n')

fichierListe.close

l2.sort
l2.append('Total:\n')
fichierhledger.write(DateInversee.replace('-','/')+' Extraction du '+DateInversee+'\n')
for i, ligne in enumerate(l2):
	fichierhledger.write('	'+ligne)

fichierhledger.close
