import socket
from _thread import *
import pickle
from player import Player

server = "192.168.0.106"
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    if gameId in games:
    	conn.send(pickle.dumps(games[gameId]))

    reply = ""
    while True:
    
        try:
            data = pickle.loads(conn.recv(4096))

            if gameId in games:
                game = games[gameId]

                if not data:
                    break            
                else:
                	if (data.message == "reset"):
                		game.bluescore=data.bluescore
                		game.redscore=data.redscore
                		game.resetgame()
                		
                	elif (data.message == "drop"):
                		game.grid=data.grid
                		game.objects=data.objects
                		game.win=data.win
                		game.count=data.count
                		game.turn=data.turn
                	conn.sendall(pickle.dumps(game))
                	
            else:
                break
                
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
    	games[gameId] = Player(gameId)
    	print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1
    games[gameId].player=p


    start_new_thread(threaded_client, (conn, p, gameId))
