from utils import *
from random import randint

if __name__ == "__main__":
    # Heurística Definition
    def heuristica(estadoAtual, estadoFinal):
        return abs(estadoAtual[0] - estadoFinal[0]) + abs(estadoAtual[1] - estadoFinal[1])
         # 0 é a primeira coordenada e o 1 é a segunda

    def heuristica2(estadoAtual, guardas):
        valorh2 = min([heuristica(estadoAtual, guarda) for guarda in guardas])
        if valorh2 != 0:
            return 1/valorh2
        else:
            return 0

    # A* Definition
    def search(estadoInicial, estadoFinal, bloqueios, guardas, heuristica, heuristica2):
        estadoAtual = estadoInicial
        listaFechada = []
        listaAberta = []

        # primeiro nó da árvore
        custo_G = 0
        heuristica_H = heuristica(estadoAtual, estadoFinal) + heuristica2(estadoAtual, guardas)
        total_F = custo_G + heuristica_H
        novo_no = No(estadoAtual,total_F, custo_G, heuristica_H, None)
        listaAberta.append(novo_no)

        # busca
        while estadoAtual != estadoFinal:
            listaExpansao = getAdjacentes(estadoAtual, listaAberta, listaFechada, bloqueios)
            print("Adjacentes válidos:", listaExpansao)
            listaAberta = abrirLista(listaExpansao, estadoInicial, estadoFinal, estadoAtual, listaAberta, listaFechada, heuristica, heuristica2, guardas)
            # fechar primeiro nó da listaAberta
            no = listaAberta[0]
            listaFechada.append(no)
            listaAberta.remove(no)
            listaAberta = reordenarLista(listaAberta)

            # mudar estado se ainda tiver listaAberta
            if len(listaAberta) != 0:
                estadoAtual = listaAberta[0].estado

        # fim da busca
        listaFechada.append(listaAberta[0])
        return melhorCaminho(estadoAtual, estadoInicial, listaFechada)

    # Game config
    def blockConfig():
        qtdbloqueios = randint(3, 6) #mudar no relatorio
        #print("Quantidade de bloqueios: ", qtdbloqueios)
        cordbloqueios_set = []
        while len(cordbloqueios_set) < qtdbloqueios:
            x, y = 6, 0
            while (x, y) == (6, 0):
                x, y = randint(0, 6), randint(0, 6)
                cordbloqueios_set.append((x, y))
        bloqueios = cordbloqueios_set
        print("Bloqueios: ", bloqueios)
        return bloqueios

    def guardaConfig():
        qtdguardas = randint(2, 3)
        cordguarda_set = []
        while len(cordguarda_set) < qtdguardas:
            x, y = 6, 0
            while (x, y) == (6, 0):
                x, y = randint(0, 6), randint(0, 6)
                cordguarda_set.append((x, y))
        # cordguarda_set.add((1, 2)) #depois apaga
        guardas = cordguarda_set
        print("Guardas: ", guardas)
        return guardas

    def estFinalConfig():
        nosAbertosFinal = []
        while nosAbertosFinal == []:
            xfinal, yfinal = randint(0, 6), randint(0, 6)
            estadoFinal = (xfinal, yfinal)
            nosAbertosFinal = todosAdjacentesValidos(estadoFinal, bloqueios)
            # print('Gerarando um novo estado final', estadoFinal)
            print("Estado Objetivo", estadoFinal)
        return estadoFinal

    def estInicConfig():
        foi_preso = False
        print("Digite as coordenadas [separadas por uma virgula]: \n")
        x, y = input().split(',')
        x, y = int(x), int(y)
        estadoInicial = (x, y)

        if estadoInicial in bloqueios:
            print("O estado inicial escolhido é invalido(tentou inserir em um bloqueio)")
            estInicConfig()
        #arrumar aqui, pq ele n ta considerando
        elif estadoInicial == estadoFinal:
            print("O estado inicial escolhido é o estado final, ganhou automaticamente a rodada")
            estInicConfig()
        elif estadoInicial in guardas:
            print("O estado inicial escolhido está em um guarda, perdeu automaticamente a rodada")
            estInicConfig()
        else:
            # Run

            caminho = search(estadoInicial, estadoFinal, bloqueios, guardas, heuristica, heuristica2)

            # Results
            print("Caminho: ", caminho)
            print("Guardas: ", guardas)
            for guarda in guardas:
                if guarda in caminho:
                    print("Ronaldinho foi preso")
                    foi_preso = True
                break

            for estado in caminho:
                valorFnTotal = heuristica(estado, estadoFinal) + heuristica2(estado, guardas)
                print('Estado:', estado, 'F(n):', valorFnTotal)
                #o valor a h2(n) nao fica 0 no objetivo pois é em relacao a distancia dos guardas
            if not foi_preso:
                print('Ronaldinho conseguiu driblar os guardas da prisão!')
            print("Quantidade de Movimentos:", len(caminho) - 1)

    for c in range(3):
        print("-----------------------------------------------------------")
        print("-----------------------------------------------------------")
        print("Rodada:", c)
        bloqueios = blockConfig()
        guardas = guardaConfig()
        estadoFinal = estFinalConfig()
        estInicConfig()

