class Playlist():

    def __init__(self, nome, minutosReproducao):
        self.nome = nome
        self.minutosReproducao = minutosReproducao
        self.inicioReproducao = 0

    def listar():
        playlist = []
        playlist.append(Playlist("Sicko Drop", 2))
        playlist.append(Playlist("É Hit Brasil", 5))
        playlist.append(Playlist("Guns and Roses", 2))
        playlist.append(Playlist("Acorda Pedrinho", 5))
        return playlist
