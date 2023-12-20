import os
from subprocess import PIPE, run # execute des commande de run pour go
import json      # Working with json files
import shutil    # Copy and overwrite operations
import sys       # command line arguments



GAME_DIR_PATTERN = "game"    # variable correspondant au pattern recherché 
GAME_CODE_EXTENSION = ".go"  # variable correspondant au pattern ".go"

GAME_COMPILE_COMMAND = ["go", "build"] #xxxxxxxxxxxxxxxxxxxxxxxxxxx#


def find_all_games_paths(source):   # Fonction pour trouver les dossier contenant la str "game"
    game_paths = []                 # Liste vide dans laquelle on stockera les path trouvés
    
    for root, dirs, files in os.walk(source):       # Boucle qui permet de rechercher dans tous les dossiers grâce à os.walk en fonction de source(argv[1]) 
        for directory in dirs:                      # 2e boucle
            if GAME_DIR_PATTERN in directory.lower():       # Si le pattern recherché est trouvé dans directory(transformé en min par précaution)
                path = os.path.join(source, directory)      # On concatene et on met le résultat (source + le dossier resultant) dans une variable path
                game_paths.append(path)                     # On rajoute la variable path à notre liste vide et tant qu'on est dans la boucle, tous les résultats seront rajouté en fin de liste grâce à la méthode append
                
        break
    return game_paths



def get_name_from_path(paths, to_strip):    # Fonction qui permettre d'enlever le suffixe "game" des dossier/fichiers (to_strip = enlever)
    new_names = []             # Liste vide qui contiendra les nouveaux noms de path
    for path in paths:
        _, dir_name = os.path.split(path)  # Variable qui Permet de récupérer suelement le nom du dossier en enlevant tout le préfixe_PATH
        new_dir_name = dir_name.replace(to_strip, "")   # variable qui permet de remplacer "to"_strip"(str que l'on souhaite enlever ici "game") par rien
        new_names.append(new_dir_name)
        
    return new_names



def create_dir(path):  # Fonction pour la création du dossier de destination
    if not os.path.exists(path):   # Si le dossier (path(argv[2])) n'esiste pas, check grâce à os.path.exist(nom_du_dossier)
        os.mkdir(path)              # Alors création du dossier (path(argv[2])) grâce à os.mkdir(nom_du_dossier)



def copy_and_overwrite(source, dest):     # Fonction permettant la copie des fichiers trouvés dans le nouveau dossier ainsi que l'overwrite du fichier s'il est existant
    if os.path.exists(dest):  # Si le dossier dest existe
        shutil.rmtree(dest)   # shutil.rmtree permet de suppr le dosier dest
    shutil.copytree(source, dest)   # shutil.copytree permet de copier le dossier source dans le dossier dest



def make_json_metadata_file(path, game_dirs): # Fonction permettant de créer un json à partir du Path et du nom du dossier
    data = {                                   
        "gameNames": game_dirs,                 # Dictionnaire mis en forme en fonction de ce que l'on souhaite
        "numberOfGames": len(game_dirs)
    }
    with open(path, "w") as f:              # with permet d'ouvrir un fichier sans le fermer manuellement(il se ferme automatiquement des qu'on sort du with)
        json.dump(data, f)                  # On ouvre path qui correspond au chemin du fichier souhaité en "w" ce qui va le créer automatiquement
                                            # json.dump permet de dump data(notre dico) dans f(le fichier ouvert)

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx#
def compile_game_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):     # Boucle permettant de sonder tout le repertoire à partir de path
        for file in files:                      # sonde juste les fichiers
            if file.endswith(GAME_CODE_EXTENSION):     # Si un fichier match avec le pattern ".go"
                code_file_name = file           # Alors on save le nom de ce fichier dans la variable code_file_name
                break                           # break ici pour faire la boucle qu'une seule fois( pour le premier fichier trouvé)
        break
    
    if code_file_name is None:
        return
    command = GAME_COMPILE_COMMAND + [code_file_name]  
    
    run_command(command, path)      # On appelle la fonction qui va run la commande

def run_command(command, path):     # Fonction pour compiler le code go
    cwd = os.getcwd()               # variable pour relever le CurrentWorkingDirectory
    os.chdir(path)                  # os.chdir permet de changer de CurrentWorkingDirectory(position/dossier) avec en param le dossier voulu ici "path"

    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True) # Comme la commande go n'est pas un builtins, PIPE permet de faire lien entre le process utilisé pour run la commande et le code python.
                                                                            # Cela va donc prendre les élément de la liste "command" et les utilisés les uns à la suite des autres pour éxec la commande de compilation du code go
                                                                            # On mets tout ça dans une variable pour pouvoir le réutiliser
    print("compile result", result)    
    
    os.chdir(cwd)       # BONNE PRATIQUE, on revient au cwd enregistré au début                               

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx#                                          
                                            
def main(source, target):  # fonction main qui va appeller toutes les autres
    cwd = os.getcwd()     # os.getcwd (GetCurrentWorkingDirectory) permet de determiner le bon pwd peut importe l'OS
    source_path = os.path.join(cwd, source)  # grâce à join on concatene le current PATH et le nom du dossier
    target_path = os.path.join(cwd, target)  # idem pour le dossier de destination

    game_path = find_all_games_paths(source_path)  # On créer une variable pour la fonction en indiquant le chemin du dossier source avec la variable source_path
    new_game_dirs = get_name_from_path(game_path, GAME_DIR_PATTERN)  # Variable qui fait appel à la fonction qui permet de retirer "game" du Path trouvé

    create_dir(target_path)
    
    for src, dest in zip(game_path, new_game_dirs): # zip va permettre de créer un tuple ((source_path1: dosiier1), (source_path2: dossier2), etc) | src va itérer sur game_path et des va itérer sur new_game_dirs
        dest_path = os.path.join(target_path, dest) # création d'une variable qui permet de concatener(join) le Path destination (target_path=*/Dossier_de_destination + dest=/fichier_ou_dossier), ex : C:\\Dossier\fichier.txt
        copy_and_overwrite(src, dest_path)      # Appel de la fonction copy qui prendre en arg la src (correspondant au chemin source) et dest_path(correspondant à la variable précédente)
      # compile_game_code(dest_path)            # Appel de la fonction qui va nous permettre de compiler les fichiers .go
        
    json_path = os.path.join(target_path, "metadata.json")  # Concatene et stocke en variable le Path et le nom que l'on souhaite donner à notre fichier.json
    make_json_metadata_file(json_path, new_game_dirs)       # appel de la fonction qui va créer un json en parametre le Path du json et dossier à traiter dans le Json
    #print(new_game_dirs)
    # print(game_path) # print de cette variable
    
      
    
if __name__ == "__main__":  # Permet de s'assurer que le script s'executera que si on le lance manuellement !
    args = sys.argv         # sys.argv correspond aux arguemnts de la commande executé ex : python3 nom_du_script.py   /dir     /papa 
    #print(args)                                                                                       argv[0]      argv[1]  argv[2]
    if len(args) != 3:
        raise Exception("Vous devez passer 2 arguments: /source et /destination")
    
    source, target = args[1:] # source = argv[1], target = argv[2]  (1:) = à partir de 1 (pas le 0 qui correspond au nom du script)
    #print(source, target)
    main(source, target)  # appel de la fonction main qui elle même appelle toutes les fonctions dont on a besoin
    