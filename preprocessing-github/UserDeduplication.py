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
				first_last_name = ''
			else:
				splitName = name.split(' ')
				if len(splitName) > 1:
					first_last_name = splitName[0] + ' ' + splitName[len(splitName)-1]
				else:
					first_last_name = name
			
			if company == '\\N':
				company = ''
			
			if location == '\\N':
				location = ''
			
			if email == '\\N':
				email = ''
	
			# inclui apenas usuários fake na lista
			if fake:
				user = [user_id, login, name, first_last_name, company, location, email, created_at, usr_type, fake, deleted]
				fakeUsersList.append(user)
	r.close()

def deduplicateUsersByEmail(fakeUsersList, fakeUsersDict):
	# agrupamento de usuários por e-mail
	# retorna True se houve qualquer deduplicação e False, caso contrário
	deduplication = False

	for fakeUser in fakeUsersList:
		# para cada usuário, geraremos um dict por e-mail e armazenaremos apenas o primeiro user_id encontrado (deduplicado)

		if fakeUser[6] in fakeUsersDict:
			deduplication = True
			fakeUsersDict[fakeUser[6]][1] = fakeUsersDict[fakeUser[6]][1] + 1
		else:
			fakeUsersDict[fakeUser[6]] = [fakeUser[0], 1] # user_id, ocorrencias

	return deduplication

def deduplicateUsersByUsername(fakeUsersList, fakeUsersDict):
	# agrupamento de usuários por username/login
	# retorna True se houve qualquer deduplicação e False, caso contrário
	deduplication = False

	for fakeUser in fakeUsersList:
		# para cada usuário, geraremos um dict por username e armazenaremos apenas o primeiro user_id encontrado (deduplicado)

		if fakeUser[1] in fakeUsersDict:
			deduplication = True
			fakeUsersDict[fakeUser[1]][1] = fakeUsersDict[fakeUser[1]][1] + 1
		else:
			fakeUsersDict[fakeUser[1]] = [fakeUser[0], 1] # user_id, ocorrencias

	return deduplication

def deduplicateUsersByFirstLastName(fakeUsersList, fakeUsersDict):
	# agrupamento de usuários por nome de usuário (primeiro e último)
	# retorna True se houve qualquer deduplicação e False, caso contrário
	deduplication = False

	for fakeUser in fakeUsersList:
		# para cada usuário, geraremos um dict por primeiro e último nome e armazenaremos apenas o primeiro user_id encontrado (deduplicado)

		if fakeUser[3] in fakeUsersDict:
			deduplication = True
			fakeUsersDict[fakeUser[3]][1] = fakeUsersDict[fakeUser[3]][1] + 1
		else:
			fakeUsersDict[fakeUser[3]] = [fakeUser[0], 1] # user_id, ocorrencias

	return deduplication


#########################################################################################################################################

fakeUsersList = []
fakeUsersDictEmail = {} # chave = e-mail; conteúdo = user_id, ocorrencias
fakeUsersDictUsername = {} # chave = username; conteúdo = user_id, ocorrencias
fakeUsersDictFirstLastName= {} # chave = first_last_name; conteúdo = user_id, ocorrencias

# cria primeira lista de usuários fake
extractFakeUsers(fakeUsersList)

print('Quantidade de usuários fake:', len(fakeUsersList))


print('\n=== Deduplicação por e-mail ===')
# cria dicionário de usuários duplicados por e-mail
ret = deduplicateUsersByEmail(fakeUsersList, fakeUsersDictEmail)

if ret:
	countDeduplication = 0
	sumOccurrences = 0

	for user in fakeUsersDictEmail:
		if fakeUsersDictEmail[user][1] > 1:
			# mais de um usuário por e-mail
			if user != '':
				countDeduplication += 1
				sumOccurrences += fakeUsersDictEmail[user][1]

	print('Quantidade usuários deduplicados:', countDeduplication, '(', (countDeduplication/len(fakeUsersList)), '% )')
	print('Média de', (sumOccurrences/countDeduplication), 'usuários por e-mail')
	print('\nQuantidade usuários e-mail vazio:', fakeUsersDictEmail[''][1])
else:
	print('Nenhum usuário deduplicado utilizando o e-mail')

print('\n=== Deduplicação por username ===')
# cria dicionário de usuários duplicados por username
ret = deduplicateUsersByUsername(fakeUsersList, fakeUsersDictUsername)

if ret:
	countDeduplication = 0
	sumOccurrences = 0

	for user in fakeUsersDictUsername:
		if fakeUsersDictUsername[user][1] > 1:
			# mais de um usuário por e-mail
			if user != '':
				countDeduplication += 1
				sumOccurrences += fakeUsersDictUsername[user][1]
				
	print('Quantidade usuários deduplicados:', countDeduplication, '(', (countDeduplication/len(fakeUsersList)), '% )')
	print('Média de', (sumOccurrences/countDeduplication), 'usuários por username')
	print('\nQuantidade usuários username vazio:', fakeUsersDictUsername[''][1])
else:
	print('Nenhum usuário deduplicado utilizando o username')

print('\n=== Deduplicação por primeiro e último nomes ===')
# cria dicionário de usuários duplicados por primeiro e último  nomes
ret = deduplicateUsersByFirstLastName(fakeUsersList, fakeUsersDictFirstLastName)

if ret:
	countDeduplication = 0
	sumOccurrences = 0

	for user in fakeUsersDictFirstLastName:
		if fakeUsersDictFirstLastName[user][1] > 1:
			# mais de um usuário por e-mail
			if user != '':
				countDeduplication += 1
				sumOccurrences += fakeUsersDictFirstLastName[user][1]
				
	print('Quantidade usuários deduplicados:', countDeduplication, '(', (countDeduplication/len(fakeUsersList)), '% )')
	print('Média de', (sumOccurrences/countDeduplication), 'usuários por primeiro e último nomes')
	print('\nQuantidade usuários nome vazio:', fakeUsersDictFirstLastName[''][1])
else:
	print('Nenhum usuário deduplicado utilizando o primeiro e último nomes')

