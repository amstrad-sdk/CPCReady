import os
import sys
from rich.console import Console
from rich.text import Text
import subprocess
import datetime
import time
console = Console()


class ConsoleColor:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

##
# Print message warning
#
# @param file: File to which the message refers
# @param message: message to display
##
def messageWarning(message):
    console.print("[yellow]\[🟡] ==> [white]" + message)

##
# Print message eror
#
# @param file: File to which the message refers
# @param message: message to display
##
def messageError(message):
    console.print("[bold red]\[💥] ==> [bold white]" + message)

##
# Print message info
#
# @param file: File to which the message refers
# @param message: message to display
##
def messageInfo(message):
    console.print("[green]\[👍] ==> [bold white]" + message)


# def checkProjectValue(text, value):
#     if value is None or value == "":
#         messageError(value, "The " + str(text) + " key does not exist or has no value.")
#         sys.exit(1)


##
# Print message color
#
# @param text: text to print
# @param color: Color with which the text will be painted
##
def consoleMessage(text, color):
    colored_text = f"{color}{text}{ConsoleColor.RESET}"
    return colored_text

##
# Get Get file without extension
#
# @param source: source filename
##
def getFile(source):
    file_name = os.path.basename(source)
    file_name = os.path.splitext(file_name)[0]
    return file_name


##
# Get file and extension
#
# @param source: source filename
##
def getFileExt(source):
    file_name = os.path.basename(source)
    return file_name


##
# Get extension file
#
# @param source: source filename
##
def getFileExtension(source):
    file_extension = os.path.splitext(source)[1]
    return file_extension


##
# Remove comment lines
#
# @param source: source filename
# @param output: output filename
##
def removeComments(source, output):
    global file
    if not os.path.exists(source):
        messageError(f"The " + getFileExt(source) +" file does not exist")
        return False

    with open(source, 'r') as file:
        lines = file.readlines()

    filtered_lines = [line for line in lines if not line.startswith("1'") and not line.startswith("1 '")]

    with open(output, 'w') as file:
        file.writelines(filtered_lines)
    file = getFileExt(source)
    messageInfo(file +"[green] ==> [/green]File Comments Removed")
    return True


##
# Conver unix2dos files
#
# @param source: source filename
# @param output: output filename
##
# def convert2Dos2(source):
#     if not os.path.exists(source):
#         messageError(f"The " + getFileExt(source) +" file does not exist")
#         endCompilation("ERROR")
#         sys.exit(1)
#     SDK4BASIC_PATH = os.environ.get('SDK4BASIC_PATH')

#     cmd = ['unix2dos', source]
#     try:
#         output = subprocess.check_output(cmd)
#         messageInfo(getFileExt(file) + f" unix to dos.")
#     except subprocess.CalledProcessError as e:
#         messageError(getFileExt(source) + f' ==> Error executing command: {e.output.decode()}')
#         sys.exit(1)

#     files = getFileExt(source)
#     messageInfo(files +"[green] ==> [/green]Convert unix to dosdddddd")
    
def convert2Dos(source, output):
    if not os.path.exists(source):
        messageError(f"The " + getFileExt(source) +" file does not exist")
        return False
    with open(source, 'r') as file:
        unix_lines = file.readlines()

    dos_lines = [line.rstrip('\n') + '\r\n' for line in unix_lines]

    with open(output, 'w') as file:
        file.writelines(dos_lines)

    files = getFileExt(source)
    messageInfo(files +"[green] ==> [/green]Convert unix to dos")
    return True

##
# Concatenate Bas file
#
# @param source: source file name
# @param output: output file name
##
def concatFile(source, output):
    with open(source, 'r') as origen_file:
        contenido_origen = origen_file.read()
    with open(output, 'a') as destino_file:
        destino_file.write(contenido_origen)
    os.remove(source)
    # messageInfo(getFileExt(source), f"Concatenate in {getFileExt(output)}.")
    messageInfo(getFileExt(source) + f" ==> {getFileExt(output)}")
    return True

##
# verify file exist
#
# @param source: source file name
##
def fileExist(source):
    if not os.path.isfile(source):
        messageError(getFileExt(source) +"[red] ==> FILE DOES NOT EXIST")
        return False
    return True

##
# Concatenate Bas files
#
# @param files: list files separate with ","
# @param output: output filename
##
def concatBasFiles(files, output, folder):
    if files != "":
        ficheros = files.split(',')
        folder = folder + "/"
        if os.path.exists(folder + output):
            os.remove(folder + output)
        with open(folder + output, 'a') as salida:
            for fichero in ficheros:
                nombre_fichero = fichero.strip()
                if os.path.exists(folder + nombre_fichero):
                    with open(folder + nombre_fichero, 'r') as archivo:
                        contenido = archivo.read()
                        salida.write(contenido)
                    os.remove(folder + nombre_fichero)
                    messageInfo(nombre_fichero + f" ==> {getFileExt(output)}")
                else:
                    messageError(f"The " + getFileExt(nombre_fichero) +" file does not exist")
                    return False
    else:
        messageWarning("Warning Not concat files.")
        return True
    return True

##
# end compilation
#
# @param type: show final compilation values OK or ERROR
##
def endCompilation(type,start_time):
    end_time = time.time()  # Registrar el tiempo de finalización
    execution_time = end_time - start_time
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    console.print("\n[bold white]------------------------------------------------------------------------------------- [/bold white]")
    if type == "OK":
        console.print("[bold green]BUILD SUCCESSFULLY [/bold green]")
    if type == "ERROR":
        console.print("[bold red]BUILD FAILURE [/bold red]")
    console.print("[bold white]------------------------------------------------------------------------------------- [/bold white]")
    console.print(f"[white]Total time: {execution_time:.2f} seg [/white]")
    console.print(f"[white]Finished at: {formatted_datetime}[/white]")
    console.print("[bold white]------------------------------------------------------------------------------------- [/bold white]")
    if type == "ERROR":sys.exit(1)
    if type == "OK":sys.exit(0)
##
# begin compilation
#
# @param project: show project name in initial compilation
##
def beginCompilation(project,author,model):
    # console.print("\n[bold white]------------------------------------------------------------------------------------- [/bold white]")
    # console.print("[bold blue] PROJECT: [/bold blue][bold white]" + project + "[/bold white]")
    # console.print("[bold white]------------------------------------------------------------------------------------- [/bold white]\n")
    console.print("\n[bold white]------------------------------------------------------------------------------------- [/bold white]")
    console.print("[bold blue] PROJECT: [/bold blue][bold white]" + project + "[/bold white]")
    console.print("[bold blue] AUTHOR : [/bold blue][bold white]" + author + "[/bold white]")
    console.print("[bold blue] MODEL  : [/bold blue][bold white]CPC " + str(model) + "[/bold white]")
    console.print("[bold white]------------------------------------------------------------------------------------- [/bold white]\n")

##
# compilation image
#
# @param project: image name
##
def imageCompilation(image):
    console.print("\n[bold white]------------------------------------------------------------------------------------- [/bold white]")
    console.print("[bold blue] IMAGE: [/bold blue][bold white]" + image + "[/bold white]")
    console.print("[bold white]------------------------------------------------------------------------------------- [/bold white]\n")

##
# create project
#
# @param project: image name
##
def createProject(project):
    console.print("\n[bold white]------------------------------------------------------------------------------------- [/bold white]")
    console.print("[bold blue]CREATE PROJECT: [/bold blue][bold white]" + project + "[/bold white]")
    console.print("[bold white]------------------------------------------------------------------------------------- [/bold white]\n")

##
# end create project
#
# @param type: show final compilation values OK or ERROR
##
def endCreteProject(type):
    console.print("\n[bold white]------------------------------------------------------------------------------------- [/bold white]")
    if type == "OK":
        console.print("[bold green]CREATE PROJECT SUCCESSFULLY [/bold green]")
    if type == "ERROR":
        console.print("[bold red]CREATE PROJECT FAILURE [/bold red]")
    console.print("[bold white]------------------------------------------------------------------------------------- [/bold white]")
    if type == "ERROR":sys.exit(1)
    if type == "OK":sys.exit(0)