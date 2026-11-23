from collections import deque
import config as CONFIG
import math

def BFS(G, s):
    print("Lancement de l'algo")
    events = []
    visited = []
    file = deque()
    coul = {}
    for u in G:
        coul[u] = "blanc"
    
    file.append(s)
    visited.append(s)
    coul[s] = "gris"
    events.append([("node", s, CONFIG.DECOUVERTE)])
    
    
    while len(file) != 0:
        u = file[0]
        events.append([("node", u, CONFIG.CURRENT_NODE)])
        for v in G[u]:
            
            if coul[v] == "blanc":
                file.append(v)
                coul[v] = "gris"
                visited.append(v)
            events.append([("edge", (u,v), CONFIG.DECOUVERTE),("node", v, CONFIG.DECOUVERTE)])
                
                
                
        file.popleft()
        coul[u] = "noir"
        events.append([("node", u, CONFIG.END)])
    print(visited)
    print(events)
    return events
            
            

def proc_DFS_rec(G,u,coul,events,visited):
    
    coul[u] = "gris"
    events.append([("node", u, CONFIG.CURRENT_NODE)])
    visited.append(u)
    for v in G[u]:
        events.append([("edge", (u,v), CONFIG.DECOUVERTE),("node", v, CONFIG.DECOUVERTE)])
        if coul[v] == "blanc":
            proc_DFS_rec(G,v,coul,events, visited)
            events.append([("node", u, CONFIG.CURRENT_NODE)])
    coul[u] = "noir"
    events.append([("node", u, CONFIG.END)])
    return events

def DFS(G,s):
    events = []
    visited = []
    coul = {}
    for u in G:
        coul[u] = "blanc"
    events.append([("node", s, CONFIG.DECOUVERTE)])
    return proc_DFS_rec(G,s, coul,events,visited)


def Dijkstra(G,s):
    poids = G[1]
    G = G[0]
    print("Forme de G : ", G)
    coul = {}
    dist = {}
    events = []
    Q = deque()
    for u in G:
        coul[u] = "blanc"
        dist[u] = math.inf
    
    
    
    dist[s] = 0
    events.append([("node", s, CONFIG.DECOUVERTE),("weight", s, CONFIG.DECOUVERTE, dist[s])])
    Q.append(s)
    coul[s] = "gris"
    while len(Q) != 0:
        u = next((n for n in Q if dist[n] == min(dist[n] for n in Q)), None)
        events.append([("node", u, CONFIG.CURRENT_NODE)])
        Q.remove(u)
        coul[u] = "noir"
        events.append([("weight", u, CONFIG.END, dist[u])])
        for v in G[u]:
            if dist[u] + poids[(u,v)] < dist[v]:
                dist[v] = dist[u] + poids[(u,v)]
                
                if coul[v] == "blanc":
                    Q.append(v)
                    coul[v] = "gris"
                    events.append([("edge", (u,v), CONFIG.DECOUVERTE),("node", v, CONFIG.DECOUVERTE),("weight", v, CONFIG.DECOUVERTE, dist[v])])
                else:
                    events.append([("edge", (u,v), CONFIG.DECOUVERTE),("weight", v, CONFIG.MAJ, dist[v])])
        events.append([("node", u, CONFIG.END)])
    return events



def Bellman_ford(G,s):
    poids = G[1]
    G = G[0]
    dist = {}
    events = []
    Q = deque()
    for u in G:
        dist[u] = math.inf
    dist[s] = 0
    events.append([("weight", s, CONFIG.MAJ, dist[s])])
    events.append([("weight", s, CONFIG.DEFAULT, dist[s])]) 
    for k in range(1,len(G)):
        events.append([("Up_passe", None, f"Passe {k}")])
        for (u,v) in poids:
            if dist[v] > dist[u] + poids[(u,v)]:
                dist[v] = dist[u] + poids[(u,v)]
                events.append([("node", u, CONFIG.CURRENT_NODE),("edge", (u,v), CONFIG.MAJ),("weight", v, CONFIG.MAJ, dist[v])])
                events.append([("node", u, CONFIG.DEFAULT),("edge", (u,v), CONFIG.DEFAULT),("weight", v, CONFIG.DEFAULT_W, dist[v])])
                
            else:
                events.append([("edge", (u,v), CONFIG.REJET)])
                events.append([("edge", (u,v), CONFIG.DEFAULT)])
    events.append([("Up_passe", None, "Passe de vérification")])
    for (u, v) in poids:
        if dist[u] == math.inf:
            continue
        if dist[v] > dist[u] + poids[(u, v)]:
            events.append([("edge", (u, v), CONFIG.CYCLE), ("node", v, CONFIG.CYCLE)])
            events.append([("Up_passe", None, "Cycle négatif détecté")])
            break
        events.append([("edge", (u, v), CONFIG.CURRENT_EDGE)])
        events.append([("edge", (u, v), CONFIG.DEFAULT)])
    return events

def Floyd_Warshall(G,s):
    print("NULL")

def Prim(G,s):
    poids = G[1]
    G = G[0]
    dist = {}
    coul = {}
    pere = {}
    events = []
    Q = deque()
    for u in G:
        coul[u] = "blanc"
        dist[u] = math.inf
        pere[u] = None
    dist[s] = 0
    for node in G.keys():
        Q.append(node)
    while len(Q) != 0:
        u = next((n for n in Q if dist[n] == min(dist[n] for n in Q)), None)
        
        events.append([("node", u, CONFIG.MAJ),("edge", (u,pere[u]), CONFIG.MAJ)])
        
        Q.remove(u)
        coul[u] = "noir"
        for v in G[u]:
            
            if coul[v] == "blanc" and poids[(u,v)] < dist[v]:
                dist[v] = poids[(u,v)]
                events.append([("edge", (pere[v],v), CONFIG.DEFAULT)])
                pere[v] = u
                events.append([("edge", (u,v), CONFIG.DECOUVERTE)])
                
    print(pere)
    print(events)
    return events
    
    




def find(F,u):
    if F[u] != u:
        F[u] = find(F,F[u])
    return F[u]

def union(F, u, v):
    F[find(F,u)] = find(F,v)
    


def Kruskal(G):
    poids = G[1]
    G = G[0]
    F = {u: u for u in G}
    A = []
    events = []
    poids = sorted((w, u, v) for (u, v), w in poids.items() if u < v)
    w,u,v = poids[0]
    events.append([("edge", (u,v), CONFIG.DECOUVERTE)])
    for i in range(0,len(poids)):
        w,u,v = poids[i]
        
        
        if find(F,u) != find(F,v):
            if i + 1 >= len(poids): 
                events.append([("node", u, CONFIG.MAJ),("edge", (u,v), CONFIG.MAJ)])
                continue
            wp,up,vp = poids[i+1]
            events.append([("node", u, CONFIG.MAJ),
                           ("node", v, CONFIG.MAJ),
                           ("edge", (u,v), CONFIG.MAJ),
                           ("edge", (up,vp), CONFIG.DECOUVERTE)])
            A.append((u,v))
            union(F,u,v)
        else:
            
            
            if i + 1 >= len(poids):      
                events.append([("edge", (u,v), CONFIG.REJET)])
                events.append([("edge", (u,v), CONFIG.DEFAULT)])
                continue
            wp,up,vp = poids[i+1]
            
            events.append([("edge", (u,v), CONFIG.REJET),("edge", (up,vp), CONFIG.DECOUVERTE)])
            events.append([("edge", (u,v), CONFIG.DEFAULT)])
    print(A)
    return events
    