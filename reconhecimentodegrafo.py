# Rodrigo Luís Zimmermann
import numpy as np

class Grafo:

  matriz = np.array([[0, 1, 1, 0],
                     [1, 0, 0, 1],
                     [1, 0, 0, 1],
                     [0, 1, 1, 0]])

  if np.array_equal(matriz, matriz.T):
    isDigrafo = False
  else:
    isDigrafo = True

  def tipoDoGrafo(self):
      print("A)")
      self.isDirigido()
      self.isMultigrafoOuSimples()
      self.isRegularAndCompleto()
      self.isNulo()
      self.isBipartido()
      
  def isDirigido(self):
      if self.isDigrafo:
          print("Dirigido")
      else:
          print("Não é Dirigido")
          
  def isMultigrafoOuSimples(self):
      isMulti = False
      for i in range(len(self.matriz)):
          if self.matriz[i][i] > 0:
              isMulti = True
              break
          for j in range(len(self.matriz)):
              if self.matriz[i][j] > 1:
                  isMulti = True
                  break
      if isMulti:
          print("Multigrafo")
      else:
          print("Simples")

  def isRegularAndCompleto(self):
    graus = np.sum(self.matriz, axis=0)
    resto = len(graus) * (len(graus) + 1) % 2
    if np.all(graus == graus[0]):
      print("Regular")
      if resto == 0:
        print("Completo")
    else:
      print("Não é regular")
      print("Não é completo")

  def isNulo(self):
      if any(self.matriz.flatten()):
          print("Não é Nulo")
      else:
          print("Nulo")

  def isBipartido(self):
    isBipartido = True
    num_vertices = len(self.matriz)
    cores = [-1] * num_vertices

    if self.isDigrafo:
      cores[0] = 0
      fila = [0]
      # Executa a busca em largura
      while fila:
          v = fila.pop(0)
          for i in range(num_vertices):
              if self.matriz[v][i] == 1: # Verifica se o vértice i é adjacente a v
                  if cores[i] == -1: # Se o vértice i não tiver sido colorido ainda
                      cores[i] = 1 - cores[v] # Atribui a cor oposta à do vértice anterior
                      fila.append(i) # Adiciona o vértice i na fila
                  elif cores[i] == cores[v]: # Se o vértice i tiver a mesma cor que o vértice anterior
                      isBipartido = False
                      break
    else:
      for i in range(num_vertices):
          if cores[i] == -1:
              cores[i] = 0
              fila = [i]
              while fila:
                  v = fila.pop(0)
                  for j in range(num_vertices):
                      if self.matriz[v][j] == 1:
                          if cores[j] == -1:
                              cores[j] = 1 - cores[v]
                              fila.append(j)
                          elif cores[j] == cores[v]:
                              isBipartido = False
                              break
    if isBipartido:
      print("Bipartido")
    else:
      print("Não é Bipartido")

  def arestasDoGrafo(self):
    print("\nB)")
    if self.isDigrafo:
      num_arestas = int(np.sum(self.matriz))
    else:
      num_arestas = int(np.sum(self.matriz) / 2)
      
    print("Quantidade: " + str(num_arestas) + " e " + self.conjuntoArestas())

  def conjuntoArestas(self):
      arestas = set()
      for i in range(len(self.matriz)):
          for j in range(len(self.matriz)):
              if self.matriz[i][j] > 0:
                  arestas.add((i+1, j+1))
      return "Conjunto:" + str(arestas)

  def grausDoVertice(self):
    print("\nC)")
    graus = [sum(linha) for linha in self.matriz]
    print("Grau: " + str(graus) + " e Sequência: " + str(sorted(graus)))

executa = Grafo();
executa.tipoDoGrafo();
executa.arestasDoGrafo();
executa.grausDoVertice();