import numpy as np
import cherrypy
import sys
import random

class Server:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    
    
    def move(self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''
        
        body = cherrypy.request.json
        
        interdits = { 'E': [4, 9, 14, 19, 24],
                      'W': [0, 5, 10, 15, 20],
                      'N': [0, 1, 2, 3, 4],
                      'S': [20, 21, 22, 23, 24] }
        
        if body['players'][0] == body['you']:
            you = 0
        else:
            you = 1
        
        cube = random.choice([0,1,2,3,4,5,10,15,20,9,14,19,24,21,22,23])
        while body['game'][cube] != None and body['game'][cube] != you:
            cube = random.choice([0,1,2,3,4,5,10,15,20,9,14,19,24,21,22,23])
        
        # par defaut le coup est choisit aleatoirement
        orientation = random.choice(['N','S','E','W']) # si tt va bien on a un cube et une direction valide
        if cube == 0 :
            orientation = random.choice(['S','E'])

        elif cube == 4:
            orientation = random.choice(['S','W'])

        elif cube == 20:
            orientation = random.choice(['N','E'])

        elif cube == 24:
            orientation = random.choice(['N','W'])

        elif cube in interdits['N']:
            orientation = random.choice(['S','E','W'])

        elif cube in interdits['S']:
            orientation = random.choice(['N','E','W'])
        
        elif cube in interdits['E']:
            orientation = random.choice(['N','S','W'])

        elif cube in interdits['W']:
            orientation = random.choice(['N','S','E'])
        
        game_island = np.array(body['game']).reshape(5,5).tolist() # plateau de jeu
        grid_island = np.arange(25).reshape(5,5).tolist() # sert à faire la correspondance

        game_island_tr = np.array(body['game']).reshape(5,5).T.tolist()
        grid_island_tr = np.arange(25).reshape(5,5).T.tolist()

        ### opening
        if you == 0 :  # si on joue en premier
            if len(body['moves']) == 0: # premier coup
                cube , orientation = 20 , 'N'
            if len(body['moves']) == 2 : # deuxieme coup
                if game_island[0][0] != you : # l'adversaire essaye de deloger le corner up_gauche 
                    cube , orientation = 20 , 'N'
                elif game_island[0][0] == 0: # on a pas ete contré
                    if game_island[4][4] == None: # coup valide
                        cube , orientation = 24 , 'N'
                    else:
                        cube , orientation = 20 , 'E' # on le deloge du coin bas droit
                
            


        
        ### milieu de partie
        lin_you_nb = list()  # contient le nombre de 'you par ligne'
        for line in game_island:  # remplissage
            lin_you_nb.append(line.count(you))

        col_you_nb = list() # nombre de you par collone
        for col in game_island_tr:
            col_you_nb.append(col.count(you))
        
        if max(lin_you_nb) > max(col_you_nb): # les lignes sont plus prometteuses que les collones
            the_line = lin_you_nb.index(max(lin_you_nb))  # indice de la ligne la plus prometteuse
            played = False
            for j in range(5): # parcours de la ligne prometteuse
                if game_island[the_line][j] != you and played == False:  # faudrait pas desaligner un de nos pions
                    if the_line != 0 and game_island[the_line - 1][j] == you: # you au dessus, attention au bord
                        if game_island[4][j] == None or game_island[4][j] == you: # on verifie que le coup est valide
                            cube = grid_island[4][j]            # on bouge la collonne vers le bas
                            orientation = 'N'
                            played = True    # on s'arrete de chercher
                    elif the_line == 0  and game_island[1][j] == you: # you juste en dessous
                        if game_island[0][j] == None or game_island[0][j] == you: # on verifie que le coup est valide
                            cube , orientation = grid_island[0][j]  , 'S'
                            played = True
                    elif the_line == 0 :  # mais y'a pas de croix en dessous
                        if game_island[4][j] == None or game_island[4][j] == you: # coup valide
                            cube , orientation = grid_island[4][j] , 'N'
                            played = True
                    elif the_line != 4 and game_island[the_line + 1][j] == you : # you en dessous
                        if game_island[0][j] == None or game_island[0][j] == you: # coup valide
                            cube , orientation = grid_island[0][j] , 'S'
                            played = True  # on s'arrete de chercher
                    elif the_line == 4 and game_island[3][j] == you : # you au dessus
                        if game_island[4][j] == None or game_island[4][j] == you: # coup valide
                            cube , orientation = grid_island[4][j]  , 'N'
                            played = True
                    elif the_line == 4:
                        if game_island[0][j] == None or game_island[0][j] == you: # coup valide
                            cube , orientation = grid_island[0][j] , 'S' 
                            played = True
        elif max(lin_you_nb) < max(col_you_nb): # les collones sont plus prometteuses que les lignes
            the_col = col_you_nb.index(max(col_you_nb))  # indice de la collonne la plus prometteuse
            played = False
            for i in range(5):
                if game_island_tr[the_col][i] != you and played == False:  # faudrait pas desaligner un de nos pions
                    if the_col != 0 and game_island_tr[the_col - 1][i] == you: # you a gauche, attention au bord
                        if game_island_tr[4][i] == None or game_island_tr[4][i] == you: # on verifie que le coup est valide
                            cube = grid_island_tr[4][i]            # on bouge la collonne vers le bas
                            orientation = 'W'
                            played = True    # on s'arrete de chercher
                    elif the_col == 0  and game_island_tr[1][i] == you: # you juste à droite
                        if game_island_tr[0][i] == None or game_island_tr[0][i] == you: # on verifie que le coup est valide
                            cube , orientation = grid_island_tr[0][i]  , 'E'
                            played = True
                    elif the_col == 0 :  # mais y'a pas de croix à droite
                        if game_island_tr[4][i] == None or game_island_tr[4][i] == you: # coup valide
                            cube , orientation = grid_island_tr[4][i] , 'W'
                            played = True
                    elif the_col != 4 and game_island_tr[the_col + 1][i] == you : # you à droite
                        if game_island_tr[0][i] == None or game_island_tr[0][i] == you: # coup valide
                            cube , orientation = grid_island_tr[0][i] , 'E'
                            played = True  # on s'arrete de chercher
                    elif the_col == 4 and game_island_tr[3][i] == you : # you au dessus
                        if game_island_tr[4][i] == None or game_island_tr[4][i] == you: # coup valide
                            cube , orientation = grid_island_tr[4][i]  , 'W'
                            played = True
                    elif the_col == 4:
                        if game_island_tr[0][i] == None or game_island_tr[0][i] == you: # coup valide
                            cube , orientation = grid_island_tr[0][i] , 'E' 
                            played = True                            
                    


        print("les moves sont : {}".format(body['moves']))

        
        if max(lin_you_nb) == 4:
            message = "echec au roi !!!"
        if max(lin_you_nb) == 3:
            message = "Omae wa mochinderu"
        if max(lin_you_nb) == 2 or max(lin_you_nb) == 1 :
            message = "Asta la muerte !"
        if max(lin_you_nb) == 0:
            message = 'Hajime'
        
        return {"move": {"cube": cube,"direction": orientation},"message": message}


    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_port': '0.0.0.0' ,'server.socket_port': port})
    cherrypy.quickstart(Server())   

