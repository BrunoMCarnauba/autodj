# AutoDJ Amazon Music

Essa aplicação automatiza a reprodução de playlists na Amazon Music. Você informa para o sistema as playlists que deseja reproduzir e o tempo que ela deve ser reproduzida para passar para a próxima, e o sistema se encarrega de fazer essa mudança. Pode ser útil para um evento em que precise deixar o som ligado sem supervisão com uma variedade de playlists. Também é possível definir um filtro com palavras proibidas, para caso a música apresente alguma daquelas palavras, ele passe para a próxima música. Está em uma versão muito inicial, sem interface gráfica e sem tratamentos de erros. Abaixo há um trecho com algumas coisas que faltam ser implementadas.

## Tecnologia

Esse projeto foi desenvolvido com [Python 3.10.2](https://www.python.org/downloads/) e faz uso das dependências listadas abaixo. É recomendado instalá-las com o terminal no modo administrador, para que elas possam ser instaladas globalmente e evitar erros <br/>

### `pip install selenium`
"selenium" para automatizar as ações no navegador

### `pip install playsound`
"playsound" para reproduzir arquivos de audio

## Configuração

A lista de playlist pode ser informada no arquivo `playlist.py`. Nele é informado o nome da playlist e a quantidade de minutos que ela deve ser reproduzida. Na pasta vinhetas há uma vinheta de exemplo que é tocada durante a transição de playlists.

## Scripts disponíveis

No diretório do projeto, você pode rodar:

### `python main.py`

Para iniciar a aplicação.

## Como usar

Após fazer a configuração e iniciar a aplicação como informado acima, o programa irá abrir o navegador na página de login da amazon music. Após fazer o login, o programa automaticamente inicia suas atividades.

## O que falta?

- Reproduzir musicas genericas enquanto estiver mudo por ter detectado palavra proibida e não conseguir passar de faixa por não ter amazon unlimited <br/>
- Colocar possibilidade de tocar vinhetas de forma automática durante a reprodução da playlist <br/>
- Criar função de auto-duck in real time para que diminua o volume do chrome automaticamente caso determinado volume seja alcançado pelo microfone <br/>
- Melhorar organização do código <br/>
- Tratar possíveis exceções que podem acontecer pelo Selenium, para tentar ao máximo fazer com que o programa não pare <br/>
- Fechar automaticamente o diálogo do Amazon Music Unlimited caso ele apareça, após fazer o login <br/>
- Trocar de playlist apenas quando acabar a música da que está em reprodução <br/>
- Criar uma interface para configuração das playlists <br/>

## Links que podem ser úteis

[Selenium](https://selenium-python.readthedocs.io/getting-started.html) <br/>