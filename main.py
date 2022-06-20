from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta

# Locating Elements
from selenium.webdriver.common.by import By

# Actions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Waits
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Reprodução de arquivos de audio
from playsound import playsound

from playlist import Playlist

# Exemplo Whatsapp com Selenium: https://youtu.be/yUy81n5vF0k

print("Inicializando AutoDJ")

# Inicializando variáveis
titulo = None

# Configura o selenium / driver do chrome
caminhoDriver = r"chrome_driver/chromedriver.exe"
opcoes = Options()
# Se for precisar usar o perfil padrão, então tentar clonar o data-profile: https://forum.katalon.com/t/user-data-directory-is-already-in-use/40266/2
# opcoes.add_argument("user-data-dir=C:/Users/Bruno/AppData/Local/Google/Chrome/User Data")
# opcoes.add_argument("--profile-directory=Default")
opcoes.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=caminhoDriver, chrome_options=opcoes)

# Função para ajustar o volume do amazon music
def alterarVolume(key, diferencaVolume):
    # Aguarda o #volume-button aparecer
    WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.ID, "volume-button"))
    )

    volumeRange = driver.find_elements(By.CLASS_NAME, "_2A37HSwUCzCv8zFDLwOtsS")
    # * Se o range não estiver aparecendo então faz aparecer clicando no botão de volume
    if(len(volumeRange) == 0):
        containerVolume = driver.find_element(By.ID, "volume-button")
        botaoVolume = driver.execute_script("return document.querySelector('#volume-button').shadowRoot.querySelector('button')")
        ActionChains(driver).move_to_element(containerVolume).click(botaoVolume).perform()

    volumeRange = driver.find_element(By.CLASS_NAME, "_2A37HSwUCzCv8zFDLwOtsS").find_element(By.TAG_NAME, "input")
    for i in range(diferencaVolume):
        volumeRange.send_keys(key)
        time.sleep(0.4)

# Entra na página da amazon e aguarda o login
driver.get(r"https://www.amazon.com.br/ap/signin?clientContext=135-3599810-0649137&openid.return_to=https%3A%2F%2Fmusic.amazon.com.br%2F%3FrefMarker%3Dnull&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_webamp_br&openid.mode=checkid_setup&marketPlaceId=A2Q3Y263D00KWC&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=amzn_cpweb&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&siteState=clientContext%3D144-7069719-2176232%2CsourceUrl%3Dhttp%253A%252F%252Fmusic.amazon.com.br%252F%253FrefMarker%253Dnull%2Csignature%3Dnull")

print("Aguardando login")
WebDriverWait(driver, 1800).until(
    EC.presence_of_all_elements_located((By.ID, "navbarSearchInput"))
)

# FALTA FAZER: Se tiver aparecido o diálogo do Amazon Music Unlimited
# Se id dialogHeader (é um h1) tiver aparecido com o texto "Cadastre-se no Amazon Music Unlimited", então executar o comando abaixo
# clicar no botão document.querySelector('music-button').shadowRoot.querySelector('button')
# Se não, apenas continuar o código.

# Inicia a reprodução
listaPlaylists = Playlist.listar()
playlistAtual = -1
while(True):
    # Inicia a reprodução da playlist: Se ainda não tiver começado a tocar uma playlist ou estiver na hora de iniciar uma nova playlist.
    if((playlistAtual == -1 or (listaPlaylists[playlistAtual].inicioReproducao != 0 and time.time() - listaPlaylists[playlistAtual].inicioReproducao > listaPlaylists[playlistAtual].minutosReproducao*60)) and ((playlistAtual + 1) < len(listaPlaylists))):
        playlistAtual = playlistAtual + 1

        # Se já estiver tocando alguma playlist, então fazer a transição para tocar a próxima
        if(playlistAtual != 0):
            print("Transição para a próxima playlist")
            # Fecha o player se estiver aberto
            containerVoltar = driver.find_elements(By.ID, 'npvCloseButton')
            if(len(containerVoltar) != 0):
                botaoVoltar = driver.execute_script("return document.querySelector('#npvCloseButton').shadowRoot.querySelector('button')")
                ActionChains(driver).move_to_element(containerVoltar[0]).click(botaoVoltar).perform()

            # Diminuindo volume
            alterarVolume(Keys.DOWN, 9)
            playsound("vinhetas/vinheta01.mp3")

        # Aguarda encontrar o input navbarSearchInput ou passar 60 segundos
        WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.ID, "navbarSearchInput"))
        )

        # Limpa o campo de pesquisa (https://stackoverflow.com/questions/50677760/selenium-clear-command-doesnt-clear-the-element) e procura por Sicko Drop na barra de busca
        driver.find_element(By.ID, "navbarSearchInput").send_keys(Keys.CONTROL + "a")
        driver.find_element(By.ID, "navbarSearchInput").send_keys(Keys.DELETE)
        driver.find_element(By.ID, "navbarSearchInput").send_keys(listaPlaylists[playlistAtual].nome, Keys.RETURN)

        # Aguarda o music-horizontal-item aparecer
        WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "music-horizontal-item"))
        )

        time.sleep(5)

        # Reproduz a playlist
        # * Como localizar elemento com shadow-root: https://stackoverflow.com/questions/65445170/cant-locate-elments-within-shadow-root-open-using-python-selenium/65452620#65452620 
        # * Método 02 (inclusive também é no amazon music): https://stackoverflow.com/questions/69585279/unable-to-click-on-shadow-root-element-using-selenium
        containerMusica = driver.execute_script("return document.querySelector('music-shoveler').querySelector('music-horizontal-item')")
        botaoPlay = driver.execute_script("return document.querySelector('music-shoveler').querySelector('music-horizontal-item').shadowRoot.querySelector('.action-icon-button').shadowRoot.querySelector('button')")
        # Para ser capaz de clicar no elemento que não está visível primeiro precisa mover-se até o container para deixá-lo visível
        ActionChains(driver).move_to_element(containerMusica).click(botaoPlay).perform()
        
        # Guarda o tempo em que começou a reprodução
        listaPlaylists[playlistAtual].inicioReproducao = time.time()

        horarioAgora = datetime.now()
        horarioFimPlaylist = (datetime.now() + timedelta(minutes=listaPlaylists[playlistAtual].minutosReproducao))
        print("Reprodução começou às "+horarioAgora.strftime('%H:%M')+" e termina às "+horarioFimPlaylist.strftime('%H:%M'))

        # Maximiza a tela caso esteja minimizada. Para que posteriormente possa ficar sendo feita a verificação da letra
        containerMusicaAtual = driver.find_elements(By.CLASS_NAME, "_3l2xsX5-KkYUgDHJDu-L0r")
        if(len(containerMusicaAtual) != 0):
            botaoMusica = driver.execute_script("return document.querySelector('._3l2xsX5-KkYUgDHJDu-L0r').querySelector('music-horizontal-item').shadowRoot.querySelector('.left').querySelector('music-button').shadowRoot.querySelector('button')")
            botaoMusica.click()

        # Aumenta o volume
        alterarVolume(Keys.UP, 10)
    

    def pularFaixa():
        containerProximaMusica = driver.find_elements(By.ID, 'nextButton')
        if (len(containerProximaMusica) != 0):
            alterarVolume(Keys.DOWN, 10)
            botaoProximaMusica = driver.execute_script("return document.querySelector('#nextButton').shadowRoot.querySelector('button')")
            botaoProximaMusica.click()

            time.sleep(2)

            # Fecha caixa de diálogo que pode ter sido aberta por não conseguir mais pular a faixa por não ter o amazon music unlimited
            containerCloseButton = driver.find_elements(By.ID, "dialogCloseButton")
            if(len(containerCloseButton) != 0):
                print("Não foi possível pular a faixa. A música ficará muda por um tempo.")
                botaoFecharDialogo = driver.execute_script("return document.querySelector('#dialogCloseButton').querySelector('music-button').shadowRoot.querySelector('button')")
                botaoFecharDialogo.click()
                time.sleep(180) # Aguarda 3 minutos para poder tocar novamente (provavelmente tempo suficiente pra musica acabar)
            
            alterarVolume(Keys.UP, 10)


    # Filtro de palavras (se houver alguma dessas, a música é passada)
    palavrasProibidasLetra = ["danada", "safada", "bunda", "caralho", "carai", "porra", "fod", "porra", "puta", "gemid", "viado", "sexo", "transa", "buceta", "pau", "pica", "cerveja", "cigarro", "fuck", "dick", "bitch", "pussy"]
    palavrasProibidasTitulo = ["explicit"]

    tagTitulo = driver.find_elements(By.ID, "_31mvYpjWxr2CSCPbBhWS8f")
    if(len(tagTitulo) != 0):
        # Só vai checar se a música que está reproduzindo ainda não tiver sido checada
        if(titulo == None or tagTitulo[0].text.lower() != titulo):
            titulo = tagTitulo[0].text.lower()
            print("* Procurando por palavras proibidas na música "+str(titulo))
            palavraProibidaEncontrada = False

            # Checa o título
            for palavraProibida in palavrasProibidasTitulo:
                if(palavraProibida in titulo):
                    print("Uma palavra proibida foi encontrada no título. Essa faixa será pulada.")
                    pularFaixa()
                    palavraProibidaEncontrada = True
                    break
            
            if(palavraProibidaEncontrada == False):
                # Checa a letra
                containerLetra = driver.find_elements(By.CLASS_NAME, 'UM9lXLnqskf0yS8tO8zIO')
                if(len(containerLetra) != 0):

                    linhas = containerLetra[0].find_elements(By.TAG_NAME, 'li')
                    for linha in linhas:
                        for palavraProibida in palavrasProibidasLetra:
                            if(palavraProibida in linha.text.lower()):
                                print("Uma palavra proibida foi encontrada na letra. Essa faixa será pulada.")
                                pularFaixa()
                                palavraProibidaEncontrada = True
                                break   #  Break 2º for
                        if (palavraProibidaEncontrada == True):
                            break   # Break 1º for

            print("* Fim da busca por palavras proibidas")
        