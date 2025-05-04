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

1. **`Birch(n_clusters=3, threshold=0.07, branching_factor=100):`**  
   Tento riadok vytvorí inštanciu triedy `Birch` z knižnice `sklearn.cluster` a určuje, že chceme rozdeliť dáta do 3 klastrov.

   - `n_clusters=3`: Určuje počet klastrov, ktoré má algoritmus BIRCH nájsť (3 klastry vo vašom prípade).

   **Parametre:**
   - **`n_clusters=k:`**  
     Tento parameter určuje počet klastrov, ktoré algoritmus BIRCH má nájsť po vykonaní zoskupovania.  
     - `k`: Môže to byť akákoľvek hodnota, ktorá určuje požadovaný počet klastrov. Ak je hodnota `n_clusters=k`, algoritmus sa pokúsi rozdeliť dáta na `k` klastrov.  
     - Ak je `n_clusters` nastavené na `None`, algoritmus bude pokračovať v procesoch zoskupovania, až kým sa počet klastrov nestabilizuje podľa iných parametrov.

   - **`threshold=0.07:`**  
     `threshold` určuje maximálnu vzdialenosť, akú môže mať bod od centrálnej hodnoty mikroklastra (Centroidu) predtým, než bude priradený k novému mikroklastru.  
     - Tento parameter riadi, ako „tesne“ sa budú mikroklastre držať pohromade.  
     - Nižšia hodnota znamená prísnejšie kritériá na to, aby sa bod priradil k existujúcemu mikroklastru, čo môže viesť k väčšiemu počtu mikroklastrov.  
     - Vyššia hodnota znamená, že bod môže byť priradený k širšiemu rozsahu mikroklastrov, čím sa zníži počet mikroklastrov, ale môže to spôsobiť, že sa niektoré klastre budú miešať.

   - **`branching_factor=100:`**  
     `branching_factor` určuje maximálny počet podstromov, ktoré môže obsahovať každý uzol v CF Tree (Cluster Feature Tree), ktorý BIRCH používa na reprezentáciu klastrov.  
     - Vyššia hodnota umožňuje väčšie podstromy, čím sa znižuje počet uzlov a zjednodušuje hierarchia stromu.  
     - Nižšia hodnota spôsobí, že strom bude mať viac úrovní a uzlov, čo môže spomaliť výpočty, ale zvýši flexibilitu v spracovaní dát.

2. **`.fit(outlier_points):`**  
   Metóda `.fit()` aplikuje algoritmus BIRCH na naše dáta (`outlier_points`).

   - **Ako funguje algoritmus BIRCH:**
     - **Mikroklastre (Microclusters):** Algoritmus začína tým, že rozdelí dáta na malé mikroklastre. Každý mikroklaster je reprezentovaný centroidom a ďalšími štatistikami ako priemer a rozptyl.
     - **CF Tree (Cluster Feature Tree):** Potom vytvorí hierarchickú štruktúru známa ako CF Tree, ktorá efektívne uchováva informácie o mikroklastroch.
     - **Zoskupovanie:** Algoritmus postupne priraďuje mikroklastre do väčších klastrov a vytvára konečnú štruktúru klastrov na základe týchto agregovaných informácií.
     - **Iterácia:** Tento proces prebieha v iteráciách, kde algoritmus postupne zoskupuje mikroklastre do väčších, a to všetko za použitia hierarchickej štruktúry, ktorá optimalizuje výpočty.
   - **Výsledok:** Po dokončení `.fit()` má model BIRCH uložené priradenia bodov do klastrov a informácie o mikroklastroch a ich centroidoch.

3. **`labels = birch.labels_:`**  
   Po natrénovaní modelu obsahuje `birch.labels_` priradenia jednotlivých dátových bodov do klastrov.

   - `labels_`: Je to pole (zoznam), kde každá položka udáva, do ktorého klastru bol daný dátový bod zaradený. Napr. ak máte 10 bodov a `n_clusters=3`, pole `labels_` bude obsahovať hodnoty `0`, `1` alebo `2`, podľa toho, do ktorého z troch klastrov patrí daný bod.

---

### Zhrnutie:
- **`Birch(n_clusters=3):`** Inicializuje algoritmus BIRCH na rozdelenie dát do 3 klastrov.
- **`.fit(outlier_points):`** Spustí BIRCH algoritmus na vašich dátach a vykoná zoskupovanie pomocou mikroklastrov a CF Tree.
- **`birch.labels_:`** Vracia priradenia dátových bodov do klastrov (t. j. ktorý bod patrí do ktorého klastru).

---

## K-means

1. **`KMeans(n_clusters=k, random_state=0):`**
   - Tento riadok vytvorí inštanciu triedy `KMeans` z knižnice `sklearn.cluster` a určuje, že chceme rozdeliť dáta do `k` klastrov (v tomto prípade `k=3`).
   - `n_clusters=k`: Určuje počet klastrov, ktoré má algoritmus nájsť (3 klastry vo vašom prípade).
   - `random_state=0`: Zabezpečuje, že náhodná inicializácia centroidov bude reprodukovateľná – výsledky budú rovnaké pri každom spustení kódu.

2. **`.fit(outlier_points):`**
   - Metóda `.fit()` aplikuje K-means algoritmus na naše dáta (`outlier_points`).
   - **Ako funguje K-means algoritmus:**
     - **Náhodná inicializácia:** Začne náhodným výberom `k=3` počiatočných centroidov z vašich dátových bodov.
     - **Fáza priradenia:** Každý bod sa priradí k najbližšiemu centroidu (na základe euklidovskej vzdialenosti).
     - **Fáza aktualizácie:** Po priradení všetkých bodov sa centroidy prepočítajú ako priemer všetkých bodov v každom klastri.
     - **Iterácia:** Tento proces (priraďovanie bodov + prepočítanie centroidov) sa opakuje, až kým sa centroidy prestanú výrazne meniť (t. j. dosiahne sa konvergencia), alebo sa dosiahne maximálny počet iterácií.
   - **Výsledok:** Po dokončení `.fit()` má model (`kmeans`) uložené priradenia do klastrov aj súradnice centroidov.

3. **`labels = kmeans.labels_:`**
   - Po natrénovaní modelu obsahuje `kmeans.labels_` priradenia jednotlivých dátových bodov do klastrov.
   - `labels_`: Je to pole (zoznam), kde každá položka udáva, do ktorého klastru bol daný dátový bod zaradený. Napr. ak máte 10 bodov a `k=3`, pole `labels_` bude obsahovať hodnoty `0`, `1` alebo `2`, podľa toho, do ktorého z troch klastrov patrí daný bod.

---

### Zhrnutie:
- **`KMeans(n_clusters=k):`** Inicializuje K-means algoritmus na rozdelenie dát do 3 klastrov.
- **`.fit(outlier_points):`** Spustí K-means na vašich dátach a vykoná zoskupovanie.
- **`kmeans.labels_:`** Vracia priradenia dátových bodov do klastrov (t. j. ktorý bod patrí do ktorého klastru).

