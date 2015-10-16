import valve.source.a2s

SERVER_ADDRESS = ('74.91.114.144', 27015)

server = valve.source.a2s.ServerQuerier(SERVER_ADDRESS)
info = server.get_info()
players = server.get_players()

print("{player_count}/{max_players} on {map} {server_name}".format(**info))
