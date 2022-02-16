# fan-or-poser

Neste trabalho foi desenvolvida uma aplicação interativa utilizando diversos conceitos de recuperação de informação musical. A aplicação tem o propósito de julgar se o usuário é fã ou não de determinado artista musical ou banda. Funciona como um _quiz_, inicialmente o usuário deve fornecer o nome do artista que ele se considera fã, e depois serão retornadas músicas desse artista com algumas modificações, como a remoção de vocal ou algum instrumento e inserção de ruído. Para a remoção dos instrumentos foi utilizado o [Spleeter](https://github.com/deezer/spleeter) que é uma ferramenta para decomposição musical. 

## Instalação
```
pip install -r requirements.txt
```

### Como Executar
```
export CLIENT_ID=client_id_from_spotify_API
export CLIENT_SECRET=client_secret_from_spotify_API
python app.py
```
