import sqlite3

# Se define  la funcion para crear la DB
def crear_bd():
	# Creación y conexión con la DB

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
			# Campo ID es PK y AUTOINCREMENT. Nombre es UNIQUE
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

# Definir función categoria
def agregar_categoria():

	# Input para que el usuario escriba categoria
	categoria = input("Escribe el nombre de la nueva categoria\n")

	conexion = sqlite3.connect('restaurante.db')
	cursor = conexion.cursor()

	# Insertar valores en la tabla categorías
	try:
		cursor.execute("INSERT INTO categorias VALUES (null, '{}')".format(categoria))

	# Mandar error si ya existe
	except sqlite3.IntegrityError:
		print("La categoria '{}' ya ha sido creada anteriormente".format(categoria))

	# Mandar aviso cuando se crea
	else:
		print("Categoria '{}' creada correctamente".format(categoria))

	conexion.commit()
	conexion.close()

# Definir función plato
def agregar_plato():

	# Creación y conexión con la DB
	conexion = sqlite3.connect('restaurante.db')
	cursor = conexion.cursor()	

	categorias = cursor.execute("SELECT * FROM categorias").fetchall()

	print("Selecciona una categoria para añadir el plato: ") 

	# Iterar las categorias y mostrar campo 1 y 2
	for categoria in categorias:
		print("[{}]{}".format(categoria[0], categoria[1]))

	# Input para usuario. Concertir el input a integer
	categoria_usuario = int(input("---> "))

	plato = input("Escribe el nombre del nuevo plato\n ")

	# Insertar valores en la tabla platos. Se pasan los valores plato y categoria_usuario
	try:
		cursor.execute("INSERT INTO platos VALUES (null, '{}', {})".format(plato, categoria_usuario))

	# Revisar si ya fue creada el plato
	except sqlite3.IntegrityError:
		print("El plato '{}' ya fue agregado anteriormente.".format(plato))

	else:
		print("Plato '{}' creado exitosamente".format(plato))

	conexion.commit()
	conexion.close()

# Definir función mostrar menú
def mostrar_menu():
	# Creación y conexión con la DB
	conexion = sqlite3.connect('restaurante.db')
	cursor = conexion.cursor()	

	# Seleccionar las categorias
	categorias = cursor.execute("SELECT * FROM categorias").fetchall()

	# Iterar categorias y mostrar campo categoria
	for categoria in categorias:
		print(categoria[1])

		# Seleccionar platos
		platos = cursor.execute("SELECT * FROM platos WHERE categoria_id={}".format(categoria[0])).fetchall()

		# Iterar y mostrar platos
		for plato in platos:
			print("\t{}".format(plato[1]))

	conexion.close()

# Iniciar BD
crear_bd()

# Menu de opciones del programa
# Menú de inicio
while True:
	print("\n Bienvenido al menu del restaurante")

	opcion = input('''

		Elije una opción:

			1.- Introducir categorías 

			2.- Agregar un plato

			3.- Mostrar el menú

			4.- Salir del programa

		''')
	# Ejecutar funciones
	if opcion == "1":
		agregar_categoria()

	elif opcion == "2":
		agregar_plato()

	elif opcion == "3":
		mostrar_menu()

	# Salir del programa 
	elif opcion == "4":
		print("Nos vemos")
		break

	else:
		print("Opción no disponible. Favor de introducir un dígito existente")
