from spleeter.separator import Separator

def separador(caminho):
	separator = Separator('spleeter:5stems')
	dest = 'output'
	separator.separate_to_file(caminho, dest)

# separador('music/Downtown.mp3')
