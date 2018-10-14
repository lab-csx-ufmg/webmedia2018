from datetime import datetime
import sys, csv, operator
import collections
import sys

# ordenação da lista por repositório
def commit_order(c):
	return (c[0])

def firstLastCommitUser(firstLastDict):
	with open('data/commits_with_dates.csv', 'r') as r:
		data = csv.reader(r, delimiter=',')
		next(data) # cabeçalho: repository_id,author_id,commit_id,commit_date
		
		for row in data:
			rep_id = int(row[0])
			dev_id = int(row[1])
			commit_id = row[2]
			commit_date = row[3]
			
			# não realiza alteração se data não for válida
			if commit_date[:10] != '0000-00-00':
				
				if (rep_id, dev_id) in firstLastDict:
					# avalia data inicial de contribuição
					if firstLastDict[rep_id, dev_id][1] > commit_date:
						#print("Change developer", dev_id, "on repository", rep_id, "begin date", firstLastDict[rep_id, dev_id][1], "to", commit_date)
						firstLastDict[rep_id, dev_id][0] = commit_id
						firstLastDict[rep_id, dev_id][1] = commit_date
					
					# avalia data final de contribuição
					if firstLastDict[rep_id, dev_id][3] < commit_date:
						#print("Change developer", dev_id, "on repository", rep_id, "end date", firstLastDict[rep_id, dev_id][3], "to", commit_date)
						firstLastDict[rep_id, dev_id][2] = commit_id
						firstLastDict[rep_id, dev_id][3] = commit_date
				else:
					#print("Including developer", dev_id, "on repository", rep_id)
					# dict: key = (rep_id, dev_id)
					#       value = lista [first_commit_id, first_commit_date, last_commit_id, last_commit_date]
					firstLastDict[rep_id, dev_id] = [commit_id, commit_date, commit_id, commit_date, 0]
	r.close()

def permuteWithoutDates(repository_id, list_users):
	# para cada conjunto de desenvolvedores, calcula valores dois a dois
	with open('data/developers_social_network_without_dates.csv', 'a') as a:
		permute_file = csv.writer(a, delimiter=',')
		contributions = 0

		for i in list_users:
			for j in list_users:
				if i < j:
					permute_file.writerow([repository_id, i, j])
					contributions += 1

		print('Quantidade de contribuições:', contributions)

	a.close()

def permuteWithDates(dict_infos, repository_id, list_users):
	# para cada conjunto de desenvolvedores, calcula valores dois a dois
	with open('data/developers_social_network_with_dates.csv', 'a') as a:
		permute_file = csv.writer(a, delimiter=',')
		contributions = 0

		for i in list_users:
			for j in list_users:
				if i < j:
					# calcula contribuições com datas

					# define data inicial de contribuição
					join_date_dev_i = datetime.strptime(dict_infos[repository_id, i][1], '%Y-%m-%d %H:%M:%S')
					join_date_dev_j = datetime.strptime(dict_infos[repository_id, j][1], '%Y-%m-%d %H:%M:%S')
					# data inicial é a maior entre as datas de entrada de cada dev
					begin_date = max(join_date_dev_i, join_date_dev_j)

					# define data inicial de contribuição
					out_date_dev_i = datetime.strptime(dict_infos[repository_id, i][3], '%Y-%m-%d %H:%M:%S')
					out_date_dev_j = datetime.strptime(dict_infos[repository_id, j][3], '%Y-%m-%d %H:%M:%S')
					# data final é a menor entre as datas de saída da cada dev
					end_date = min(out_date_dev_i, out_date_dev_j)

					# calcula dias de contribuição
					contribution_days = (end_date - begin_date).days

					# se o contribution_days for negativo, não houve colaboração ao mesmo tempo (se igual a zero, houve contribuição no mesmo dia)
					# grava no arquivo apenas colaborações realmente existentes
					if contribution_days >= 0: 
						permute_file.writerow([repository_id, i, j, str(begin_date), str(end_date), contribution_days])
						contributions += 1

		print('Quantidade de contribuições:', contributions)

	a.close()

###########################################################################################################################################################

firstLastCommit = {}

# percorre arquivo com os commits para definir a data inicial e final de colaboração de um desenvolvedor num repositório
# dict: key = (rep_id, dev_id)
#       value = lista [first_commit_id, first_commit_date, last_commit_id, last_commit_date]
firstLastCommitUser(firstLastCommit)

# cria lista para os dados a fim de ordenar por repositório e tratar os desenvolvedores de cada um deles
userRepository = list(firstLastCommit.keys())
userRepository.sort()

# cria arquivo para rede de colaboração sem tratamento por data
with open('data/developers_social_network_without_dates.csv', 'w') as w:
		permute_file = csv.writer(w, delimiter=',')
		# cabeçalho
		permute_file.writerow(["repository_id", "developer_id_1", "developer_id_2"])
w.close()

print('\n=== MODELAGEM DA REDE SEM TRATAMENTO DE DATAS ===')

# percorre lista de projetos para realizar a permutacao
permuteList = []
lastRepository = userRepository[0][0] # primeiro repositório da lista

for row in userRepository:
	rep_id = row[0]

	if rep_id == lastRepository:
		permuteList.append(row[1])
	else:
		# permuta lista do lastRepository
		print('\nPermutação de desenvolvedores - Repositório', lastRepository)
		print('Quantidade de desenvolvedores:', len(permuteList))
		permuteWithoutDates(lastRepository, permuteList)

		# limpa lista para próximo projeto
		permuteList = []
		permuteList.append(row[1])

	# atualiza lastRepository
	lastRepository = rep_id

# permuta lista do último projeto
print('\nPermutação de desenvolvedores - Repositório', lastRepository)
print('Quantidade de desenvolvedores:', len(permuteList))
permuteWithoutDates(lastRepository, permuteList)

# cria arquivo para rede de colaboração com tratamento por data
with open('data/developers_social_network_with_dates.csv', 'w') as w:
		permute_file = csv.writer(w, delimiter=',')
		# cabeçalho
		permute_file.writerow(["repository_id", "developer_id_1", "developer_id_2", "begin_contribution_date", "end_contribution_date", "contribution_days"])
w.close()

print('\n=== MODELAGEM DA REDE COM TRATAMENTO DE DATAS ===')

# percorre lista de projetos para realizar a permutacao
permuteList = []
lastRepository = userRepository[0][0] # primeiro repositório da lista

for row in userRepository:
	rep_id = row[0]

	if rep_id == lastRepository:
		permuteList.append(row[1])
	else:
		# permuta lista do lastRepository
		print('\nPermutação de desenvolvedores - Repositório', lastRepository)
		print('Quantidade de desenvolvedores:', len(permuteList))
		permuteWithDates(firstLastCommit, lastRepository, permuteList)

		# limpa lista para próximo projeto
		permuteList = []
		permuteList.append(row[1])

	# atualiza lastRepository
	lastRepository = rep_id

# permuta lista do último projeto
print('\nPermutação de desenvolvedores - Repositório', lastRepository)
print('Quantidade de desenvolvedores:', len(permuteList))
permuteWithDates(firstLastCommit, lastRepository, permuteList)

