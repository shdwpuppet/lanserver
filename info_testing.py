import valve.source.a2s

SERVER_ADDRESS = ('10.0.0.62', 27018)

server = valve.source.a2s.ServerQuerier(SERVER_ADDRESS)
info = server.get_info()
players = server.get_players()

print("{player_count}/{max_players} on {map} {server_name}".format(**info))
