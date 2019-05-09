import numpy as np
import cherrypy
import sys
import random

class Server:
    
    tableau = [ [ 0,  1,  2,  3,  4],
                [ 5,  6,  7,  8,  9],
                [10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19],
                [20, 21, 22, 23, 24] ]

    

    diagonales_ind = [ [ 0,  6, 12, 18, 24],
                       [ 4,  8, 12, 16, 20] ]
    
    but = np.identity(5)

    ind_but = np.where(but == 1)

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
        
        case = [0,1,2,3,4,5,10,15,20,9,14,19,24,21,22,23]

        cube = random.choice(case)

        deplacements = { 'N': -5,
                         'S': +5,
                         'E':  1,
                         'W': -1 }

        orientation = random.choice(list(deplacements.keys()))
        
        interdits = { 'E': [4, 9, 14, 19, 24],
                      'W': [0, 5, 10, 15, 20],
                      'N': [0, 1, 2, 3, 4],
                      'S': [20, 21, 22, 23, 24] }
        
        if body['players'][1] == body['you']:
            you = 1
        else:
            you = 0

        while body['game'][cube] != None and body['game'][cube] != you:
            cube = random.choice(case)
        
        if cube == 0:
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
                
        print("hello")
        if len(body['moves']) == 0:
            cube = 20
            orientation = 'N'

        #if len(body['moves']) == 1:
            cube = 20
            orientation = 'N'

        if len(body['moves']) == 2:
            cube = 24
            orientation = 'W'

        #if len(body['moves']) == 3:
            cube = 0
            orientation = 'S'

        if len(body['moves']) == 4:
            cube = 24
            orientation = 'N'
        
        #if len(body['moves']) == 5:
            cube = 24
            orientation = 'S'
        
    
        #print(body['move'])
        return {"move": {"cube": int(cube),"direction": str(orientation)},"message": "Hi"}

    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_port': '0.0.0.0' ,'server.socket_port': port})
    cherrypy.quickstart(Server())