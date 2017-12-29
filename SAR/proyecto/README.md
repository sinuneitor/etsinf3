# Proyecto laboratorio: News-SARcher

Se incluye un servidor buscador para poder probarlo con nc, con la [app android](https://play.google.com/store/apps/details?id=com.kauron.newssarcher) (código incluido) o con el bot de Telegram. Con el bot se puede hablar directamente como si fuera un usuario o utilizar el modo inline.

Para el [bot](./telegram-bot/bot.py):
* [API key](https://core.telegram.org/bots#6-botfather) para la comunicación con Telegram.
* IP o dominio y puerto (2048 por defecto) del servidor python que responde a las preguntas de los usuarios.

Para el despliegue de ambos se incluyen Dockerfiles, que siven para generar containers:

* Para crear las imágenes de docker, en esta carpeta

    docker build -t user/news-sarcher:mini-enero .
    cd telegram-bot
    docker built -t user/news-sarcher-bot:latest .

* Para ejecutar por primera vez (la configuración no se puede cambiar después de que haya comenzado)

    docker run -p 2048:2048 -dt user/news-sarcher:mini-enero
    docker run -t user/news-sarcher-bot:latest -e SERVER_PORT=2048 -e SERVER_URL=localhost

* Para parar o arrancar cada servicio:

    docker start [IMAGE]
    docker stop [IMAGE]

