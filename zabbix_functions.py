# coding: utf-8
# Módulo funções customizadas - API Zabbix

#############################################################33

from datetime import datetime, date, time


# function que recebe group_id(_group_id) como parametro e retorna a lista de HOSTs do grupo (hostid, name)
def zbHostList(pGroupID, pZapi):
        vHostFields=["hostid", "name", "proxy_hostid"] # Vetor com a lista de campos do HOST que serão retornados
	vHostList=pZapi.host.get({"groupids": pGroupID, "output": vHostFields}) # Gera a lista dos Hosts do Grupo e retorna os Campos 
	return vHostList



# function que recebe proxy_hostid como parametro e retorna o proxy_name
def zbProxyName(pProxyHostID, pZapi):
	if int(float(pProxyHostID)) > 0:
		vProxyName=pZapi.proxy.get({"proxyids": pProxyHostID, "output": ["host"]})[0]['host']
	else:
		vProxyName="Proxy não encontrado"
	return vProxyName



# function que recebe hostid como parametro e retorna a lista dos IPs associados ao hostid
def zbInterfaceList(pHostID, pZapi):
	vInterfaceList=pZapi.hostinterface.get({"hostids": pHostID, "output": ["ip","type"]})
	vIPList=[]
	for vInterface in vInterfaceList:
		vIPList.append(str(vInterface['ip']))
	return vIPList



# function que recebe hostid como parametro e retorna a lista de Templates associados ao HOST
def zbTemplateList(pHostID, pZapi):
	vTemplateList=[]	
	vTemplateListFull=pZapi.template.get({"output": ["name"], "hostids": pHostID})
	for vTemplate in vTemplateListFull:
		vTemplateList.append(str(vTemplate['name']))
	return vTemplateList




# function que recebe hostid como parametro e retorna a lista de GRUPOS associados ao HOST
def zbGroupList(pHostID, pZapi):
	vGroupList=[]
	vGroupListFull=pZapi.hostgroup.get({"output": "extend", "hostids": pHostID})
	for vGroup in vGroupListFull:
		vGroupList.append(str(vGroup['name'].encode("UTF-8"))) # adicionado .encode("UTF-8") pois há grupos com caracteres especiais - verificar depois se dá pra remover
	return vGroupList



# function que recebe hostid como parametro e retorna alguns itens, o valor da última leitura e data e hora da ultima leitura
def zbItemList(pHostID, pKeysList, pZapi):
	# Lista campos de itens que serão retornados
	vItemFields=["lastvalue", "hostid", "name", "key_", "lastclock"]
	# vItemList : Lista onde serão carregados os dados que serão retornados
	vItemList=[]
	vItemListFull=pZapi.item.get({"output": vItemFields, "hostids": pHostID, "filter": {"key_": pKeysList}})
	for vItem in vItemListFull:
		vItemList.append([str(vItem['key_']),str(vItem['lastvalue']),str(datetime.fromtimestamp(float(vItem['lastclock'])))])

	return vItemList

###############################################################
