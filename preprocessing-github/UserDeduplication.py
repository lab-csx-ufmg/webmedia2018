import csv

def extractFakeUsers(fakeUsersList):
	with open('data/users.csv', 'r') as r:
		data = csv.reader(r, delimiter=',')
		
		for row in data:
			user_id = int(row[0])
			login = row[1]
			name = row[2]
			company = row[3]
			location = row[4]
			email = row[5]
			created_at = row[6][:10]
			usr_type = row[7]
			fake = int(row[8])
			deleted = int(row[9])

			# limpa campos com valor \\N
			if name == '\\N':
				name = ''
			if company == '\\N':
				company = ''
			if location == '\\N':
				location = ''
			if email == '\\N':
				email = ''
	
			# inclui apenas usuários fake na lista
			if fake:
				user = [user_id, login, name, company, location, email, created_at, usr_type, fake, deleted]
				fakeUsersList.append(user)
	r.close()

#########################################################################################################################################

fakeUsersList = []
fakeUsersDict = {} # chave = e-mail; conteúdo = user_id, ocorrencias

# cria primeira lista de usuários fake
extractFakeUsers(fakeUsersList)

print('Quantidade de usuários fake:', len(fakeUsersList))

countDeduplication = 0

# agrupamento de usuários por e-mail
for fakeUser in fakeUsersList:
	# para cada usuário, geraremos um dict por e-mail e armazenaremos apenas o primeiro user_id encontrado (deduplicado)

	if fakeUser[5] in fakeUsersDict:
		fakeUsersDict[fakeUser[5]][1] = fakeUsersDict[fakeUser[5]][1] + 1

		if fakeUser[5] != '':
			countDeduplication += 1
	else:
		fakeUsersDict[fakeUser[5]] = [fakeUser[0], 1] # user_id, ocorrencias

print('Quantidade usuários deduplicados por e-mail:', countDeduplication)
print('Quantidade usuários e-mail vazio:', fakeUsersDict[''][1])