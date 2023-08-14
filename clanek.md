# Using Isolation Forest as a Novelty Detection tool - work title

## Abstract
- téma
- toto jsme udělali
- co řešíme
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
- **here we describe the domain!! - aneb jak ta data vypadají - co je cílem hlavně vysvětlit čeho jsme chtěli dosáhnout**
 
## SOTA
- [ ] TODO: zde ze scikitu apod články na novelty detection algoritmy, stěmi to pak budeme porovnávat
https://scikit-learn.org/stable/modules/outlier_detection.html#novelty-detection
https://scikit-learn.org/stable/modules/outlier_detection.html#novelty-detection-with-local-outlier-factor

http://proceedings.mlr.press/v5/smola09a/smola09a.pdf

One of the successful methods dealing with novelty detection is OneClass SVM algorithm (10.1162/089976601750264965). 
#### One-class SVM novelty
The One-class SVM algorithm is the unsupervised outlier detection algorithm which can also be used for novelty detection.
It computes (optimizes) a binary function which is supposed to capture regions in input space where the probability density lives (its support), i.e., a function such that most of the data will live in the region where the function is nonzero (Schölkopf et al., 1999). 

Another method, initially used for unsupervised outlier detection but capable of being used as a novelty detection is the Local Outlier Factor algorithm.
#### Local Outlier Factor
The Local Outlier Factor (LOF) algorithm (https://doi.org/10.1145/335191.335388) assigns each point in the dataset a degree of outlier-ness.
Whereas previous attempts assigned datapoints a binary property (outlier/not), LOF algorithm assigns a real value, following a k-distance neighborhood. 
It first calculates the reachability distance from all the neighbors.
Based on this, the algorithm calculates the LOF score of the point and compares with the threshold.
This is done for all of the points until each point has its own LOF score.
When using this method for novelty detection, the novelty decision function is shifted opposite (large values correspond to inliers, whereas small values are novel datapoints).

#### Isolation Forest
Isolation forest on the other hand, has been widely used for outlier detection. 
In (https://doi.org/10.1016/j.patrec.2022.09.015) Xu, Yang and Rahardja show Isolation Forest outperforming other 12 state-of-the-art outlier detectors by running the experiments on public outlier detection datasets.
Thorough the years, many successful enhancements of the Isolation Forest have been developed. Gałka, Karczmarek, Tokovarov in (https://doi.org/10.1016/j.patrec.2022.09.015) implement Minimal Spanning Tree clustering-based enhancement.
Instead of random determination of a split point, first, two clusters are prepared and then a split point is set to the middle of prepared clusters. Another interesting enhancement comes from Chater and al. (https://doi.org/10.1016/j.procs.2022.09.147) where the team deal with the necessity of having precise and crisp data when using basic Isolation Forest approach by implementing Fuzzy adaptation for the Isolation Forest.
However, there does not seem to be much work regarding using Isolation Forest as a novelty detection tool. 

## Theory
Datapoint
: Datapoint is any observable data in


Outlier
: Outlier is an out-lying point.

Novelty
: Outlier is an out-lying point.


Anomaly
: Anomaly point is a point which is different can be any (both Outlier and Novelty) datapoint.


## Methods

Traditional approaches for anomaly separation consist of either novelty detection or outlier detection.
Novelty detection is an anomaly detection mechanism, where we search for unusual observations, which are discovered due to their differences from the training data.
Novelty detection is a semi-supervised anomaly-detection technique, whereas outlier detection uses unsupervised methods.
With novelty detection, the training data is not polluted by anomalous elements, and we are interested in detecting whether a new observation is an anomaly. In this context also called a novelty.
This is a crucial distinction, due to a fact that whereas the outlier detection is usually presented with data containing both anomalies and regular observation, it then uses mathematical models that try to make distinction between them, novelty detection on the other hand is usually presented data with little to zero anomalies (the proportion of anomalies in the dataset is called a contamination) and later, when conferred with an anomalous observation, it makes a decision. 

Consider following example. 
Figure X contains random datapoints arranged in a way they form a cluster like shape. 
Say this data is our regular observations. 
![](https://raw.githubusercontent.com/chazzka/clanekcluster/9047b936158e6320e0b4b942ab0d65c8e12f280f/clanek_figures/regular_observations_no_novelites.svg) 
> Figure X Dataset with regular observations. 

When an unsupervised, outlier detection algorithm tries to analyze such data, it sees the datapoints as a cluster containing both regular and anomalous observations. 
Figure X shows the result of evaluating classical Isolation Forest on such dataset.
![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/clanek_figures/regular_observations_outlier_if.svg) 
> Figure X Dataset with regular observations. 

Let *x* be regular observations and *y* false positive regular observations marked by Isolation Forest (batch_size 128, trees_count: 100, zbytek default), figure x shows that approx. 10% of observations are marked as anomalies.
This is not unwanted behavior in the sense of outlier detection but is undesired in the sense of novelty detection, because the false positive marked data are regular observations which should not be omitted.

Another problem is with the unsupervised separation itself.
Consider data polluted by anomalies in close to 1:1 ratio.
Even human will find it nearly impossible to differentiate between these two classes when given plotted dataset.
Finding the line itself is obvious.
Deciding which observations are anomalies, without some domain knowledge on the other hand is close to impossible.


### Isolation Forest
Isolation Forest ([1](https://doi.org/10.1016/j.engappai.2022.105730 "article 1"), [2](https://doi.org/10.1016/j.patcog.2023.109334 "article 2")) is an outlier detection, semi-supervised ensemble algorithm. 
This approach is well known to successfully isolate outliers by using recursive partitioning (forming a tree-like structure) to decide whether the analyzed particle is an anomaly or not.
The less partitions required to isolate the more probable it is for a particle to be an anomaly.

- [ ] TODO: Honza tu vysvětlí jak funguje isolation forest, popíše všechny parametry a co dělají
      
#### Isolation Tree
Isolation tree je kořenový binární strom sestaven na základě vybrané podmnožiny $A$ prvků (bodů) o velikosti $s=|A|$.

Isolation Tree is a binary tree constructed with a subset of $A$ items (datapoints) with the size $s=|A|$.

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
 - [ ] TODO: co ovlivňuje contanimation v kódu
- [ ] TODO: další možnost výzkumu (jinej článek) jak udělat isolation forest, 
  když data (features) nebudou hodnoty z intervalu, ale třeba hodnoty z konečné podmnožiny 

### Proposed novelty isolation forest enhancement
In this section, we propose a new enhancement of the original Isolation Forest algorithm for making it possible to detect novel observations. 
The proposed enhancement takes the basic idea of an ensemble of trees with depths but is taking it further to make supervised novel detection possible.
The essential problem with Isolation Forest algorithm not being able to detect novel observations is caused by the fact that with every new separation, isolation forest uses the separated data to evaluate next separation.

Let $x$ be regular observations known to the Isolation Forest algorithm a priory and $y$ the novel datapoints provided later. 
The standard Isolation Forest algorithm as defined by Liu et. al. selects the split point based on the min-max value according to a priory datapoints.

Figure X shows the first two decisions (*max_depth=2*) of the Isolation Forest algorithm provided a priory data points (marked red in left corner).
First, random dimension X and split point approx. around value 20 is chosen, orphaning most of the observations on the left side.
In the second decision, dimension Y was chosen, cracking the area on the right in two parts.
As we can see, the theoretical novel observations $y$ get assigned the same *path_length* as a priory known, non-novel regular observations. 

![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/clanek_figures/regular_observations_with_novelties_lines_squares.svg)
> Figure X standard Isolation Forest with novelty points. 


 - [ ] TODO: tady popíšeme naši isolation servisku
 
In our proposed enhancement, we clearly have to deal with this issue.
The proposed solution is altering the concept of evaluation of a split point.
Whereas the original Isolation Forest is evaluating the split point based on the previous data, in our proposed solution we evaluate the split point based on a range.
For this to work, several alterations to the split point evaluation and form of data passed between nodes has to be done, but the overall concept of the forest stays the same. 
This is demonstrated by simply adding a new service to our proposed algorithm.

  - [ ] TODO: šup sem odkaz na ruby algoritmus s dokumentací

 We encourage you to try it and maybe create your own service based on our already implemented ones.

 The service used in this article is making two main alteration concepts:
 
 1. When selecting a sample from the given data, to randomly selecting the sample of a given *batch size*, the evaluation of range was added.
 2. When the split point is calculated, random dimension is chosen, and the split point is taken from the evaluated range (and not the data itself).

The evaluation of a range starts by selecting some initial (either random or user defined) range for each dimension of N-dimensional problem. 
This range should be reasonable enough to allow all the domain space to be separated correctly, hence some tolerance is needed.

As a baseline, we select range by constructing a box plot, using interquartile range (1).

$$IQR = Q_3 - Q_1 = q_{.75} - q_{.25} \qquad (1)$$,
where $Q_1$ is the first quartile (also defined as 75th percentile) and $Q_3$ second quartile (also defined as 25th percentile).

#### Range tolerance selection
I addition to this, we need to add a tolerance layer to contain the later observed novelties.
This is usually done by adding a set of whiskers to a box plot.
The most straightforward selection of the whiskers is the min-max of the dataset.
This is not desired since the min-max would not cover possible later anomalies.
Instead, two other variations are tested, the *Notched box* and the *Adjusted box*.
##### Notched box
Notched box plots apply a "notch" or narrowing of the box around the median. 
Notches are useful in offering a rough guide of the significance of the difference of medians; if the notches of two boxes do not overlap, this will provide evidence of a statistically significant difference between the medians.

Let *n* be the amount of data, the boundaries of the notches around the median can be obtained as in (2).

$$f(x) = \pm \frac{1.58IQR}{\sqrt{n}} \qquad (2)$$

##### Adjusted box
Adjusted box is useful for describing the skew distributions.
It relies on the *medcouple* value (MC) of the dataset.
The *medcouple* is a statistic to measure the skewness (asymmetry of the prop. distribution) of a univariate distribution. 
As of Humert et. al (https://www.sciencedirect.com/science/article/pii/S0167947307004434?via%3Dihub)
for a medcouple value of MC, the lengths of the upper and lower whiskers on the box-plot are respectively defined in (3).

$$
f(x)= 
   \begin{cases}
    [Q_1 - 1.5\,IQR \cdot e^{-4\,MC},  Q_3 + 1.5\,IQR \cdot e^{3\,MC}],& \text{if } MC\geq 0\\
    [Q_1 - 1.5\,IQR \cdot e^{-3\,MC},  Q_3 + 1.5\,IQR \cdot e^{4\,MC}],& \text{if } MC\leq 0
	\end{cases}
	\tag{3}
$$

for symmetrical distributions, the MC value being zero, after substitution we get:

$$f_{MC_0}(x)=1.5\,IQR \tag{4}$$

Using above defined functions, the range is generated for each of the dimensions of the dataset.
The appropriate choice of the algorithm for the range tolerance selection is a matter of experiments and future research.

$$ranges = map(r_f , D)  \tag{5},$$

where $r_f$ being a random range generated using one of the above-defined functions and D being all of the dimensions of a given dataset.

This is due to a fact that individual dimensions can differ in their statistical distributions.

During the ITree initialization, a random range $r_f$ from the mapping (5) is chosen. 
Each node is grouped by a split point (SP), obtained as in (6).
$$SP = rand(r_f)  \tag{6}$$

, generating two groups for left and right node respectively (7).

$$group_{l,r}  = group\_by(<, SP) \tag{7}$$


Each of the nodes is then assigned a new ranges array as in (8,9).

$$range_{left} =  [{r_0, SP}] \tag{8}$$
$$range_{right} =  [{SP, r_{max}}] \tag{9}$$
, where $r_0$ is inherited (previous) range starting point and $r_{max}$ the inherited range ending point.

This allows the novel datapoints to make their way through the tree, making novelty detection possible.

Figure X shows, that after three runs (max_depth = 3) we successfully isolated the novel datapoints (y) by fitting them in the regions of a higher path_length.

Consider now point $P_x$ as depicted in Figure X. 
Using our new approach, $P_x$ is assigned into an area (node) with the *path length = 2*, assigning $P_x$ different path length.
This allows the distinctions between the points, making later novelty evaluation much more feasible.

![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/clanek_figures/regular_observations_with_novelties_lines_squares_novelty.svg)
> Figure X Isolation Forest novelty point insertion on using our novelty approach. Squares being points fed after the learning. 


## Experiments

The Scikit-Learn platform (scikit-learn.org) offers several implemented, documented and tested machine-learning open-source algorithms.

- [ ] TODO:  popíšeme že scikit má nějaké novelty detection algortimy, budeme to s nimi porovnávat
- [ ] TODO:  popíšeme že challenge je dobře nastavit hyperparametry

This kind of issue is widely known amongst AutoML community.
Some tools have already been implemented that try to deal with the issue of automatic hyperparameter tuning, namely H20 (h2o.ai) or AutoGluon (auto.gluon.ai). 

- [ ] TODO: prvně bychom měli vyhodnotit experimenty s odchylkou

| statistics:          | http.csv | shuttle.csv |   |   |
|----------------------|--------|-------|---|---|
| % anomalies/ % found |        |       |   |   |
| % false positive     |        |       |   |   |
|                      |        |       |   |   |

- [ ] TODO: tady experimenty, heatmapa atp., nějaký SOTA novelty algoritmus ze scikitu na porovnání

- [ ] TODO: přídáme i porovnání s bin/simple_novelty.rb
SVM: http.csv - anomalie všechny, ale pulku regularů označil jako ochylky
SVM: shuttle.csv - najde anomalie správně, ale pulku regularů označí jako anomálie
simple_novelty : http.csv - hodně dobře funguje, až moc
simple_novelty: shuttle.csv - nic moc
naše novelty: http.csv - slušné
naše novelty: shuttle.csv - horší ale OK
lof: http.csv - super
lof: shuttle.csv - super

- [ ] TODO: stanovit ranges na základě střední hodnoty a odchylky (doteď děláme mezikvart. odcyhlku) 

### Drawbacks, todos
-  [ ] TODO: TADY POPIŠ například ŽE PRO MOC DIMENZÍ KDYŽ BY JICH BYLO HODNĚ STEJNÝCH TAK JE TO NAPRD, když by se to lišilo jen v jedné tak je to naprd...
 
### automl hyperparameter tuning for IF - v jinem članku


## Results and discussion
- tady můžeme zkusit tabulku kde budeme ukazovat kolik procent novelty to našlo apt možná porovnání s nějakým buď expertem nebo nějakými referenčními olabelovanými daty
- zde napíšeme co se povedlo, jak to neni vubec lehke najit dva či více algoritmů které spolu dobře fungují a velký problem je jejich validace a verifikace, zkus navhrnout nějaké řešení verifikace
## Conclusion




<!--stackedit_data:
eyJoaXN0b3J5IjpbLTczNzM0MzM1NCwyMTQxNTY1ODU5LC01Nj
QxNzQ2OTIsMzkxNzgzNzAxLC0xODI2NDk4NzM0LDIwMDI2ODc3
MzcsMzI3MzI2NDQ4LC0yNTA3MzI3MiwtMzU1ODgxNzA3LDE0Mz
I4Mzk3MDAsLTIwMDIzNjEzODksLTc1NjQ3NjUzMiwtMTYwNDk3
Njg3NywtNzUxNTU0NzAxLDE2NDI0NzE0LDE1MzM4NDYyMjcsMT
kzODI2NTc1LDM3MDM2MzQzOCwxMTQ0MTI4MzMzLC00Mjk2OTc1
ODVdfQ==
-->