from ex1 import texto
puntuacion = "¡!\"'(),-.,:;¿?]" + u"\u00AB" + u"\u00BB"
texto = "".join([x for x in texto if x not in puntuacion])
