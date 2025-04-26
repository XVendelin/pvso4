# Klasifikácia bodového mraku pomocou BIRCH alebo K-means

Tento Python skript načíta 3D bodový mrak zo súboru `.ply`, vyhľadá a odstráni najväčšiu rovinu (napr. zem, stenu) a zvyšné body rozdelí do klastrov pomocou jedného z dvoch algoritmov: **BIRCH** alebo **K-means**. Výsledné klastre sú vizualizované rôznymi farbami.

## Čo skript robí

1. **Načíta bodový mrak** zo súboru.
2. **Segmentuje najväčšiu rovinu** pomocou RANSAC algoritmu.
3. **Oddelí zvyšné body** (outliery) od roviny.
4. **Odstráni NaN hodnoty** z dát.
5. **Klastruje outliery** pomocou vybraného algoritmu (BIRCH alebo K-means).
6. **Vizualizuje výsledok** v 3D okne.

---

## BIRCH

- **Čo je BIRCH?**  
  BIRCH (Balanced Iterative Reducing and Clustering using Hierarchies) je algoritmus vhodný pre veľmi veľké datasety. Pracuje rýchlo a efektívne tým, že buduje kompaktnú hierarchickú štruktúru bodov už počas načítania dát.

- **Výhody:**  
  - Lepšie škáluje na milióny bodov.
  - Pamäťovo úspornejší.
  - Automaticky agreguje podobné body do clusterov.

- **Použitie v kóde:**  
  Predvolený algoritmus je BIRCH. Klastruje outliery podľa počtu klastrov `k`:
  
  ```python
  birch = Birch(n_clusters=k, threshold=0.5, branching_factor=100)
  labels = birch.fit_predict(outlier_points)

---

## K-means

- **Čo je K-means?**
    K-means je klasický a veľmi rozšírený algoritmus na klastrovanie dát. Cieľom je rozdeliť body do k skupín tak, aby boli čo najbližšie k svojmu centroidu (stredu klastra). Algoritmus opakovane priraďuje body k najbližšiemu centroidu a aktualizuje polohy centroidov, až kým sa nezmení priradenie bodov.

- **Výhody:**
    - Extrémne rýchly pri menších a stredne veľkých datasetoch.
    - Jednoduchá implementácia a použitie.
    - Vhodný pre dáta, kde sú klastre približne guľovité a rovnakých veľkostí.

- **Nevýhody:**
    - Menej efektívny pri veľkých a veľmi nerovnomerných datasetoch.
    - Musí sa vopred určiť počet klastrov k.

- **Použitie v kóde:**
    Ak chceš použiť K-means namiesto BIRCH, stačí odkomentovať tieto riadky:
    ```python
    from sklearn.cluster import KMeans

    kmeans = KMeans(n_clusters=k, random_state=0).fit(outlier_points)
    labels = kmeans.labels_

---