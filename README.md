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
  K-means je iteratívny algoritmus používaný na klastrovanie dát. Jeho cieľom je rozdeliť \( n \) dátových bodov do \( K \) zhlukov (klastrov), kde body v rámci jedného zhluku sú čo najbližšie k svojmu centroidu (stredu zhluku). Algoritmus funguje na princípe opakovaného priraďovania bodov k najbližšiemu centroidu a aktualizovania polôh centroidov, až kým sa priradenie bodov nezmení alebo sa nedosiahne stanovený počet iterácií.

- **Hlavné premenné:**
    - **\( K \)** – počet zhlukov (určuješ ty).
    - **\( X = \{x_1, x_2, ..., x_n\} \)** – množina vstupných dátových bodov.
    - **\( \mu_1, \mu_2, ..., \mu_K \)** – centroidy (stredy zhlukov).
    - **\( C(i) \in \{1, ..., K\} \)** – priradenie dátového bodu \( x_i \) ku konkrétnemu zhluku.

- **Algoritmus (iteratívny proces):**
    1. **Inicializácia centier zhlukov:**  
       Vyber náhodne \( K \) dátových bodov ako počiatočné centroidy \( \mu_1, ..., \mu_K \).
    
    2. **Priraďovanie bodov ku zhlukom:**  
       Pre každý bod \( x_i \) nájdi najbližší centroid \( \mu_j \), podľa euklidovskej vzdialenosti:
       $$
       C(i) = \arg\min_{j \in \{1, ..., K\}} \left\| x_i - \mu_j \right\|^2
       $$

    3. **Aktualizácia centroidov:**  
       Pre každý zhluk \( j \), vypočítaj nový centroid ako priemer všetkých bodov priradených do tohto zhluku:
       $$
       \mu_j = \frac{1}{|S_j|} \sum_{x_i \in S_j} x_i
       $$
       kde \( S_j = \{ x_i : C(i) = j \} \) je množina bodov priradených k zhluku \( j \).

    4. **Opakovanie:**  
       Kroky 2 a 3 opakuj, až kým sa priradenie bodov nezmení, alebo sa nedosiahne stanovený počet iterácií.

- **Výhody:**
    - Jednoduchý a rýchly na menších a stredne veľkých datasetoch.
    - Intuitívne výsledky pre dobre oddelené zhluky.
    - Relatívne jednoduchá implementácia.

- **Nevýhody:**
    - Musíš vopred určiť počet zhlukov \( K \).
    - Citlivý na počiatočné hodnoty centroidov (môže to viesť k rôznym výsledkom pri rôznych inicializáciách).
    - Citlivý na odľahlé hodnoty (outliers).
    - Predpokladá, že zhluky majú guľový tvar a rovnakú veľkosť, čo nie je vždy pravda.

- **Použitie v kóde:**  
  Ak chceš použiť **K-means** v Python-e, môžeš využiť knižnicu `scikit-learn`. Tu je ukážka kódu:

  ```python
  from sklearn.cluster import KMeans

  # Predpokladáme, že máš vstupné dáta v premennej `data`
  kmeans = KMeans(n_clusters=K, random_state=0).fit(data)

  # Získanie priradení bodov k zhlukom
  labels = kmeans.labels_

  # Získanie centroidov
  centroids = kmeans.cluster_centers_
