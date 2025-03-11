
# Variables globales

# Variable que almacena el número de discos que se van a mover
numbers_disks = 0
# Lista que almacena el tamaño y color de los discos
sizeAndColor = []

""" Funcion enfocada en obtener la cantidad de discos """
def get_quantity_disks():
    # Se llama a la variable global
    global numbers_disks
    # Se solicita al usuario la cantidad de discos que desea mover
    disks = int(input("Enter the quantity of disks you want to move: "))
    if disks > 0 and disks < 9:
        numbers_disks = disks
    else:
        print("The number of disks must be between 1 and 8")
        get_quantity_disks()

""" Funcion enfocada en obtener el tamaño y color de los discos """
def get_size_and_color():
    # Se solicita al usuario el tamaño y color de los discos segun la cantidad ingresada de discos
    for _ in range(numbers_disks):
        # Se solicita al usuario el tamaño del disco
        size = int(input("Enter the size of the disk: "))
        # Se solicita al usuario el color del disco
        color = input("Enter the color of the disk: ")
        # Se agrega el tamaño y color a la lista
        sizeAndColor.append({'size': size, 'color': color})




""" Fncion enfocada en inicializar los pilares y en llamar la función que gestiona los movimientos de los discos """
def set_towers(numbers_disks, sizeAndColor):

    # Se verifica que la lista no este vacia
    if not sizeAndColor:
        return "No Disk Provided"

    # Se crea un diccionario con las torres con las cuales se administrarán los discos
    towers = {
        "A": sizeAndColor,
        "B": [],
        "C": []
    }

    try:
        # Se crea un array para almacenar los movimientos de los discos
        moves = []
        # Se llama a la función que gestiona los movimientos de los discos
        hanoi(numbers_disks, 'A', 'B', 'C', towers, moves)

        # Se imprimen los movimientos
        for move in moves:
            print(move)
    except ValueError as Error:
        # Se imprime el mensaje de error
        print(Error)


"""" Funcion que valida si se puede mover el disco """
def can_move(disk, tower):

    # Se verifica si la torre esta vacia
    if not tower:
        return True
    
    # Se toma el disco que se encuentra en la parte superior de la torre
    top_disk = tower[-1]
    # Se retorna booleano para confirmar que los discos puedan ser movidos
    return disk['size'] < top_disk['size'] and disk['color'] != top_disk['color']

"""" Funcion que gestiona los movimientos de los discos """
def hanoi(numbers_disks, origin, destination, axuiliary, towers, moves):

    # Se verifica que la cantidad de discos que se encuentran en el pilar de origen
    if numbers_disks == 0:
        return
    
    # Se reutliza la funcion hanoi, con el movimiento del disco
    hanoi(numbers_disks - 1, origin, axuiliary, destination, towers, moves)

    # Se mueve el disco de la torre de origen a una de las torres
    successfull, message = move_disk(origin, destination, towers)

    # Se agrega el movimiento a la lista
    if successfull:
        moves.append(message)
    else:
        raise ValueError(message)

    # Se reutliza la funcion hanoi, diferenciando las torres de origen, auxiliar y destino
    hanoi(numbers_disks - 1, axuiliary, destination, origin, towers, moves)

def move_disk(origin, destination, towers):

    # Se verifica que la torre de origen no este vacia
    if not towers[origin]:
        return False, f"NONE"

    # Se toma el disco que se encuentra en la parte superior de la torre
    disk = towers[origin][-1]

    # Se verifica si se puede mover el disco
    if can_move(disk, towers[destination]):
        # Se mueve al otro pilar el disco tomado de la torre origen
        towers[destination].append(towers[origin].pop())
        # Se retorna un booleano y el mensaje
        return True, f"{disk['size']}, ({origin}, {destination})"
    else:
        # Se retorna un booleano y un error si no se puede mover el disco
        return False, f"Impossible to complete the transfer"


""" Función principal """	
def __main__():
    # Se obtiene la cantidad de discos
    get_quantity_disks()
    # Se obtiene el tamaño y color de los discos
    get_size_and_color()
    # Se llama funcion que gestiona los movimientos
    set_towers(numbers_disks, sizeAndColor)

""" Condicional que ejecuta el archivo si este es llamado directamente """
if __name__ == "__main__":
    __main__()