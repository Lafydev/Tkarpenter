"""
* Copyright 2021 Lafydev 
*
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public
* License as published by the Free Software Foundation; either
* version 3 of the License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
* General Public License for more details.
*
* You should have received a copy of the GNU General Public
* License along with this program; if not,
* see http :// www . gnu . org /licences / .
"""

# Outil de génération d'un design tKinter et du code associé
# 3 étapes : placer dans le tree + créer visuellement + copier le texte pour fichier

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import mod_options
import time
import subprocess
#from os import *

LARGEUR=800
HAUTEUR=700

def signal(event):
   #clic sur un widget
	#pouvoir modifier la taille par ex
	#event.widget["width"] = "40"
	#utiliser partial
	#event.widget["color"] = "red"
	print("click sur "+str(event.widget))
	
def creewidget(widget,parent,id,options,usettk=False):
   """prend widget= nom de la classe widget et
    options sous forme de dictionnaire
    si usettk recupérer la classe de ttk"""
   if usettk :
      widget=getattr(ttk,widget.__name__)
    #Pb pour intégrer les options ttk -> configurées après
   if options=={} or usettk:
         widg=widget(parent)
   else:
         widg=widget(parent,options)
   if usettk : 
      widg.configure(options)
   dictwidg[id]=widg
   widg.bind("<Button-1>",signal);  
   return widg

class Treeview():
   def inserertreeview(nomwidget,id, optpack=""):
      #insere les infos dans le treeview pour vision d'ensemble et modifs
      #detecte le parent suivant focus 
       select=ltree.focus()
       #print(select)
       if select!="" and 'Conteneur' in str(ltree.item(select)['text']):
           #si un containeur est selectionné devient parent du nouveau widget
           ret=ltree.insert(select,'end',id,text=""+nomwidget+"",values=(id,optpack))
           parent=select
           
       else:
           ret=ltree.insert('top', 'end',id,text=""+nomwidget+"",values=(id,optpack))
           #si conteneur ouvrir
           if 'Conteneur' in nomwidget :
               ltree.item(ret, open=TRUE)
           parent='top'
       return(parent)

   def deselectionne():
      #si une ligne du tree selectionnée =>déselectionner
      select=ltree.selection() #liste des elts selectionnés
      if len(select)>0:
         ltree.selection_remove(select[0])
         
   def clicktree(events):
      Treeview.deselectionne()
   
   def haut():
      select=ltree.focus()
      parent=ltree.parent(select)
      row=ltree.index(select) 
      #print(str(parent)+'-'+str(row))
      if select !="":
          
          #ltree.detach(select)
          ltree.move(select,parent,row-1)
   
   def bas():
      select=ltree.focus()
      parent=ltree.parent(select)
      row=ltree.index(select) 
      if select !="":
          ltree.move(select,parent,row+1)  
          
   
def indexunique(base):
   """prend une base d'index comme btn pour un bouton
   renvoie un index unique pour le bouton comme btn22"""
   i=1
   while base+str(i) in dictwidg:
      i=i+1
   return(base+str(i))

def extrairelisteoptions(NomWidget):
   #former listeoptions a partir du fichier
   listeoptions=[]
   localise=False
   fich=open('widgets.info','r',encoding='utf-8')
   for lig in fich:
      if (lig.strip("\n") =="["+NomWidget+"]"): 
         localise=True 
      elif (lig.strip(" ")[0]=="[") :
         localise =False
      elif (localise==True) :
         listeoptions.append(lig.strip(' \t\n'))
   return(listeoptions)
            
def formedicopt(opt):
   dicopt={}
   for arg in opt.args :
      (x,y)= arg.split("=")
      dicopt[x]=y.strip('"')
   return(dicopt)
            
class Widget():
   #------------------- Widgets CONTENEURS ----------------------
   def cdeframe():
      widg="Frame"
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      if (cancel != "True"):
         #opt.args contient les options récupérées ss forme de liste
         #à mettre sous forme de dict
         ind=indexunique("fr")
         dicopt=formedicopt(opt)  
         dicpack={}
         dicpack['side']="left"
         dicpack['padx']="2m"
         dicpack['pady']="2m"
         parent=Treeview.inserertreeview("Conteneur "+widg,ind,dicpack)
         #inserertreeview("Conteneur Frame ",ind,dicpack)
         CodePython.ecritdata(ind,Frame,parent,dicopt)
         CodePython.ecritpack(ind,dicpack)

         fr=creewidget(Frame,dictwidg[parent],ind,dicopt)
         fr.pack(dicpack)
        
      
   def cdelabelframe():
      widg="LabelFrame"
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      if (cancel != "True"):
         ind=indexunique("fr")
         dicopt=formedicopt(opt) 
         parent= Treeview.inserertreeview("Conteneur "+widg,ind)
         CodePython.ecritdata(ind,LabelFrame,parent,dicopt)
         dicpack={}
         dicpack['padx']="2m"
         dicpack['pady']="2m"
         CodePython.ecritpack(ind,dicpack)

         fr=creewidget(LabelFrame,dictwidg[parent],ind,dicopt)
         fr.pack(padx="2m", pady="2m")

   def cdepanedwindow():
      #donner choix horizontal/vertical
      widg="PanedWindow"
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      if (cancel != "True"):
         ind=indexunique("pw")
         dicopt=formedicopt(opt) 
            
         parent=Treeview.inserertreeview("Conteneur "+widg,ind)
         CodePython.ecritdata(ind,PanedWindow,parent,dicopt)
         pw=creewidget(PanedWindow,dictwidg[parent],ind,dicopt)
         
         ltree.focus(ind)
         indlf1=indexunique("lf")
         Treeview.inserertreeview("Conteneur Labelframe 1",indlf1)
         fich.insert(END,"\t\t"+str(indlf1)+"= ttk.Labelframe("+str(ind)+", text='Pane1', width=100, height=100)\n")
         fich.insert(END,"\t\t"+str(ind)+'.add('+str(indlf1)+')\n')
         lf1 = LabelFrame(pw, text='Pane1', width=100, height=100)
         pw.add(lf1)
         dictwidg[indlf1]=lf1

         indlf2=indexunique("lf")
         Treeview.inserertreeview("Conteneur Labelframe 2", indlf2 )
         #2eme plus petit si horiz => en largeur 
         if dicopt['orient'] == "horizontal" : 
               fich.insert(END,"\t\t"+str(indlf2)+" = ttk.Labelframe("+str(ind)+", text='Pane2', width=80, height=100)\n")
               lf2 = LabelFrame(pw, text='Pane2', width=80, height=100) 
         else:
               fich.insert(END,"\t\t"+str(indlf2)+" = ttk.Labelframe("+str(ind)+", text='Pane2', width=100, height=80)\n")
               lf2 = LabelFrame(pw, text='Pane2', width=100, height=80)
         fich.insert(END,"\t\t"+str(ind)+'.add('+str(indlf2)+')\n')
         
         pw.add(lf2)
         pw.pack() 
         CodePython.ecritpack(ind)
         dictwidg[indlf2]=lf2
         #enleve le focus pour la suite
         ltree.focus('')
      
   def cdenotebook():
      #ttk widget
      widg = "Notebook"
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      if (cancel != "True"):
         dicopt=formedicopt(opt)
         ind=indexunique("nb")
         parent=Treeview.inserertreeview("Conteneur ttk Notebook",ind )
         ltree.focus(ind)
         
         CodePython.ecritdata(ind,ttk.Notebook,parent,dicopt, usettk=True)
         dicpack={}
         dicpack['side']="left"
         dicpack['padx']="2m"
         dicpack['pady']="5m"
         CodePython.ecritpack(ind,dicpack)
        
         nb=creewidget(ttk.Notebook,dictwidg[parent],ind,dicopt,usettk=True)
         nb.pack(side="left", padx="2m", pady="5m")

         #insere 2 label frame pour matérialiser les 2 pages
         indlf1=indexunique("lf")
         Treeview.inserertreeview("Conteneur LabelFrame 1",indlf1)
      
         fich.insert(END,"\t\t"+str(indlf1)+' = Frame('+ind+')\n')
         fich.insert(END,"\t\t"+str(indlf1)+'.pack()\n')
         fich.insert(END,"\t\t"+str(ind)+'.add('+str(indlf1)+', text="Page1")\n')
         f1 = Frame(nb)
         f1.pack(side="left")
         nb.add(f1, text="Page1")
         dictwidg[indlf1]=f1

         indlf2=indexunique("lf")
         Treeview.inserertreeview("Conteneur LabelFrame 2",indlf2 )
         fich.insert(END,"\t\t"+str(indlf2)+' = Frame('+ind+')\n')
         fich.insert(END,"\t\t"+str(indlf2)+'.pack()\n')
         fich.insert(END,"\t\t"+str(ind)+'.add('+str(indlf2)+', text="Page2")\n')
         f2 = Frame(nb)
         f2.pack(side="left")
         nb.add(f2, text="Page2")
         dictwidg[indlf2]=f2 
         ltree.focus('')
   
   def cdescrollbar():
      widg="Scrollbar"
      ind=indexunique("sc")
      parent=Treeview.inserertreeview(widg,ind)
      dicopt={}
      
      CodePython.ecritdata(ind,Scrollbar,parent,dicopt)
      dicpack={}
      dicpack['side']="left"
      dicpack['fill']="y"
      CodePython.ecritpack(ind,dicpack)
      
      #associer à l'objet précédent
      #command=ind.yview)\n' ou xview pour horiz
      #ind.configure(yscrollcommand=sc.set)
      asc=creewidget(Scrollbar,dictwidg[parent],ind,dicopt)
      asc.pack(side="left", fill="y")
      
   def cdebutton():
      #choix state, text 
      widg="Button"
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      if (cancel != "True"):
         #retour au destroy de la toplevel
         ind=indexunique("btn")
         parent=Treeview.inserertreeview(widg,ind)
         dicopt={}
         for arg in opt.args :
            (x,y)= arg.split("=")
            dicopt[x]=y.strip('"')
         print(dicopt)  

         CodePython.ecritdata(ind,Button,parent,dicopt)
         dicpack={}
         dicpack['side']="left"
         CodePython.ecritpack(ind,dicpack)

         btn=creewidget(Button,dictwidg[parent],ind,dicopt)
         btn.pack(dicpack)
      
      
   def cdemenubutton():
      widg="Menubutton"
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      if (cancel != "True"):
         #retour au destroy de la toplevel
         ind=indexunique("mb")
         dicopt=formedicopt(opt) 
         
         parent=Treeview.inserertreeview("Widget "+widg,ind )
         CodePython.ecritdata(ind,Menubutton,parent,dicopt)
         dicpack={}
         dicpack['side']="left"
         CodePython.ecritpack(ind,dicpack)
         
         #fich.insert(END,'mb=Menubutton(root, text="'+libelle+'", underline=0)\n')
         fich.insert(END,'\t\tmenu1=Menu('+str(ind)+', tearoff=False)\n')
         fich.insert(END,'\t\tmenu1.add_separator()\n')
         fich.insert(END, "\t\t"+str(ind)+'["menu"]=menu1\n')
         mb=creewidget(Menubutton,dictwidg[parent],ind,dicopt)
         #mb=Menubutton(top1, text=""+libelle+"", underline=0)
         menu1=Menu(mb, tearoff=False)
         menu1.add_separator() 
         mb["menu"]=menu1
         mb.pack(dicpack)

   def cderadiobutton():
      ind=indexunique("rb")
      widg="Radiobutton"
      parent=Treeview.inserertreeview(widg,ind )       
      fich.insert(END,"\n\t\t#<"+str(ind)+":Radiobutton>\n")
      
      fich.insert(END,'\t\tvar=StringVar()\n')
      fich.insert(END,'\t\tfor txt in ("bouton1", "bouton2"):\n')
      
      fich.insert(END,'\t\t\tRadiobutton(text=txt, variable=var, value=txt, anchor="w").pack(side="top", fill="x")\n')
      fich.insert(END,"\t\t#</Radiobutton>\n")
      var=StringVar()

      
      for txt in ("bouton1", "bouton2"):
         dicopt={}
         dicopt['text']=txt
         dicopt['value']=txt
         dicopt['anchor']="w"
         dicopt['variable']= var
         rb=creewidget(Radiobutton,dictwidg[parent],ind,dicopt)
         rb.pack(side="top", fill="x")
         #Radiobutton(dictwidg[parent],text=txt, variable=var, value=txt, anchor="w").pack(side="top", fill="x")


   def cdecanvas():
      #donne choix background, borderwidth, relief
      widg="Canvas"
      ind=indexunique("ca")
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      if (cancel != "True"):
         parent=Treeview.inserertreeview(widg,ind)
         dicopt=formedicopt(opt)
         
         CodePython.ecritdata(ind,Canvas,parent,dicopt)
         CodePython.ecritpack(ind)
       
         ca=creewidget(Canvas,dictwidg[parent],ind,dicopt)
         ca.pack()

   def cdescale():
      #choix orientation
      widg="Scale"
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      if (cancel != "True"):
         ind=indexunique("sc")
         parent=Treeview.inserertreeview(widg,ind )
      
         dicopt=formedicopt(opt) 
         
         CodePython.ecritdata(ind,Scale,parent,dicopt)
         CodePython.ecritpack(ind)
         curseur=creewidget(Scale,dictwidg[parent],ind,dicopt)
         curseur.pack()
      
   def cdecheckbutton():
      widg="Checkbutton"
      ind=indexunique("cc")   
      parent=Treeview.inserertreeview(widg,ind )
      
      fich.insert(END,"\n\t\t#<"+str(ind)+":Checkbuttons>\n")
      fich.insert(END,'\t\tcases = {}\n')
      fich.insert(END,'\t\tfor txt in ("case1", "case2"):\n')
      fich.insert(END,'\t\t\tcases["+txt+"]=False\n')
      fich.insert(END,'\t\t\tCheckbutton(text=txt, variable=cases["+txt+"], anchor="w").pack(side="top", fill="x")\n')
      fich.insert(END,"\t\t#</Checkbuttons>\n")
      #prevoir un index unique sinon tous les groupes de cases à cocher ont la mm variable
      cases= {}
      for txt in ("case1", "case2"):
         dicopt={}
         dicopt['text']=txt
         cases["+txt+"]=False
         dicopt['variable']="cases["+txt+"]"
         dicopt['anchor']="w"
         cc=creewidget(Checkbutton,dictwidg[parent],ind,dicopt)
         cc.pack(side="top", fill="x")
         #Checkbutton(dictwidg[parent],text=txt, variable=cases[txt], anchor="w").pack(side="top", fill="x")

   def cdelabel():
      widg="Label"
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      if (cancel != "True"):
         ind=indexunique("lbl")
         dicopt=formedicopt(opt) 
         dicpack={}
         dicpack['side']="left"
         dicpack['padx']="2m"
         dicpack['pady']="2m"
         
         parent=Treeview.inserertreeview(widg,ind,dicpack)
         CodePython.ecritdata(ind,Label,parent,dicopt)
         CodePython.ecritpack(ind,dicpack)
         
         lbl=creewidget(Label,dictwidg[parent],ind,dicopt)
         lbl.pack(dicpack)  

   def cdelistbox():
      widg="Listbox"
      ind=indexunique("lb")
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      if (cancel != "True"):   
         parent=Treeview.inserertreeview(widg,ind)
      
         dicopt=formedicopt(opt) 
         
         CodePython.ecritdata(ind,Listbox,parent,dicopt)   
         fich.insert(END,"\t\t"+str(ind)+'.insert(1,"valeur1")\n')
         fich.insert(END,"\t\t"+str(ind)+'.insert(2,"valeur2")\n')
         dicpack={}
         dicpack['side']="left"
         CodePython.ecritpack(ind,dicpack)
         
         lb=creewidget(Listbox,dictwidg[parent],ind,dicopt)     
         lb.insert(1,"valeur1")
         lb.insert(2,"valeur2")
         lb.pack(dicpack)

   def cdemessage():
      widg="Message"
      ind=indexunique("msg")
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      if (cancel != "True"):   
         parent=Treeview.inserertreeview(widg ,ind)
         dicopt=formedicopt(opt) 
            
         CodePython.ecritdata(ind,Message,parent,dicopt)
         dicpack={}
         dicpack['side']="left"
         CodePython.ecritpack(ind,dicpack) 
          
         msg=creewidget(Message,dictwidg[parent],ind,dicopt)        
         msg.pack(side=pack)      

   def cdespinbox():
      widg="Spinbox"
      ind=indexunique("sp")
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      if (cancel != "True"):   
         parent=Treeview.inserertreeview(widg ,ind)
         dicopt=formedicopt(opt) 
         CodePython.ecritdata(ind,Spinbox,parent,dicopt)
         dicpack={}
         dicpack['side']="left"
         CodePython.ecritpack(ind,dicpack)
         
         sp=creewidget(Spinbox,dictwidg[parent],ind,dicopt) 
         sp.pack(side=pack)
            
   def cdetext():
      widg="Text"
      ind=indexunique("txt")
      
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      
      if (cancel != "True"):
         parent=Treeview.inserertreeview(widg ,ind)
      
         dicopt=formedicopt(opt) 
         
         CodePython.ecritdata(ind,Text,parent,dicopt)
         dicpack={}
         dicpack['side']="left"
         dicpack['expand']="True"
         dicpack['fill']="both"
         CodePython.ecritpack(ind,dicpack)
        
         txt=creewidget(Text,dictwidg[parent],ind,dicopt)   
         txt.pack(dicpack)
      
   def cdeentry():
      widg="Entry"
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      
      if (cancel != "True"):
         #retour au destroy de la toplevel
         ind=indexunique("txt")
         parent=Treeview.inserertreeview(widg ,ind)        
         dicopt=formedicopt(opt) 
        
         CodePython.ecritdata(ind,Entry,parent,dicopt)
        
         fich.insert(END,'\t\tvar=StringVar()\n')
         #fich.insert(END,'txt=Entry(root,width=20, relief="sunken",state=""+etat+"" , bd=2, textvariable=var)\n')
         dicpack={}
         dicpack['side']="left"
         dicpack['padx']="2m"
         dicpack['pady']="2m"
         CodePython.ecritpack(ind,dicpack)
        
         var=StringVar()
         txt=creewidget(Entry,dictwidg[parent],ind,dicopt)   
         #txt=Entry(top1,width=20, relief="sunken", state=etat ,bd=2, textvariable=var)
         txt.pack(dicpack)

   #---------------- CDES WIDGETS TTK ---------------
   def cdetreeview():
      widg="Treeview"
      ind=indexunique("tv")
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      
      if (cancel != "True"):
         parent=Treeview.inserertreeview(widg ,ind)
         dicopt=formedicopt(opt)
         CodePython.ecritdata(ind,ttk.Treeview,parent,dicopt,usettk=True)
         dicpack={}
         dicpack['side']="left"
         dicpack['padx']="2m"
         dicpack['pady']="2m"
         CodePython.ecritpack(ind,dicpack)
        
         tv=creewidget(ttk.Treeview,dictwidg[parent],ind,dicopt,usettk=True) 
         tv.pack(dicpack)
      
   def cdecombobox():
      widg="Combobox"
      ind=indexunique("cmb")
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      
      if (cancel != "True"):
         parent=Treeview.inserertreeview(widg,ind )
         dicopt=formedicopt(opt)
         CodePython.ecritdata(ind,ttk.Combobox,parent,dicopt,usettk=True)
         dicpack={}
         dicpack['side']="left"
         dicpack['padx']="2m"
         dicpack['pady']="2m"
         CodePython.ecritpack(ind,dicpack)
        
         cmb=creewidget(ttk.Combobox,dictwidg[parent],ind,dicopt,usettk=True) 
         cmb.pack(dicpack)

   def cdeprogressbar():
      widg="Progressbar"
      ind=indexunique("pgb")
      listeoptions= extrairelisteoptions(widg)
      cancel=StringVar()
      cancel.set("False")
      opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
      cancel=str(cancel.get())
      
      if (cancel != "True"):
         parent=Treeview.inserertreeview(widg,ind)
         
         dicopt=formedicopt(opt)
         CodePython.ecritdata(ind,ttk.Progressbar,parent,dicopt,usettk=True)
         dicpack={}
         dicpack['side']="left"
         dicpack['padx']="2m"
         dicpack['pady']="2m"
         CodePython.ecritpack(ind,dicpack)
         
         pgb=creewidget(ttk.Progressbar,dictwidg[parent],ind,dicopt,usettk=True) 
         pgb.pack(side=pack, padx="1m", pady="2m")

#--------------- FONCTIONS DU MODULE PRINCIPAL   
class CodePython():
   def initcode():
      fich.insert(END,'""" Date de création: ')
      ajd=time.localtime()
      # jj/mm/aa
      fich.insert(END,'%d/%d/%d """\n' %(ajd[2],ajd[1],ajd[0]))
      fich.insert(END,"#Fenetre principale\n")
      fich.insert(END,"from tkinter import *\n")
      fich.insert(END,"from tkinter import ttk\n")
      fich.insert(END,"root=Tk()\n\n")
      fich.insert(END,"class Newui:\n")
      fich.insert(END,"\tdef __init__(self,master=None):\n")
      fich.insert(END,"\t\tself.master=master\n")
      
   def ecritdata(raccourci,widget,parent,options,usettk=False):
       """prend widget= nom de la classe widget et
       options sous forme de dictionnaire
       forme une chaine pour le fichier à créer"""
       if usettk :
         nomwidget ="ttk."+widget.__name__
       else: 
         nomwidget =widget.__name__
         
       fich.insert(END,"\n\t\t#<"+raccourci+":"+nomwidget+">\n")
       if parent=='top': parent='root'
       if options=={} :
          data=str(raccourci)+"="+nomwidget+"("+parent+")\n"
       else:
          listeopt= ",".join([ "%s=\"%s\"" %(k,v) for (k,v) in options.items()  ])
          data=str(raccourci)+"="+nomwidget+"("+parent+","+listeopt+")\n"
       #dans tous les cas ecriture
       fich.insert(END,"\t\t"+data)

   def ecritpack(raccourci,opt={}):
      """pack et fermeture de </balise>  """
      if opt=={} :
         fich.insert(END,"\t\t"+raccourci+'.pack()\n')
      else :
         listeopt= ",".join([ "%s=\"%s\"" %(k,v) for (k,v) in opt.items()  ])
         fich.insert(END,"\t\t"+raccourci+'.pack('+listeopt+')\n')
      fich.insert(END,"\t\t#</"+raccourci+">\n")
   
   def gagnecaracteresuivant(curseur):
      #exemple [14.2] devient [14.3]
      point= curseur.index(".")
      curseur=str(curseur[0:point])+"."+ str( int(curseur[point+1:])+1)
      return curseur
   
   def gagnelignesuivante(curseur):
      #exemple [14.2] devient [15.0]
      curseur=str(int(curseur[0:curseur.index(".")])+1)+".0" 
      return curseur
            
   def enregistrecode():
      nomfich= 'fenetredemo.py'
      enregistrer=True
      #si fichier existe avertir
      if os.path.exists(nomfich):
         if (messagebox.askquestion('Attention','ce fichier existe déjà, écraser ?')=='no'):
            enregistrer=False
       
      if (enregistrer):
         fichier=open('fenetredemo.py','w')
         #reprend le code affiché
         fichier.write(fich.get("1.0",END))
         #compléter la fin du fichier
         fichier.write("\tdef run(self):\n")
         fichier.write("\t\tself.master.mainloop()\n\n")
         #fonction de lancement
         fichier.write("if __name__=='__main__' : \n")
         fichier.write("\timport tkinter as tk\n")
         fichier.write("\tapp=Newui(root)\n")
         fichier.write("\tapp.run()\n")   

         fichier.close
         print ('fenetredemo a été généré dans le répertoire courant')

   
def CentrerFenetre(fenetre, width, height):
    """ Fonction, pour centrez une fenêtre """
    screenX = (fenetre.winfo_screenwidth() - width) //2
    screenY = (fenetre.winfo_screenheight() - height) //2
 
    fenetre.geometry("%ix%i+%i+%i"%(width, height,
                                    screenX, screenY))

   
def Suppr():
   select=ltree.focus()
   #ne pas supprimer top
   if select=='top':
      messagebox.showinfo('Refusé','Suppression refusée')
   elif messagebox.askokcancel('Supprimer','Confirmer la suppression ?'):
      #message différent s'il a des enfants ?
         
      #supprimer les widgets réels
      dictwidg[select].destroy()
      #supprimer du dico
      del(dictwidg[select])
      #supprimer du treeview
      ltree.delete(select)
      #supprimer le code data entre < > et </ >
      deb=fich.search("#<"+select,0.0 )
      fin=fich.search("#</"+select+">",0.0)
      #gagner la ligne suivante
      fin=CodePython.gagnelignesuivante(fin)
      fich.delete(deb,fin)

def Modif():
	#ouvrir le module de choix
    select=ltree.focus()
    if select!="":
        #select contient id unique
        #retrouver le code data entre < > et </ >
        deb=fich.search("#<"+select,0.0 )
        fin=fich.search("#</"+select+">",0.0)
        listeoptions={}
        
        #Récuperer le type de widget à modifier
        debwidg = fich.search(":",deb)
        finwidg = fich.search(">",deb)
        widg=fich.get(CodePython.gagnecaracteresuivant(debwidg),finwidg)
        #print("widget à modifier "+widg)
        
        #chercher les virgules devant option="valeur"
        #for i = deb to fin:
        sep1= fich.search(",",deb)
        sep1=CodePython.gagnecaracteresuivant(sep1)
        sep2=fich.search(")",deb)
        listeoptions=(fich.get(sep1,sep2))
        listeoptions=(listeoptions.split(","))
        #print(options avant modifs " + str(listeoptions))
        cancel=StringVar()
        cancel.set("False")
        opt=mod_options.Proprietes(root,widg,listeoptions,cancel=cancel)
        if (cancel != "True"):
            #retour au destroy de la toplevel
            #print ("options après modifs" +str(opt.args))
            
            #replacer dans la ligne de code
            fich.delete(sep1,sep2)
            newline=""
            for arg in (opt.args):
               if (newline!=""): newline+=","
               newline=newline+arg
               #changer le widget 
               expr="dictwidg[select].configure("+arg+")"
               exec(expr)
               #dictwidg[select].configure(arg) 
            fich.insert(sep1,newline)
            
        #retrouver les pack par le tree view
        #optionspack=ltree.item(select,'values')[1]
        #print(optionspack)
        

#---------Fenêtre principale
root=Tk()

root.title('Générateur de fenêtre Tkinter')
CentrerFenetre(root,LARGEUR,HAUTEUR)

#Frame contenants tous les widgets
frmOutils=Frame(root,bg="#d0d0d0",relief=GROOVE)   
frmOutils.pack(side="left",anchor="n")

# Barre d'outils1: conteneurs
tool_cont=LabelFrame(frmOutils,bg="#d0d0d0",text="conteneurs",relief=GROOVE)   
tool_cont.pack(side="top",anchor="w")
     
class BtnOutil(Button):
   def __init__(self,parent,nom, pack="left",img=None):
      #méthode directe ne récupere pas les autres méthodes du bouton Tk
      #btn=Button(parent,text=nom,underline=0) 
      
      super().__init__(parent,text=nom,underline=0,command=eval("Widget.cde"+nom))
      self=self
      if img!=None: self.configure(image=img)
      #eviter events interfere avec toplevel
      #self.bind("<Button-1>",eval("cde"+nom))
      if pack=="left" :
		  #barre d'outil tool_cont=container
         self.pack(side="left",fill=X)
      else:
         self.pack(side="top",anchor="w",fill=X)
            
ListeBoutons=["frame","labelframe","panedwindow","notebook"]
imgcont={}
for i in range(len(ListeBoutons)):
   nom = ListeBoutons[i]
   libelle="btn"+nom
   #images: pas de majuscules, png ou gif uniquement
   imgcont[i]= PhotoImage(file='symbols/'+nom+'.png')
   libelle=BtnOutil(tool_cont,nom,pack="left",img=imgcont[i])

# Barre d'outils2: widgets tk
tool_tk=LabelFrame(frmOutils,bg="#d0d0d0",text="widgets tk",relief=GROOVE)
tool_tk.pack(side=LEFT, anchor="n", fill=NONE)


ListeBoutons=["label","entry","button","radiobutton","checkbutton","canvas","scale" ,\
              "scrollbar","listbox","message","spinbox","text"]
img={}
ListeLibelle=["btn"+x for x in ListeBoutons]  # sert à rien noms btn... perdus à la création des boutons
for i in range(len(ListeBoutons)):
   nom = ListeBoutons[i]
   img[i]= PhotoImage(file='symbols/'+nom+'.png')
   ListeLibelle[i]=BtnOutil(tool_tk,nom, pack="top",img=img[i])

# Barre d'outils3: widgets ttk
tool_ttk=LabelFrame(frmOutils,bg="#d0d0d0",text="widgets ttk",relief=GROOVE)
tool_ttk.pack(side="top", anchor="w",fill=NONE)

ListeBoutons=["treeview","combobox","progressbar"]
ListeLibelle=["btn"+x for x in ListeBoutons]

imgttk={}
for i in range(len(ListeBoutons)):
   nom = ListeBoutons[i]
   imgttk[i]= PhotoImage(file='symbols/'+nom+'.png')
   ListeLibelle[i]=BtnOutil(tool_ttk,nom,pack="top",img=imgttk[i])

# Barre d'outils4: widgets menus
tool_menu=LabelFrame(frmOutils,bg="#d0d0d0",text="menus",relief=GROOVE)
tool_menu.pack(side="top", anchor="w",fill=NONE)

ListeBoutons=["menubutton"]
ListeLibelle=["btn"+x for x in ListeBoutons]

imgmenu={}
for i in range(len(ListeBoutons)):
   nom = ListeBoutons[i]
   imgmenu[i]= PhotoImage(file='symbols/'+nom+'.png')
   ListeLibelle[i]=BtnOutil(tool_menu,nom,pack="top",img=imgmenu[i])

# frame contenant le treeview
frtree=LabelFrame(root,bg="#d0d0d0",text="treeview",relief=GROOVE)
frtree.pack(side=TOP, anchor="n",fill=NONE)

# widget tree
ltree=ttk.Treeview(frtree,selectmode='browse') #une seule selection à la fois
ltree['columns']=('ind','pack')
ltree.heading('ind',text='ind')
ltree.column('ind',width="60" )
ltree.heading('pack',text='pack')
ltree.column('pack',width="200" )
ltree.pack(side=LEFT,anchor="n")
#intercepter le click :pour déselectionner
ltree.bind("<Button-1>",Treeview.clicktree)

# fleches de changement de position
pw=PanedWindow(frtree,orient=VERTICAL)
btnSuppr=Button(pw,text="Suppr",command=Suppr)
btnSuppr.pack(side=TOP,fill=X)
btnModif=Button(pw,text="Modif",command=Modif)
btnModif.pack(side=TOP,fill=X)

btnH=Button(pw,text="Haut",command=Treeview.haut)
##btnB=Button(pw,text="Bas", command=Treeview.bas)
btnH.pack(side=TOP,fill=X)
##btnB.pack(side=TOP,fill=X)
pw.pack(side=LEFT)

# frame contenant le code python et le bouton enregistrer le code
frBottom=LabelFrame(root,bg="#d0d0d0",text="Code python",relief=GROOVE)
frBottom.pack(side=TOP, anchor="s",fill=NONE)

# Bouton pour générer le code
btn=Button(frBottom,text="Copier le code python dans un fichier",underline=0,command=CodePython.enregistrecode)
btn.pack(side=BOTTOM, anchor="s")


# widget text pour afficher le code produit
fich=Text(frBottom)
fich.configure(tabs="30")#bizarre 30 pour 3
fich.pack(side=BOTTOM)
#scrollbar
sc1=Scrollbar(frBottom,orient="vertical")
sc1.pack(side="left")
#fich.configure(yscrollcommand=sc1.set)

CodePython.initcode()

ltree.insert('', 0,'top',text="Fenetre principale",value="top")
ltree.item('top', open=TRUE) #noeud déployé

#rendre optionnel : fenetre unique ou top ?
#fich.insert(END,"\n#TopLevel \n")
#fich.insert(END,'top=Toplevel(root)')
 
top1=Toplevel(root)
top1.configure(borderwidth=5)
dictwidg={}
dictwidg['top']=top1
top1.resizable(FALSE,FALSE)
top1.transient(root)  #pas de bouton reduire la fenetre marche pas
top1.grab_status() 
   
root.mainloop()
