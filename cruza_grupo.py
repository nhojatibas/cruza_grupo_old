#!/usr/bin/python
# -*- coding: utf-8 -*-

# cliza = cliente zabbix (brega mas tá bom por hora)

# Carregando bibliotecas

# Glade (carregando bibliotecas do Glade)
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf

# Zabbix (carregando biblioteca da API do Zabbix e biblioteca de funcoes criadas)
from zabbix_api import ZabbixAPI
from zabbix_functions import *

# Bibliotecas de apoio
from datetime import datetime, date, time
import time as t


# Constantes
vServer = "http://monitor.ciasc.gov.br"
vUserName = "nholiveira@ciasc.sc.gov.br"
vPassword = ""

_vermelho = GdkPixbuf.Pixbuf.new_from_file("vermelho.png")
_verde = GdkPixbuf.Pixbuf.new_from_file("verde.png")

####################################onButtonSearch_clicked
# Abrindo a sessão com o servidor zabbix
vZapi=ZabbixAPI(server=vServer, log_level=0)
vZapi.login(vUserName, vPassword)

# Buscando a lista de grupos no servidor Zabbix
vGroupListIni=vZapi.hostgroup.get({"output": ["name", "groupid"]})

class _cliza:
    def __init__(self):

        # Carrega do Glade os elementos da janela principal (cruza_grupo.glade), em variaveis self.main_window
	#print self

        self.main_window=Gtk.Builder()
        self.main_window.add_from_file("cruza_grupo.glade")
	self.main_window.connect_signals(self) 

        self.main_window.janela_principal=self.main_window.get_object("_janela_principal")

        self.main_window.treeview_lista_origem=self.main_window.get_object("_treeview_lista_origem")
        self.main_window.liststore_lista_origem=self.main_window.get_object("_liststore_lista_origem")

        self.main_window.button_refresh=self.main_window.get_object("_button_refresh")
        self.main_window.entry_filtragrupo=self.main_window.get_object("_entry_filtragrupo")

        self.main_window.button_add=self.main_window.get_object("_button_add")
        self.main_window.button_remove=self.main_window.get_object("_button_remove")

        self.main_window.button_search=self.main_window.get_object("_button_search")

        self.main_window.treeview_lista_destino=self.main_window.get_object("_treeview_lista_destino")
	self.main_window.liststore_lista_destino=self.main_window.get_object("_liststore_lista_destino")

# Cargas iniciais
        for grupo in vGroupListIni:
#	     print grupo
            self.main_window.liststore_lista_origem.append([grupo['name'],int(grupo['groupid'])])

# Declarando o filtro a ser aplicado na "self.main_window.liststore_lista_origem"
	self.treemodelfilter_lista_origem=self.main_window.liststore_lista_origem.filter_new()
        self.treemodelfilter_lista_origem.set_visible_func(self.treemodelfilter_lista_origem_func)

# Colocando o loop do Gtk para rodar
        self.main_window.janela_principal.show_all()

    def run(self):
	print "Ao rodar"
	print self
	print dir(self)
        Gtk.main()


# Função de filtro a ser aplicado em "self.glade.treeview_lista_origem"
#    def treemodelfilter_lista_origem_func(self, model, iter, data):
    def treemodelfilter_lista_origem_func(self, model, iter, data):
        #print "self", dir(self)
        if len(self.current_filter_lista_origem) < 1:
            return True
        else:
            return self.current_filter_lista_origem in model[iter][0]
	    #print iter

        
# Ligando os SINAIS do Glade a funções da classe (no Glade chamadas de Handler)

# Sinais da Janela Principal

# Fechando a aplicacao
    def onDeleteWindow(self, *args):
 	Gtk.main_quit(*args)

# Pressionando o botão "atualiza"
    def onButtonRefreshClicked(self, *args):
        self.main_window.treeview_lista_origem.set_model(self.treemodelfilter_lista_origem)    # define o moldel do filtro como model a ser exibido pela treeview
        self.current_filter_lista_origem=self.main_window.entry_filtragrupo.get_text()         # pega o parâmetro de filtragem do campo - self.glade.entry_filtragrupo.get_text() 
        self.treemodelfilter_lista_origem.refilter()                                           # aplica o filtro

# Pressionando o botão "+" (add)
    def onButtonAdd_clicked(self, *args):
        _treeview_origem_full = self.main_window.treeview_lista_origem.get_selection()
        _treeview_origem_selected = _treeview_origem_full.get_selected()
	print "_treeview_origem_full:", _treeview_origem_full
	print "_treeview_origem_selected:", _treeview_origem_selected
	print "_treeview_origem_selected[1]:", _treeview_origem_selected[1]
        if _treeview_origem_selected[1] != None:
            (_modelo, _iter) = _treeview_origem_selected
            #print "selected-->", _modelo[_iter], " : ",  _modelo[_iter][0], " : ", _iter.stamp, " : ", type(_iter)
            #print self.main_window.button_search.get_events()
            if _modelo[_iter][0] not in [_linha[0] for _linha in self.main_window.liststore_lista_destino]: # Verifica se existe na lista para adicionar (só se nao existe)
		print "modelo[iter]:",[_modelo[_iter][0]],[_modelo[_iter][1]]
                self.main_window.liststore_lista_destino.append([_modelo[_iter][0],_modelo[_iter][1]])
#	print self.main_window.button_search.get_label()
#       print self.main_window.button_search.activate()

# Pressionando o botão "-" (remove)
    def onButtonRemove_clicked(self, *args):
        _treeview_destino_full = self.main_window.treeview_lista_destino.get_selection()
        _treeview_destino_selected = _treeview_destino_full.get_selected()
        if _treeview_destino_selected[1] != None:
            (_modelo, _iter) = _treeview_destino_selected
            self.main_window.liststore_lista_destino.remove(_iter)

# Pressionando o botao "Procurar"
    def onButtonSearch_clicked(self, *args):
#    def on(self, *args):
        print "Procurou"
	print dir(self)
	print args
	print "Lista Destino: ",self.main_window.liststore_lista_destino
	_sub_window=_cliza_sub(self.main_window.liststore_lista_destino)
	_sub_window.run_sub()


# Sinais da Sub Janela
#    def onsubDeleteWindow(self, *args):
#        Gtk.main_quits(*args)

class _cliza_sub:
    def __init__(self, lista_grupos):

        # Carrega do Glade os elementos da sub janela (cruza_grupo_sub.glade), em variaveis self.glade.sub
        self.sub_window=Gtk.Builder()
        self.sub_window.add_from_file("cruza_grupo_sub.glade")
        self.sub_window.connect_signals(self)

        self.sub_window.janela_principal=self.sub_window.get_object("_sub_window")
	self.sub_window.info_label=self.sub_window.get_object("_sub_info_label")
	self.sub_window.treeviewgrupo=self.sub_window.get_object("_sub_selected_groups_treeview")
	self.sub_window.liststoregrupo=self.sub_window.get_object("_sub_selected_groups_liststore")
	self.sub_window.liststorehost=self.sub_window.get_object("_sub_selected_hosts_liststore")

	self.sub_window.lista = lista_grupos
	

# Colocando o loop do Gtk para rodar
        self.sub_window.janela_principal.show_all()

    def run_sub(self):
#	print dir(self)
#	print "Lida da sub: ",len(self.sub_window.lista), self.sub_window.lista
#	print "Antes :", len(self.sub_window.liststoregrupo)

# Aqui recebemos a liststore com os grupos selecionados e a usamos como base para:
#
#  1 - Gerar uma LISTA <_lista_grupo> com os <group_id> de cada grupo selecionado baseando-se na LISTSTORE<self.sub_window.lista> do GTK, passado como parâmetro
#  2 - Gerar um DICT <_dict_group_hosts> (chave = <group_id>, data = lista de <host_id> dos Hosts que pertencem ao grupo)
#  3 - Identificar os hosts de intersecção nos grupos passados como parâmetro na LISTA <_intersec_hosts> a partir de <_lista_grupo>
#  4 - Gerar uma LISTA de LISTA<_lista_grupo_completa> para carregar na caixa de GRUPOS da sub_tela. Essa lista terá listas com : <group_id>, <group_name>, <qtd_hosts_group>
#  5 - Gerar uma LISTA de LISTA <_lista_host_intersec_completa> para carregar na caixa de HOSTS da sub_tela. Essa lista terá listas com : <host_id>, <host_name>, <ip>
#

# Declarando

	_lista_grupo=[]
	_dict_group_hosts={}
	_intersec_hosts=[]
	_lista_grupo_completa=[]
	_lista_host_itersec_completa=[]

	_hosts_zabbix=[] # lista que recebe a o resultado da pesquisa de hosts no grupo (API ZABBIX) - resultado é uma lista de dicionários entregue pela API do Zabbix
	_hosts=[]        # lista que recebe a lista de hostid


# Carregando a _lista_grupo com os group_id passados como parâmetro em self.sub_window.lista (gerando 1)

	for _iter_liststore in self.sub_window.lista:
		_lista_grupo.append(_iter_liststore[1]) # adiciona group_id a _lista_grupo

	_old = [] # Lista de apoio - não é base do processo

# Percorrendo a LISTA <_lista_grupo>, usando-a de base para carga do DICIONARIO _dict_group_hosts e identificando os hosts de intersecção em _intersec_hosts (gerando 2 e 3)

	for _group_id in _lista_grupo: # percorrendo _lista_grupo
		_hosts_zabbix=vZapi.host.get({"groupids": _group_id, "output": "hostid"}) # faz a pesquisa no API do Zabbix e retorna uma lista de dicionario com os "host_id" que pertencem ao grupo
		print _hosts_zabbix
		for _host in _hosts_zabbix: # percorrendo a resposta da API Zabbix para separar os host_id e carrega-la na LISTA _hosts
			_hosts.append(_host['hostid']) # adiciona o "host_id" a LISTA _hosts para posterior carga no DICIONARIO _dict_host
		_dict_group_hosts[str(_group_id)]=_hosts # carrega o DICIONARIO "_dict_host" usando "str(_group_id)" como chave e a LISTA _hosts como DADO
		_hosts=[] #descarrega a LISTA _hosts para ser gerada novamente com dados de outro grupo se for o caso
		if len(_old)>0:
			if len(_intersec_hosts)<1:
				_intersec_hosts=list(set(_old).intersection(set(_dict_group_hosts[str(_group_id)])))
			else:
				_intersec_hosts=list(set(_intersec_hosts).intersection(set(_old)).intersection(set(_dict_group_hosts[str(_group_id)])))
		_old = _dict_group_hosts[str(_group_id)]

# Percorrendo a LISTA _lista_grupo, pesquisa o DICIONARIO _dict_group_hosts e API ZABBIX para determinar _group_name e _qtd_hosts_group

	for _group_id in _lista_grupo:
		_group_name=vZapi.hostgroup.get({"output": ["name"], "groupids": [_group_id]})
		print _group_name
		_qtd_hosts_group=len(_dict_group_hosts[str(_group_id)])
		print _group_id, _group_name[0]['name'], _qtd_hosts_group

		# Carregando os dados na TreeView de Grupo
		self.sub_window.liststoregrupo.append([_group_name[0]['name'], _qtd_hosts_group])

# Percorrendo a LISTA _intersec_hosts, pesquisando na API ZABBIX o hostname e IPs (lista)
	
	if len(_intersec_hosts) > 0:
		print "--------------------------------------------------"
		for _host_id in _intersec_hosts:
			_host_name=vZapi.host.get({"output": ["name"], "hostids": [_host_id]}) 
			_host_ip=vZapi.hostinterface.get({"hostids": _host_id, "output": ["ip"]})
			_templates=vZapi.template.get({"output": ["name"], "hostids": [_host_id]})
#			_host_templates=vZapi.template.get({"output": "extend", "hostids": [_host_id]})
			_host_templates=""
			for _template in _templates:
				if len(_host_templates) < 1:
					_host_templates=_template["name"]
				else:
					_host_templates=_host_templates+" | "+_template["name"]

			# Captura valores dos itens que devem ser exibidos da treeviewe (no momendo 'agent.version' e 'icmpping[{IPADDRESS},,,,]')
			_host_itens=vZapi.item.get({"output": ['lastvalue', 'name', 'key_'], "hostids": [_host_id], "filter": {"key_": ['agent.version', 'icmpping[{IPADDRESS},,,,]']}})
#			_host_itens=vZapi.item.get({"output": ['lastvalue', 'name', 'key_'], "hostids": [_host_id]})

#			print "_host_itens..:", _host_name[0]['name'], ":", _host_itens

#			print _host_id, _host_name[0]['name'], _host_ip[0]['ip'], _host_templates
#			print "template", _host_templates
			
			_host_agentversion=_host_itens[0]['lastvalue']  # se mudar os itens, isso aqui deve ser mudado tbém - ATENÇÃO
			_host_pingvalue=_host_itens[1]['lastvalue']

#			print "Versao agente:",_host_agentversion
#			print "Status PING  :",_host_pingvalue
			print _host_id+":"+_host_name[0]['name']+":"+_host_ip[0]['ip']+":"+_host_templates+":"+_host_agentversion+":"+_host_pingvalue

			

			# carrega o gráfico de status de ping na variavel que será adicionada na treeview (GdkPixbuf)
			if _host_pingvalue == '1':
				_host_pingstatus=_verde				
			else:
				_host_pingstatus=_vermelho


			# Carregando os dados na Treeview de Hosts
			self.sub_window.liststorehost.append([_host_name[0]['name'], _host_ip[0]['ip'], _host_templates, _host_agentversion, _host_pingstatus])
		print "--------------------------------------------------"


		# Carregando o valor adequado no LABEL
		_TEXTO = str(len(_intersec_hosts))+" Hosts nos Grupos selecionados"
		print _TEXTO
		self.sub_window.info_label.set_text(_TEXTO)
			

			
	else:
			self.sub_window.info_label.set_text("Não há Hosts que atendam o critério")



	print "---------------------------------------------------"
	print " respostas"
	print "---------------------------------------------------"
	print "1 _lista_grupo"
	print _lista_grupo
	print "2 _dict_host"
	print _dict_group_hosts 
	print "3 _intersec_hosts"
	print _intersec_hosts 

	

        Gtk.main()

# Sinais da Janela Sub

# Fechando a aplicacao
    def onsubDeleteWindow(self, *args):
        Gtk.main_quit(*args)


_main_window=_cliza()
_main_window.run()
