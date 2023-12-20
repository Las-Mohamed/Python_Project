import os
import sys
import subprocess
import shutil
Game_Pattern = "game"
def show_dir(source):
    list_directory = []
    for dirs in os.walk(source):                # Sonde le Répertoire grâce à oswalk        
        for directory in dirs:
            if Game_Pattern in directory:
                cwd = os.getcwd()
                path = os.path.join(source, directory)
                list_directory.append(path)
    print(list_directory)

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        raise Exception("Vous devez fournir 1 argument seulement")
    source = args[1]
    print(source)
show_dir(source)