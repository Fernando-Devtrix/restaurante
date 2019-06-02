import sqlite3

def crear_bd():
	conexion = sqlite3.connect('restaurante.db')
	cursor = conexion.cursor()

	# tabla categorias
	try:
		cursor.execute(
			'''
			CREATE TABLE categorias
				(
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					nombre VARCHAR(100) UNIQUE NOT NULL
				);
			'''
			)

	except sqlite3.OperationalError:
		print("La tabla 'Categorias' ya ha sido creada anteriormente")

	else:
		print("La tabla 'Categorias' sido creada exitosamente")

	# tabla platos

	try:
		cursor.execute(
			'''
			CREATE TABLE platos
				(
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					nombre VARCHAR(100) UNIQUE NOT NULL,
					categoria_id INTEGER NOT NULL,
					FOREIGN KEY(categoria_id) 
						REFERENCES categoria(id)
				);
			'''
			)

	except sqlite3.OperationalError:
		print("La tabla 'Platos' ya ha sido creada")

	else:
		print("La tabla 'Platos' se ha creado correctamente")

	conexion.close()

def agregar_categpria():
	categoria = input("Escribe el nombre de la nueva categoria\n")

	conexion = sqlite3.connect('restaurante.db')
	cursor = conexion.cursor()

	try:
		cursor.execute("INSERT INTO categorias VALUES (null, '{}')".format(categoria))

	except sqlite3.IntegrityError:
		print("La categoria '{}' ya ha sido creada anteriormente".format(categoria))

	else:
		print("Categoria '{}' creada correctamente".format(categoria))

	conexion.commit()
	conexion.close()

def agregar_plato():
	conexion = sqlite3.connect('restaurante.db')
	cursor = conexion.cursor()	

	categorias = cursor.execute("SELECT * FROM categorias").fetchall()

	print("Selecciona una categoria para añadir el plato: ") 

	for categoria in categorias:
		print("[{}]{}".format(categoria[0], categoria[1]))

	categoria_usuario = int(input("---> "))

	plato = input("Escribe el nombre del nuevo plato\n ")

	try:
		cursor.execute("INSERT INTO platos VALUES (null, '{}', {})".format(plato, categoria_usuario))

	except sqlite3.IntegrityError:
		print("El plato '{}' ya fue agregado anteriormente.".format(plato))

	else:
		print("Plato '{}' creado exitosamente".format(plato))

	conexion.commit()
	conexion.close()

def mostrar_menu():
	conexion = sqlite3.connect('restaurante.db')
	cursor = conexion.cursor()	

	categorias = cursor.execute("SELECT * FROM categorias").fetchall()

	for categoria in categorias:
		print(categoria[1])

		platos = cursor.execute("SELECT * FROM platos WHERE categoria_id={}".format(categoria[0])).fetchall()

		for plato in platos:
			print("\t{}".format(plato[1]))

	conexion.close()

# Iniciar BD
crear_bd()

# Menu de opciones del programa

while True:
	print("\n Bienvenido al menu del restaurante")

	opcion = input('''

		Elije una opción:

			1.- Introducir categorías 

			2.- Agregar un plato

			3.- Mostrar el menú

			4.- Salir del programa

		''')

	if opcion == "1":
		agregar_categpria()

	elif opcion == "2":
		agregar_plato()

	elif opcion == "3":
		mostrar_menu()

	elif opcion == "4":
		print("Nos vemos")
		break

	else:
		print("Opción no disponible. Favor de introducir un dígito exitente")
