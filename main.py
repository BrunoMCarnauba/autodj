from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

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

# Configura o selenium / driver do chrome
# FALTA FAZER ISSO: clonar data-profile? https://forum.katalon.com/t/user-data-directory-is-already-in-use/40266/2
caminhoDriver = r"chrome_driver/chromedriver.exe"
opcoes = Options()
opcoes.add_argument("user-data-dir=C:/Users/Bruno/AppData/Local/Google/Chrome/User Data")
opcoes.add_argument("--profile-directory=Default")
opcoes.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=caminhoDriver, chrome_options=opcoes)

# Função para ajustar o volume do amazon music
def alterarVolume(key, diferencaVolume):
    # Aguarda o #volume-button aparecer
    WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.ID, "volume-button"))
    )

    volumeRange = driver.find_elements(By.CLASS_NAME, "_2A37HSwUCzCv8zFDLwOtsS")
    # * Se o range não estiver aparecendo então faz aparecer
    if(len(volumeRange) == 0):
        containerVolume = driver.execute_script("return document.querySelector('#volume-button')")
        botaoVolume = driver.execute_script("return document.querySelector('#volume-button').shadowRoot.querySelector('button')")
        driver.implicitly_wait(10)
        ActionChains(driver).move_to_element(containerVolume).click(botaoVolume).perform()

    volumeRange = driver.find_element(By.CLASS_NAME, "_2A37HSwUCzCv8zFDLwOtsS").find_element(By.TAG_NAME, "input")
    for i in range(diferencaVolume):
        volumeRange.send_keys(key)
        time.sleep(0.4)

# Entra na pasta da amazon e aguarda o login
driver.get(r"https://www.amazon.com.br/ap/signin?clientContext=132-6012886-8774842&openid.return_to=https%3A%2F%2Fmusic.amazon.com.br%2F&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_webamp_br&openid.mode=checkid_setup&marketPlaceId=A2Q3Y263D00KWC&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=amzn_cpweb&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&siteState=clientContext%3D138-1406355-6104023%2CsourceUrl%3Dhttps%253A%252F%252Fmusic.amazon.com.br%252F%2Csignature%3Dnull")
print("Aperte ENTER após fazer o login")
input()

# FALTA FAZER: Se tiver aparecido o diálogo do Amazon Music Unlimited
# Se id dialogHeader (é um h1) tiver aparecido com o texto "Cadastre-se no Amazon Music Unlimited", então executar o comando abaixo
# clicar no botão document.querySelector('music-button').shadowRoot.querySelector('button')
# Se não, apenas continuar o código.

# Inicia a reprodução
listaPlaylists = Playlist.listar()
playlistAtual = 0
while(playlistAtual < len(listaPlaylists)):
    # Se já estiver tocando alguma playlist, então fazer a transição para tocar a próxima
    if(playlistAtual != 0):
        print("Transição para a próxima playlist")
        # Fecha o player se estiver aberto
        containerVoltar = driver.find_elements(By.ID, 'npvCloseButton')
        if(len(containerVoltar) != 0):
            botaoVoltar = driver.execute_script("return document.querySelector('#npvCloseButton').shadowRoot.querySelector('button')")
            driver.implicitly_wait(10)
            ActionChains(driver).move_to_element(containerVoltar[0]).click(botaoVoltar).perform()

        # Diminuindo volume
        alterarVolume(Keys.DOWN, 8)
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

    time.sleep(10)

    # Reproduz a playlist
    # * Como localizar elemento com shadow-root: https://stackoverflow.com/questions/65445170/cant-locate-elments-within-shadow-root-open-using-python-selenium/65452620#65452620 
    # * Método 02 (inclusive também é no amazon music): https://stackoverflow.com/questions/69585279/unable-to-click-on-shadow-root-element-using-selenium
    containerMusica = driver.execute_script("return document.querySelector('music-shoveler').querySelector('music-horizontal-item')")
    botaoPlay = driver.execute_script("return document.querySelector('music-shoveler').querySelector('music-horizontal-item').shadowRoot.querySelector('.action-icon-button').shadowRoot.querySelector('button')")
    # Para ser capaz de clicar no elemento que não está visível
    driver.implicitly_wait(10)
    ActionChains(driver).move_to_element(containerMusica).click(botaoPlay).perform()

    # Aumenta o volume
    alterarVolume(Keys.UP, 10)

    # Aguarda o tempo para a próxima playlist
    time.sleep((listaPlaylists[playlistAtual].minutosReproducao * 60))
    playlistAtual = playlistAtual + 1
        
    print("Fim da playlist")
