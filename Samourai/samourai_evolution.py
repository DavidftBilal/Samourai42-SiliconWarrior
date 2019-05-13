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

        ### identification
        if body['you'] == body['players'][0]:
            you , adv = 0 , 1
        else:
            you , adv = 1 , 0
    
        ### par defaut le coup est choisit aleatoirement
        cube = random.choice([0,1,2,3,4,5,10,15,20,9,14,19,24,21,22,23])
        while body['game'][cube] == adv:
            cube = random.choice([0,1,2,3,4,5,10,15,20,9,14,19,24,21,22,23])
        
        orientation = random.choice(['N','S','E','W']) # si tt va bien on a un cube et une direction valide
        # mtn gerons les cas particuliers:
        interdits = { 'E': [4, 9, 14, 19, 24],
                      'W': [0, 5, 10, 15, 20],
                      'N': [0, 1, 2, 3, 4],
                      'S': [20, 21, 22, 23, 24] }
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

        game_island_tr = np.array(body['game']).reshape(5,5).T.tolist() # sert a parcourir les collones
        grid_island_tr = np.arange(25).reshape(5,5).T.tolist()

        ### ouverture
        if you == 0 :  # si on joue en premier
            if len(body['moves']) == 0: # premier coup
                return {"move": {"cube": 20,"direction": 'N'},"message": "Hajime !"}
            if len(body['moves']) == 2 : # deuxieme coup
                if game_island[0][0] != you : # l'adversaire essaye de deloger le corner up_gauche 
                    return {"move": {"cube": 20,"direction": 'N'},"message": "on va vous atomiser !"}
                elif game_island[0][0] == you: # on a pas ete contré
                    if game_island[4][4] == None: # coup valide
                        return {"move": {"cube": 24,"direction": 'N'},"message": "on va vous atomiser !"}
                    elif game_island[4][0] == None:
                        return {"move": {"cube": 20,"direction": 'E'},"message": "on va vous atomiser !"}
            if len(body["moves"]) == 4:# troisieme coup
                if game_island[4][4] == None: # coup valide
                    return {"move": {"cube": 24,"direction": 'W'},"message": "sa commence fort !"}
        elif you == 1: # on joue en deuxieme 
            if len(body['moves']) == 1: # premier coup
                if game_island[4][0] == None: #coup valide
                    return {"move": {"cube": 20,"direction": 'N'},"message": "Hajime !"}
            if len(body['moves']) == 3: # deuxieme coup
                if game_island[4][4] == None: # coup valide
                    return {"move": {"cube": 24,"direction": 'N'},"message": "on va vous atomiser !"}
            if len(body["moves"]) == 5:# troisieme coup
                if game_island[4][4] == None: # coup valide
                    return {"move": {"cube": 24,"direction": 'W'},"message": "sa commence fort !"}
            

        ### est il possible de gagner par la grande diagonale ?, on utilise return pour stopper les calculs
        grand_diag = [game_island[0][0] , game_island[1][1] , game_island[2][2] , game_island[3][3], game_island[4][4]]
        if grand_diag.count(you) == 4:
            for k in range(5):
                if game_island[k][k] != you:
                    if k == 0:
                        if game_island[4][0] == None or game_island[4][0] == you:
                            return {"move": {"cube": grid_island[4][0],"direction": 'N'},"message": "checkmate"}
                        elif game_island[0][4] == None or game_island[0][4] == you:
                            return {"move": {"cube": grid_island[0][4],"direction": 'W'},"message": "checkmate"}
                    if k == 4:
                        if game_island[4][0] == None or game_island[4][0] == you:
                            return {"move": {"cube": grid_island[4][0],"direction": 'E'},"message": "checkmate"}
                        elif game_island[0][4] == None or game_island[0][4] == you:
                            return {"move": {"cube": grid_island[0][4],"direction": 'S'},"message": "checkmate"}
                    if k == 1 or k == 2 or k == 3:
                        if game_island[k-1][k] == you: # il est en echec par le cube au dessus
                            if game_island[4][k] == you or game_island[4][k] == None: # coup valide
                                return {"move": {"cube": grid_island[4][k],"direction": 'N'},"message": "checkmate"} 
                        if game_island[k][k+1] == you: # il est en echec par le cube à droite
                            if game_island[k][0] == you or game_island[k][0] == None: #coup valide
                                return {"move": {"cube": grid_island[k][0],"direction": 'E'},"message": "checkmate"}
                        if game_island[k+1][k] == you: # il est en echec par le cube du dessous
                            if game_island[0][k] == you or game_island[0][k] == None: # coup valide
                                return {"move": {"cube": grid_island[0][k],"direction": 'S'},"message": "checkmate"} 
                        if game_island[k][k-1] == you: # il est en echec par le cube à gauche
                            if game_island[k][4] == you or game_island[k][4] == None: # coup valide
                                return {"move": {"cube": grid_island[k][4],"direction": 'W'},"message": "checkmate"}


        ### est-il possible de gagner par la petite diagonale ? On utilise return pour stopper les calculs
        petit_diag = [game_island[0][4] , game_island[1][3] , game_island[2][2] , game_island[3][1] , game_island[4][0]]
        if petit_diag.count(you) == 4: # on est à un cube de la victoire
            for i in range(5):
                for j in range(5):
                    if (game_island[i][j] in petit_diag) and (game_island[i][j] != you):
                        if i == 0 and j == 4:
                            if game_island[0][0] == None or game_island[0][0] == you:
                                return {"move": {"cube": grid_island[0][0],"direction": 'E'},"message": "checkmate"}
                            elif game_island[4][4] == None or game_island[4][4] == you:
                                return {"move": {"cube": grid_island[4][4],"direction": 'N'},"message": "checkmate"}
                        if i == 4 and j ==0:
                            if game_island[0][0] == None or game_island[0][0] == you:
                                return {"move": {"cube": grid_island[0][0],"direction": 'S'},"message": "checkmate"}
                            elif game_island[4][4] == None or game_island[4][4] == you:
                                return {"move": {"cube": grid_island[4][4],"direction": 'W'},"message": "checkmate"}
                        if (i==1 and j == 3) or (i==2 and j == 2) or (i == 3 and j == 1):
                            if game_island[k-1][k] == you: # il est en echec par le cube au dessus
                                if game_island[4][k] == you or game_island[4][k] == None: # coup valide
                                    return {"move": {"cube": grid_island[4][k],"direction": 'N'},"message": "checkmate"} 
                            if game_island[k][k+1] == you: # il est en echec par le cube à droite
                                if game_island[k][0] == you or game_island[k][0] == None: #coup valide
                                    return {"move": {"cube": grid_island[k][0],"direction": 'E'},"message": "checkmate"}
                            if game_island[k+1][k] == you: # il est en echec par le cube du dessous
                                if game_island[0][k] == you or game_island[0][k] == None: # coup valide
                                    return {"move": {"cube": grid_island[0][k],"direction": 'S'},"message": "checkmate"} 
                            if game_island[k][k-1] == you: # il est en echec par le cube à gauche
                                if game_island[k][4] == you or game_island[k][4] == None: # coup valide
                                    return {"move": {"cube": grid_island[k][4],"direction": 'W'},"message": "checkmate"}
        ### milieu de partie
        lin_you_nb = list()  # contient le nombre de 'you par ligne'
        for line in game_island:  # remplissage
            lin_you_nb.append(line.count(you))

        col_you_nb = list() # nombre de you par collone
        for col in game_island_tr:
            col_you_nb.append(col.count(you))

        lin_adv_nb = list() # contient le nombre de non you 
        for line in game_island:
            lin_adv_nb.append(line.count(adv))
        
        col_adv_nb = list() 
        for col in game_island_tr:
            col_adv_nb.append(col.count(adv))
        

        ## y'a t-il une victoire immmédiate ?
        if max(lin_you_nb) == 4: 
            the_line = lin_you_nb.index(4) # ligne offrant l'echec et mat
            deja_aligne = list() # indices des cases deja alignées
            for k in range(5):
                if game_island[the_line][k] == you:
                    deja_aligne.append(k)
            if deja_aligne == list(range(4)): # tt serrees a gauche
                if game_island[the_line][4] == None:
                    return {"move": {"cube": grid_island[the_line][4],"direction": 'W'},"message": "checkmate"}

            if deja_aligne == list(range(1,5)): # tt serree a droite
                if game_island[the_line][0] == None:
                    return {"move": {"cube": grid_island[the_line][0],"direction": 'E'},"message": "checkmate"}
        if max(col_you_nb) == 4:
            the_col = col_you_nb.index(4) # collone offrant l'echec et mat.
            deja_aligne = list() # indices des cases deja alignee
            for m in range(5):
                if game_island_tr[the_col][m] == you:
                    deja_aligne.append(m)
            if deja_aligne == list(range(4)): # tt serre vers le haut
                if game_island_tr[the_col][4] == None:
                    return {"move": {"cube": grid_island_tr[the_col][4],"direction": 'N'},"message": "checkmate"}
            if deja_aligne == list(range(1,5)):  # tt serree vers le bas 
                if game_island_tr[the_col][0] == None:
                    return {"move": {"cube": grid_island_tr[the_col][0],"direction": 'S'},"message": "checkmate"}
                  

        ## y'a t'il une défaite immediate ?
        if max(lin_adv_nb) == 4:
            the_line = lin_adv_nb.index(4) # ligne menacant le mat
            for j in range(5): # parcour de la ligne problematique
                if game_island[the_line][j] == adv:
                    if the_line != 0 and game_island[the_line - 1][j] != adv: # faudrait lui realigner le pion
                        if game_island[4][j] == None or game_island[4][j] == you: # coup valide
                            return {"move": {"cube": grid_island[4][j],"direction": 'N'},"message": "Bien essayé"}
                    if the_line == 0:
                        if game_island[4][j] == None or game_island[4][j] == you: # coup valide
                            return {"move": {"cube": grid_island[4][j],"direction": 'N'},"message": "Bien essayé"}
                    if the_line !=4 and game_island[the_line + 1][j] != adv:
                        if game_island[0][j] == None or game_island[0][j] == you: # coup valide
                            return {"move": {"cube": grid_island[0][j],"direction": 'S'},"message": "Bien essayé"}
                    if the_line == 4:
                        if game_island[0][j] == None or game_island[0][j] == you: # coup valide
                            return {"move": {"cube": grid_island[0][j],"direction": 'S'},"message": "Bien essayé"}
        if max(col_adv_nb) == 4:
            the_col = col_adv_nb.index(4) # collonne menacant de mat
            for i in range(5): # parcour de la collonne problematique 
                if game_island_tr[the_col][i] == adv:
                    if the_col != 0 and game_island_tr[the_col - 1][i] != adv:
                        if game_island_tr[4][i] == None or game_island_tr[4][i] == you: # coup valide
                            return {"move": {"cube": grid_island_tr[4][i],"direction": 'W'},"message": "Bien essayé"}
                    if the_col == 0:
                        if game_island_tr[4][i] == None or game_island_tr[4][i] == you: # coup valide
                            return {"move": {"cube": grid_island_tr[4][i],"direction": 'W'},"message": "Bien essayé"}
                    if the_col != 4 and game_island_tr[the_col + 1][i] != adv:
                        if game_island_tr[0][i] == None or game_island_tr[0][i] == you: # coup valide
                            return {"move": {"cube": grid_island_tr[0][i],"direction": 'E'},"message": "Bien essayé"}
                    if the_col == 4:
                        if game_island_tr[0][i] == None or game_island_tr[0][i] == you: #coup valide
                            return {"move": {"cube": grid_island_tr[0][i],"direction": 'E'},"message": "Bien essayé"}                            

        ### on joue un coup classique
        ## Situation A : les lignes sont plus prometteuses que les collones
        if max(lin_you_nb) >= max(col_you_nb): 
            the_line = lin_you_nb.index(max(lin_you_nb))  # indice de la ligne la plus prometteuse
            played = False
            for j in range(5): # parcours de la ligne prometteuse
                if game_island[the_line][j] != you and played == False:  # faudrait pas desaligner un de nos pions
                    if the_line != 0 and game_island[the_line - 1][j] == you: # you au dessus, attention au bord
                        if game_island[4][j] == None or game_island[4][j] == you: # on verifie que le coup est valide
                            cube = grid_island[4][j]            # on bouge la collonne vers le bas
                            orientation = 'N'
                            played = True    # on s'arrete de chercher
                    if the_line == 0  and game_island[1][j] == you: # you juste en dessous
                        if game_island[0][j] == None or game_island[0][j] == you: # on verifie que le coup est valide
                            cube , orientation = grid_island[0][j]  , 'S'
                            played = True
                    if the_line == 0 and game_island[1][j] != you :  # mais y'a pas de croix en dessous
                        if game_island[4][j] == None or game_island[4][j] == you: # coup valide
                            cube , orientation = grid_island[4][j] , 'N'
                            played = True
                    if the_line != 4 and game_island[the_line + 1][j] == you : # you en dessous
                        if game_island[0][j] == None or game_island[0][j] == you: # coup valide
                            cube , orientation = grid_island[0][j] , 'S'
                            played = True  # on s'arrete de chercher
                    if the_line == 4 and game_island[3][j] == you : # you au dessus
                        if game_island[4][j] == None or game_island[4][j] == you: # coup valide
                            cube , orientation = grid_island[4][j]  , 'N'
                            played = True
                    if the_line == 4 and game_island[3][j] != you:
                        if game_island[0][j] == None or game_island[0][j] == you: # coup valide
                            cube , orientation = grid_island[0][j] , 'S' 
                            played = True
        # Situation B : les collones sont plus prometteuses que les lignes
        elif max(lin_you_nb) < max(col_you_nb):
            the_col = col_you_nb.index(max(col_you_nb))  # indice de la collonne la plus prometteuse
            played = False
            for i in range(5):
                if game_island_tr[the_col][i] != you and played == False:  # faudrait pas desaligner un de nos pions
                    if the_col != 0 and game_island_tr[the_col - 1][i] == you: # you a gauche, attention au bord
                        if game_island_tr[4][i] == None or game_island_tr[4][i] == you: # on verifie que le coup est valide
                            cube = grid_island_tr[4][i]            # on bouge la collonne vers le bas
                            orientation = 'W'
                            played = True    # on s'arrete de chercher
                    if the_col == 0  and game_island_tr[1][i] == you: # you juste à droite
                        if game_island_tr[0][i] == None or game_island_tr[0][i] == you: # on verifie que le coup est valide
                            cube , orientation = grid_island_tr[0][i]  , 'E'
                            played = True
                    if the_col == 0 and game_island_tr[1][i] != you:  # mais y'a pas de croix à droite
                        if game_island_tr[4][i] == None or game_island_tr[4][i] == you: # coup valide
                            cube , orientation = grid_island_tr[4][i] , 'W'
                            played = True
                    if the_col != 4 and game_island_tr[the_col + 1][i] == you : # you à droite
                        if game_island_tr[0][i] == None or game_island_tr[0][i] == you: # coup valide
                            cube , orientation = grid_island_tr[0][i] , 'E'
                            played = True  # on s'arrete de chercher
                    if the_col == 4 and game_island_tr[3][i] == you : # you au dessus
                        if game_island_tr[4][i] == None or game_island_tr[4][i] == you: # coup valide
                            cube , orientation = grid_island_tr[4][i]  , 'W'
                            played = True
                    if the_col == 4:
                        if game_island_tr[0][i] == None or game_island_tr[0][i] == you: # coup valide
                            cube , orientation = grid_island_tr[0][i] , 'E' 
                            played = True                            
                    


        print("les moves sont : {}".format(body['moves']))

        message = "I'm the last samourai"
        if max(lin_you_nb) == 4 or max(col_you_nb) == 4:
            message = "echec !"
        if (max(lin_you_nb) == 3 or max(col_you_nb) == 3) and not (max(lin_you_nb) == 4 or max(col_you_nb) == 4):
            message = "Omae Wa mochinderu !"
        
        return {"move": {"cube": cube,"direction": orientation},"message": message}


    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_port': '0.0.0.0' ,'server.socket_port': port})
    cherrypy.quickstart(Server())   

