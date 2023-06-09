# Using Isolation Forest as a Novelty Detection tool - work title

## Abstract
- téma
- toto jsme udělali
- co řešíme (řešíme problem hledání clusterů dat, ne problem nějakeho algoritmu)
- takto
- takto jsme to otestovali
- toto je výsledek
## Introduction
- start with lots of refs
- describe the problem
- our main goal was to
- general -> specific (describe problem as a whole, then why the problems occurs, then why is it a problem for us, technical details, env. variables)
- constribution
- **toto až nakonec až budeme vědět co vlastně fungovalo**
- **here we describe the domain!! - aneb jak ta data vypadají - co je cílem hlavně vysvětlit že chceme cluster anomalii ne jen anomalie**
 

## Methods

The very first task is to thoroughly analyze the domain of the given problem.
The inappropriate choice of the selected solution could lead to undesirable results.
Having the problem already described, we are now able to analyze and establish a learning process. 

Using the data domain knowledge, some constraints usually arise.
As described in the introductory section, we expect the sensors to produce linear-like data, with minor deviations within the *y* axis.
These deviations do not follow any specific pattern and are completely random.
However, the errors report some kind of observable behavior.
This is usually the case when performing cluster analysis.
The main constraint that is crucial for this task is the cluster forming pattern.
The task could become straightforward if we divide it into subordinate tasks.
First of them is to use the knowledge to separate non-anomalies (not yet clusters).
Doing so, the data that is left are anomalies-only where the task of finding anomaly clusters only becomes less challenging. 

The most straightforward solution when trying to find anomalies in above-shown data would be to use some kind of statistical method that would split the data in a certain ratio.
Figure X shows the mean (straight line) of the given data. 

![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/code/figures/mean_great_colored.svg) 
> Figure X - Mean of the given dataset with anomalies.

Although this may look positive on the first glance, several problems arise.
The initial one is with the automated distinction.
When the dataset is polluted with anomalies in close to 1:1 ratio, even for human it is close to impossible to differentiate anomalies and regular observation.
The second problem brings up when anomalies are not present at all, making mean method unusable.
Figure X shows the mean method when used on the dataset polluted by very little anomalies.
Obviously, if the dataset contained no anomalies at all, the result would become even more deficient.

![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/code/figures/mean_wrong_colored.svg) 
> Figure X - Mean of the given dataset with little to zero anomalies.



One could easily argue that there is an option of using pure clustering algorithms (e.g. ([DBScan](doi/10.5555/3001460.3001507)).
This, however, leads to unpleasant outcome.
Such algorithms tend to view the data as a cluster-only data, despite it being irrelevant in cluster regards.
Figure X shows the performance of the DBScan algorithm on previously non-processed data, where different colors represent different clusters.
Even though the algorithm did find some clusters, it would be demanding to differentiate and find the one with anomalies.
Moreover, due to the gap in the measurement, the DBScan incorrectly split the regular observations into two clusters.
This brings up the idea of algorithm cross-cooperation.
Therefore, our proposed solution separates the anomalies first and then tries to find a cluster amongst them.

![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/code/figures/DBScanGap.svg) 
> Figure X - DBScan performance

Traditional approaches for anomaly separation consist of either novelty detection or outlier detection.
Novelty detection is an anomaly detection mechanism, where we search for unusual observations, which are discovered due to their differences from the training data.
Novelty detection is a semi-supervised anomaly-detection technique, whereas outlier detection uses unsupervised methods.
This a crucial distinction, due to a fact that whereas the outlier detection is usually presented with data containing both anomalies and regular observation, it then uses mathematical models that try to make distinction between them, novelty detection on the other hand is usually presented data with little to zero anomalies (the proportion of anomalies in the dataset is called a contamination) and later, when conferred with an anomalous observation, it makes a decision.
This means, that if the dataset contains observations which look like anomalies but are still valid, the performance of unsupervised outlier detection in such case is usually unsatisfactory. 

- [ ] TODO: TADY NAPIŠ JAKOBY ŽE ISOLATION FOREST NENI from scratch novelty a vysvětli proč se to asi obecně traduje, ale ukážeme později že může být

### Isolation Forest
Isolation Forest ([1](https://doi.org/10.1016/j.engappai.2022.105730 "article 1"), [2](https://doi.org/10.1016/j.patcog.2023.109334 "article 2")) is an outlier detection, semi-supervised ensemble algorithm. 
This approach is well known to successfully isolate outliers by using recursive partitioning (forming a tree-like structure) to decide whether the analyzed particle is an anomaly or not.
The less partitions required to isolate the more probable it is for a particle to be an anomaly.

- [ ] TODO: Honza tu vysvětlí jak funguje isolation forest, popíše všechny parametry a co dělají
      
#### Isolation Tree
Isolation tree je kořenový binární strom sestaven na základě vybrané podmnožiny $A$ prvků (bodů) o velikosti $s=|A|$.

1. pro sestavení isolation tree není potřeba mít početnou množinu dokonce to může být nežádoucí
2. dobře zvolené malé $s$ může pomoci odstranit *masking* a *swamping*

   masking 
   : problém anomálií v clusteru (aby byli označeny jako anomálie)
   
   swamping
   : problém normal bodů na okraji (normálního clusteru), které se jeví jako anomálie protože ty uvnitř clusteru mají moc velké ohodnocení 
3. isolation tree má dva druhy uzlů
   
   vnitřní
   : obsahuje podmínku (feature a mez) a dva potomky (jeden reprezentuje splněnou podmínku a druhý naopak nesplněnou) 
   
   vnější (list)
   : vzniká pokud podmínky rodičů splňuje (resp. nesplňuje) jeden nebo žádný prvek ze samplu, nebo je dosažena maximální hloubka stromu $l$ zpravidla $l=\ln_2(s)$. Obsahuje ohodnocení $h(x)$ pomocí vzdálenosti od kořene, pokud je dosaženo  max. délky stromu je *vzdálenost* odhadnuta pomocí $h(x)=e+c(n)$, $e$ je vzdálenost od kořene, $n$ je počet prvků ze samplu splňující podmínky rodičů, $c(n)=2\,(H_{n-1}-\frac{n-1}{N})$ a $H_{n-1}$ je $n-1$ harmonické číslo, $N$ je počet prvků celkově. 
   
- [ ] TODO: ověřit $c(n)$ nějak mi to furt nesedí
- [ ] TODO: Budeme to vysvětlovat obecně, nebo jen tak jak mi potřebujeme (2 dimenze x,y)?
- [ ] TODO: Implementace v Pythonu
   + [ ] jak je implementovaná funkce $c(x)$
   + [ ] jak je to s `max-depth` je nastaven na $\ln_2(n)$
   + [ ] jak se stanoví první interval, je $\langle 0, 1\rangle$, nebo $\langle min(data),max(data)\rangle$ nebo jinak
   + [ ] co ovlivňuje contanimation v kódu
- [ ] TODO: další možnost výzkumu (jinej článek) jak udělat isolation forest, 
  když data (features) nebudou hodnoty z intervalu, ale třeba hodnoty z konečné podmnožiny 

Despite its famousness, there are a few drawbacks.

The Scikit-Learn platform (scikit-learn.org) offers several implemented, documented and tested machine-learning open-source algorithms.
Its implementation of Isolation Forest has, in time of writing this text, 5 hyperparameters which need to be explicitly chosen and tuned.
First, the major challenge is setting the contamination parameter itself.
The contamination parameter is to control the proportion of anomalies in the dataset. 
Usually, this has to be known beforehand.
This parameter has a huge impact on the final result of the detection.
However, this is a problem because the anomalies in our dataset appear randomly and hence the proportion varies from 0% to 50%, sometimes even more.
To demonstrate the impact of contamination parameter, we prepared following experiment.
A dataset containing approx. 25% of anomalies is prepared.
Figures below show the differences when using rising values of the contamination parameter.
Note that dataset is generated randomly with each run.


![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/code/figures/contamination10.svg)
> Figure X Isolation Forest with 10% contamination.

![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/code/figures/contamination20.svg)
> Figure X Isolation Forest with 20% contamination.


![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/code/figures/contamination30.svg)
> Figure X Isolation Forest with 30% contamination.

![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/code/figures/contamination40.svg)
> Figure X Isolation Forest with 40% contamination.


Other notable parameters with huge impact on the result are *number of estimators*, *max samples* and *max features*.
Using similar dataset, we designed the experiment and tested the behavior of the Isolation Forest, with contamination parameter set to 0.25 (=25% anomalies) and varying above-mentioned parameters. 
The result of the experiment shows Figure X.
As we can see the results are quite distinct. 


![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/code/figures/isolation2.svg)
> Anomaly 2:
n_estimators=50
max_samples= 20
max_features=2
contamination = 0.25

![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/code/figures/isolation3.svg)

> Anomaly 3: 
n_estimators=10
max_samples= 10
max_features=2
contamination = 0.25


This kind of issue is widely known amongst AutoML community.
Some tools have already been implemented that try to deal with the issue of automatic hyperparameter tuning, namely H20 (h2o.ai) or AutoGluon (auto.gluon.ai). 

The last problem is with the unsupervised separation itself.
Consider data polluted by anomalies in close to 1:1 ratio.
Even human will find it nearly impossible to differentiate between these two classes when given plotted dataset.
Finding the line itself is obvious.
Deciding which observations are anomalies, without some domain knowledge on the other hand is close to impossible.

Despite this, one positive thing is that Isolation Forest managed to deal with the gaps in the measurement (seen in Figures above, around X=50). 

The final question is if it is somehow possible to teach Isolation Forest how regular observation look like. 
Can we use Isolation Forest for novelty detection despite it not being primarily novelty detection algorithm? 

### SOTA
Isolation forest has been widely used for outlier detection. 
In (https://doi.org/10.1016/j.patrec.2022.09.015) Xu, Yang and Rahardja show Isolation Forest outperforming other 12 state-of-the-art outlier detectors by running the experiments on public outlier detection datasets.
Thorough the years, many successful enhancements of the Isolation Forest have arisen. Gałka, Karczmarek, Tokovarov in (https://doi.org/10.1016/j.patrec.2022.09.015) implement Minimal Spanning Tree clustering based enhancement.
Instead of random determination of a split point, first, two clusters are prepared and then a split point is set to the middle of prepared clusters. Another interesting enhancement comes from Chater and al. (https://doi.org/10.1016/j.procs.2022.09.147) where the team deal with the necessity of having precise and crisp data when using basic Isolation Forest approach by implementing Fuzzy adaptation for the Isolation Forest.
However,  there seems to be not much work regarding using Isolation Forest as a novelty detection tool. 

### Isolation forest experiments
- [ ] TODO: TADY SI NAPÍŠEME VLASTNÍ FOREST A BUDEME DĚLAT CHYTRÉ

### Proposed novelty isolation forest enhancement
In this section, we propose a new approach for making forest detect novel observations. 
The proposed enhancement takes the basic idea of an ensemble of trees with depths but is taking it further to make supervised novel detection possible.
The basic problem with isolation forest not being able to detect novel observations is caused by the fact that with every new separation, isolation forest uses the separated data to evaluate next separation.
Figure X demonstrates this by creating a first node of a forest with dataset consisting of a sample from range (0,100), successfully creating a node and a random split point of 80. 
Later on, when Isolation Forest is being used for evaluation of a number 5000 (which is obviously far away from the initial (0, 100) range) the previous split point is used to determine its final node.
This results in 5000 being in the same node as numbers >80, making the novelty detection impossible.

![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/clanek_figures/isolation_5000.svg) 
> Figure X Isolation Forest novelty point insertion on using classic IF. 


 1. [ ] TODO:  blabla tady pokračujeme že možná nějaký obrázek jak to funguje že neustále se zmenšuje ten frame, to nám vlastně zapříčiní že 100,100 je stjeně novelty jako 1000,1000.
 2. [ ] TODO: tady popíšeme naši isolation servisku
 
In our proposed enhancement, we clearly have to deal with this issue.
The problem is to somehow evaluate the sparseness of the data, differentiating between datapoint being >80 and somehow "far bigger than 80", making the latter novelty.
The proposed solution is altering the concept of evaluation of a split point.
Whereas the original Isolation Forest is evaluating the split point based on the previous data, in our proposed solution we evaluate the split point based on the whole range.
For this to work, several alterations to the split point evaluation and form of data passed between nodes has to be done, but the overall concept of the forest stays the same. 
This is demonstrated by simply adding a new service to our proposed algorithm.
 3. [ ] TODO: šup sem odkaz na ruby algorithm s dokumentací

 We encourage you to try it and maybe create your own service based on our already implemented ones.
 This service called Novelty is making two main alteration concepts:
 
 

 4. List item

 



### Experiments using IF as a Novelty detection tool

- tady experimenty, heatmapa atp.

### Drawbacks, todos
 [ ] TODO: TADY POPIŠ například ŽE PRO MOC DIMENZÍ KDYŽ BY JICH BYLO HODNĚ STEJNÝCH TAK JE TO NAPRD 
 
### Finding clusters amongst novelties ??
 [ ] TODO: Honzo je to tu potřeba taková sekce, s přihlédnutím k tomu, že nově ten článek by měl být čistě o IF? kdyžtak prosím smazat všecko
- tady už stačí asi že prostě to není těžký ukol, vezmeme jen obyčejný DB scan a bác. oba algoritmy jsou jednoduché ale síla je v jejich kooperaci idk
- možná bychom se tu mohli taky zamyslet nad tím jak funguje ten DB Scan a zkusit trochu potunit aby to dělalo celé clustery

### automl hyperparameter tuning for IF - v jinem članku


## Results and discussion
- tady můžeme zkusit tabulku kde budeme ukazovat kolik procent novelty to našlo apt možná porovnání s nějakým buď expertem nebo nějakými referenčními olabelovanými daty
- zde napíšeme co se povedlo, jak to neni vubec lehke najit dva či více algoritmů které spolu dobře fungují a velký problem je jejich validace a verifikace, zkus navhrnout nějaké řešení verifikace
## Conclusion




<!--stackedit_data:
eyJoaXN0b3J5IjpbMjAxNzAwNTU4MywtMjMzNDcxNDY2LC0xND
c2NTM0NTYwLC0xNDc2NTM0NTYwLDE0OTkzNjA3MTgsMTQwMjcw
MDA3MywxNDAzNjY5NTEsLTc2MDY5MDUxNyw4MDg4NDAyOTUsNT
I4MDE2ODc5LDE4MDQwMTk3OTYsMTM1NTExNTM4LDExMjYxNzA4
NTUsLTEyNjc2Nzc1MzUsLTk2MTYwODY1MSwxODM5NTI5MTEwLC
0xNTIzMzc2NTA4LDEzODY0MjE5MjcsNjU2NDUzNSwxNzQ1Mzkw
NzMxXX0=
-->