from Gener_Graphe import Create_Graphe
import random
import Algos



def main():
    
    nbNodes = int(input("Nombre des noeuds : "))
    oriented = input("Orienté [y/n] : ") == "y"
    weighted = input("Pondéré [y/n] : ") == "y"
    if weighted:
        neg_weighted = input("Poids négatifs [y/n] : ") == "y"
    else:
        neg_weighted = False
    
    g = Create_Graphe("BFS",nbNodes,oriented,weighted,neg_weighted)
    g.gener_graphe()
    
    
    
    
    print("\n1. BFS")
    print("2. DFS")
    print("3. Dijkstra")
    print("4. Bellman-ford")
    print("5. Floyd-Warshall")
    print("6. Prim")
    print("7. Kruskal\n")
    
    _Algos = [Algos.BFS,
              Algos.DFS,
              Algos.Dijkstra,
              Algos.Bellman_ford,
              Algos.Floyd_Warshall,
              Algos.Prim,
                  #Algos.Kruskal
                  ]
    Algo = _Algos[int(input(">> "))-1]
    s = input("Choisissez un sommet : ").upper()
    
    if Algo == Algos.Dijkstra or Algo == Algos.Bellman_ford or Algo == Algos.Prim:
        etapes = Algo([g.edges,g.weight], s)
    else:
        etapes = Algo(g.edges, s)
    
    g.launch(etapes)
    
    

if __name__ == "__main__":
    main()