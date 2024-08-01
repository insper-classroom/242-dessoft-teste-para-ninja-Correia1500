import pygame
import sys
from gerador import gera_numeros
import time

# Inicializando o Pygame
pygame.init()

# Configurando a tela (largura = 800, altura = 600)
tela = pygame.display.set_mode((800, 600))

# Definindo o título da janela
pygame.display.set_caption("Jogo dos Quadrados")

# Definindo cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CINZA = (128, 128, 128)
PRETO = (0, 0, 0)

# Definindo dimensões e posições dos quadrados
largura_plataforma = 800
altura_plataforma = 100
plataforma_x = (800 - largura_plataforma) // 2
plataforma_y = 500

tamanho_quadrado = 100
quadrado_x = (800 - tamanho_quadrado) // 2
quadrado_y_top = plataforma_y - tamanho_quadrado * 3

# Função para desenhar o texto
def desenha_texto(texto, fonte, cor, superficie, x, y):
    obj_texto = fonte.render(texto, True, cor)
    superficie.blit(obj_texto, (x, y))

# Tela inicial
def tela_inicial(fonte_larga):
    tela.fill(BRANCO)
    desenha_texto('Jogar', fonte_larga, PRETO, tela, tela.get_width() // 2 - 50, tela.get_height() // 2 - 50)
    pygame.display.flip()
    espera_por_clique()

def espera_por_clique():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

# Função principal do jogo
def main():
    vida = 3
    resposta_correta = 0
    comeca_tempo = time.time()

    # Fonte para desenhar os números
    fonte = pygame.font.Font(None, 36)
    fonte_larga = pygame.font.Font(None, 44)

    tela_inicial(fonte_larga)

    # Definindo um evento de tempo que será acionado a cada segundo
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    while True:
        tempo_decorrido = time.time() - comeca_tempo
        if tempo_decorrido > 60:
            tela_final(resposta_correta, fonte_larga)
            break

        numeros = gera_numeros()
        quadrados = [pygame.Rect(quadrado_x, quadrado_y_top, tamanho_quadrado, tamanho_quadrado),
                     pygame.Rect(quadrado_x, quadrado_y_top + tamanho_quadrado, tamanho_quadrado, tamanho_quadrado),
                     pygame.Rect(quadrado_x, quadrado_y_top + 2 * tamanho_quadrado, tamanho_quadrado, tamanho_quadrado)]
        cores = [VERMELHO, VERDE, AZUL]
        quadrado_clicado = None

        jogo_rodando = True
        while jogo_rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = evento.pos
                    for i, quadrado in enumerate(quadrados):
                        if quadrado.collidepoint(mouse_x, mouse_y):
                            numero_selecionado = numeros[i]
                            numeros_restantes = [numeros[j] for j in range(3) if j != i]
                            if numero_selecionado == numeros[3]:
                                mensagem = "Errado!"
                                vida -= 1
                            elif sum(numeros_restantes) == numeros[3]:
                                mensagem = "Certo!"
                                resposta_correta += 1
                            else:
                                mensagem = "Errado!"
                                vida -= 1
                            quadrado_clicado = quadrado
                            jogo_rodando = False
                            break
                elif evento.type == pygame.USEREVENT:
                    tempo_decorrido = time.time() - comeca_tempo

            # Preenchendo a tela com a cor branca
            tela.fill(BRANCO)

            # Desenhando a plataforma
            pygame.draw.rect(tela, CINZA, (plataforma_x, plataforma_y, largura_plataforma, altura_plataforma))

            # Desenhando os quadrados empilhados e os números
            for i, quadrado in enumerate(quadrados):
                pygame.draw.rect(tela, cores[i], quadrado)
                texto = fonte.render(str(numeros[i]), True, PRETO)
                tela.blit(texto, (quadrado.x + (tamanho_quadrado - texto.get_width()) // 2, quadrado.y + (tamanho_quadrado - texto.get_height()) // 2))

            # Desenhando o quarto número no canto superior esquerdo da tela
            texto4 = fonte.render(str(numeros[3]), True, PRETO)
            tela.blit(texto4, (10, 10))

            # Desenhando o tempo restante e vidas
            desenha_texto(f'Tempo restante: {60 - int(tempo_decorrido)}', fonte, PRETO, tela, 550, 10)
            desenha_texto(f'Vidas: {vida}', fonte, PRETO, tela, 10, 50)

            pygame.display.flip()

        # Exibir mensagem "Certo!" ou "Errado!"
        tela.fill(BRANCO)
        if quadrado_clicado:
            desenha_texto(mensagem, fonte_larga, PRETO, tela, quadrado_clicado.x, quadrado_clicado.y)
        pygame.display.flip()
        pygame.time.wait(1000)

        if vida <= 0:
            tela_final(resposta_correta, fonte_larga)
            break

def tela_final(resposta_correta, fonte_larga):
    tela.fill(BRANCO)
    desenha_texto(f'Fim de jogo! Respostas corretas: {resposta_correta}', fonte_larga, PRETO, tela, 150, 250)
    pygame.display.flip()
    pygame.time.wait(3000)

if __name__ == '__main__':
    main()
