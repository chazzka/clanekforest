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
: Datapoint is any observable data with $n$ features.

Regular
: Regular is a datapoint included in the given dataset. Its features are expectable.

Anomaly
: Anomaly is a datapoint, that differs significantly from other observations.

Outlier
: Outlier is an anomaly included in the given dataset. 

Novelty
: Novelty is an anomaly that is not present in the given dataset during learning. Novelties are usually supplied later during evaluation.

Supervised algortihm
: Supervised algorithm is to je to co chceme aby to bylo

Unsupervised algortihm
: Supervised algorithm is to je to co chceme aby to bylo

Semisupervised algortihm
: Semi-supervised algorithm to je že máš labely jen napůl a chceš vědět které nedopovídají labelu


## Methods

Traditional approaches for anomaly detection consist of either novelty detection or outlier detection.
Novelty detection is an anomaly detection mechanism, where we search for unusual observations, which are discovered due to their differences from the training data.
Novelty detection is a semi-supervised anomaly detection technique, whereas outlier detection uses unsupervised methods.
With novelty detection, the training data is not polluted by anomalous elements, and we are interested in detecting whether a new observation is an anomaly. 
In this context such points are also called novelties.
This is a crucial distinction. 
The outlier detection is usually presented with data containing both anomalies and regular observation, it then uses mathematical models that try to make distinction between them. 
The novelty detection on the other hand is usually presented data with little to zero anomalies (the proportion of anomalies in the dataset is called a contamination) and later, when conferred with an anomalous observation, it makes a decision. 

Consider the following example:
Figure X contains random datapoints arranged in a way they form a cluster like shape. 
Say this data is our regular observations. 
![](https://raw.githubusercontent.com/chazzka/clanekcluster/9047b936158e6320e0b4b942ab0d65c8e12f280f/clanek_figures/regular_observations_no_novelites.svg) 
> Figure X Dataset with regular observations. 

When an unsupervised, outlier detection algorithm tries to analyze such data, it sees the datapoints as a cluster containing both regular and anomalous observations. 
Figure X shows the result of evaluating classical Isolation Forest on such dataset.
![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/clanek_figures/regular_observations_outlier_if.svg) 
> Figure X Dataset with regular observations. 

Figure x shows regular observations $x$ and anomaly observations $y$ marked by Isolation Forest (`batch_size 128, trees_count: 100, zbytek default`). 
Figure x shows that approx. $10\%$ of observations are anomalies.
This is not unwanted behavior in the sense of outlier detection but is false positive observation in the sense of novelty detection, because this data are regular observations which should be marked so.

Another problem is with the unsupervised separation itself.
Consider data polluted by anomalies in close to $1:1$ ratio.
Finding the line itself is obvious.
Deciding which observations are anomalies, without some domain knowledge on the other hand is close to impossible.


### Isolation Forest
Isolation Forest ([1](https://doi.org/10.1016/j.engappai.2022.105730 "article 1"), [2](https://doi.org/10.1016/j.patcog.2023.109334 "article 2")) is an outlier detection, unsupervised ensemble algorithm. 
This approach is well known to successfully isolate outliers by using recursive partitioning (forming a tree-like structure) to decide whether the analyzed datapoint is an anomaly or not.
The less partitions required to isolate the more probable it is for a datapoint to be an anomaly.

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
   
   vnitřní (internal vertex)
   : obsahuje podmínku (feature a mez) a dva potomky (jeden reprezentuje splněnou podmínku a druhý naopak nesplněnou) 
   
   vnější (list) (leaf)
   : vzniká pokud podmínky rodičů splňuje (resp. nesplňuje) jeden nebo žádný prvek ze samplu, nebo je dosažena maximální hloubka stromu $l$ zpravidla $l=\ln_2(s)$. Obsahuje ohodnocení $h(x)$ pomocí vzdálenosti od kořene, pokud je dosaženo  max. délky stromu je *vzdálenost* odhadnuta pomocí $h(x)=e+c(n)$, $e$ je vzdálenost od kořene, $n$ je počet prvků ze samplu splňující podmínky rodičů, $c(n)=2\,(H_{n-1}-\frac{n-1}{n})$ a $H_{n-1}$ je $n-1$ harmonické číslo. 
   
- [ ] TODO: Honza to tu vysvětlí obecně.
- [ ] TODO: další možnost výzkumu (jinej článek) jak udělat isolation forest, 
  když data (features) nebudou hodnoty z intervalu, ale třeba hodnoty z konečné podmnožiny 

### Proposed novelty isolation forest enhancement
#### Initial problem
In this section, we propose a new enhancement of the original Isolation Forest algorithm for making it possible to detect novelty observations. 
The proposed enhancement takes the basic idea of an ensemble of trees with various depths but is taking it further to make supervised novelty detection possible.
The standard Isolation Forest algorithm cannot be used for novelty detection.
This is because in each step, it limits the observation with the previously separated data.

Consider *regular* observations known to the Isolation Forest algorithm a priory and *anomaly* the novelty datapoints provided later. 
The standard Isolation Forest algorithm as defined by Liu et. al. selects the split point based on the min-max value according to a priory datapoints.

Figure X shows the first three decisions (`max_depth=3`) of the Isolation Forest algorithm provided a priory *regular* data points in the left bottom corner.
First, random feature $X$ and a random split point approx. $S  = 16$ are chosen, orphaning most of the observations on the left side.
In the second step, in the right area, feature *Y* was chosen, splitting the area in two parts. Observe, that the split point is always located between area-datapoint's minimum and maximum of the given feature.
As we can see, the theoretical novelty observations get assigned the same *depth* (the value of 3) as a priory known, regular observations.
After reaching the stopping criterion, the novelty point remains in the same vertex with a regular datapoint. This is true for any depth up until any chosen *max_depth*.


![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/clanek_figures/regular_observations_with_novelties_lines_squares_outlier.svg)
> Figure X Isolation Forest novelty point insertion using original approach. Squares being points fed after the learning.

#### Proposed solution
The proposed solution comes from an idea, that the original tree lacks the option to isolate more datapoints than it currently observes. 
The observed space is bounded by minimum and maximum in each feature.

Consider now point $P_a$ as depicted in Figure X.
In the proposed solution, $P_a$ falls into an area (vertex) with the *depth = 3*, isolating $P_a$ from the rest of the anomalies.
This allows the distinction between the points, making later novelty evaluation much more feasible.

Figure X shows, that after three runs (max_depth = 3) the regular datapoints had been isolated by being fitted in the regions of greater depth.
Although $P_a$ has the same depth as the regular observations, later will be shown that the final novelty score will differ. 

![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/clanek_figures/regular_observations_with_novelties_lines_squares_novelty.svg)
> Figure X Isolation Forest novelty point insertion on using our novelty approach. Squares being points fed after the learning. 


As in the original article, we use the concept of a binary decision tree.
The proposed solution is altering the concept of the split point evaluation.
Whereas the original Isolation Forest is evaluating the split point based on the previous data, in our proposed solution we evaluate the split point based on a range.
For this to work, several alterations to the split point evaluation and the form of data passed between vertices has to be done however, the overall concept of the forest stays the same. 

In the proposed solution, there are two main alteration concepts to the original solution.


 1. Each of the vertices gets assigned a space bounded by ranges.\
Each range should be reasonable enough to allow all the domain space to be separated correctly, hence some tolerance is needed.

 3. The split point is in the middle of the given feature's *range*.
 4. The input observations are only used to detect leaves.



##### Basis step
The only vertex $v$ is a trivial binary tree $T_0$. For each $i \in\{1, \dots, n\}$, feature $f_i$ is bounded by the range $r_i$. The ranges form the possibility space $R$ as in (xx). 
$$R =  r_1 \times r_2 \times \cdots \times r_n  \tag{xx}$$
Subset $D$ is a set of all datapoints, such that $D = \{d; d \in R \}$.

##### Recursive step
pro každý list: 

for each leaf v not satisftining the ending condition create two new vertices $v_l, v_r$ and same amount of edges $(v,v_l ), (v, v_r)$ as in (xx).
$$fds$$
 
internal vertex vT, 
1.  splňuje koncovou podmínku, dopočítej depth
2. nesplňuje, z listu udělej internal vertex, který si bude nést rozhodovací podmínku a bude mít dva nové listy, 

opakuj dokud všechny listy nesplňují podmínku

 
In each construction step, the random feature's range is obtained. 
The splint point $S$ is obtained as the middle of the range $r=\langle R_s, R_e\rangle$ as in (6). 

$$S = \frac{r_s + r_e}{2}, \tag{6}$$

generating two ranges $r_l = \langle R_s, S )$; $r_r = \langle  S, R_e \rangle$ for left and right vertex respectively (7).

$$B_l  = \{ x \in B; x \in r_l \}; \quad B_r  = \{ x \in B; x \in r_r \} \tag{7}$$


This process is recursively repeated for each of the branches of a tree.
The left branch gets assigned new batch $B_l$ and a new range $r_l$ and the information about current depth $d + 1$.
Analogously, the right branch gets assigned new batch $B_r$ and a new range $r_r$ with the information about current depth.


#begin další článek
-------------------

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

#end další článek
-------------------------------------------------------------------


##### Implementation

For the ease of implementing and experimenting, we created a Ruby Gem implementing the Isolation Forest algorithm. It is open-source and available online at.
- [ ] TODO: šup sem odkaz na ruby algoritmus s dokumentací

The standard Isolation Forest service can be found in the standalone package at. 
- [ ] TODO: šup sem odkaz na ruby algoritmus s dokumentací

The appropriate choice of the algorithm for the range tolerance selection is a matter of experiments and future research.

In this section we describe the Isolation Forest, pinpointing the changes made by Novelty Service.

This is demonstrated by a new service (TODO: odkaz) which was created by modifying the standard the Isolation Forest implementation in [odkaz na kapitolu].
 
 We encourage you to try it and maybe create your own service based on our already implemented ones.

First, the correct hyperparameters setting is needed in order to properly use the Novelty service.
For the Novelty service to work, it is necessary to set the following set of attributes:
These attributes apply to a single tree.

batch_size
: Each of the trees gets assigned a random sample of *batch_size* datapoints. 

ranges
 : An appropriate range of values for each of the features of a dataset. 

max_depth
: The maximum depth of a tree. 
Stopping criterion.
For high-dimensionality problems it is advised to be set a higher value than in the standard implementation.
Matter of a future research.


Moreover, the number of trees can be set during the Forest initialization.

trees
: The number of trees of a forest. 

We begin with a dataset of regular, conceivably little contaminated observations and a set of above defined parameters.
Out of these observations, the set $B$ of *batch_size* items is selected.
 

begin jiny clanek/diskuze
---------
where $r_f$ being a random range generated using one of the above-defined functions and D being all of the dimensions of a given dataset.
This is due to a fact that individual dimensions can differ in their statistical distributions.

end jiny clanek/diskuze
----


## Experiments

The Scikit-Learn platform (scikit-learn.org) offers several implemented, documented and tested machine-learning open-source algorithms.

- [ ] TODO: TADY JEN NAPÍŠEME NĚJAKÉ KECY ŽE JSME POUŽILI AUTOKONFIGURACI PRO NASTAVENÍ RANGES, jinak další článek

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

 
### automl hyperparameter tuning for IF - v jinem članku


## Results and discussion
- tady můžeme zkusit tabulku kde budeme ukazovat kolik procent novelty to našlo apt možná porovnání s nějakým buď expertem nebo nějakými referenčními olabelovanými daty
- zde napíšeme co se povedlo, jak to neni vubec lehke najit dva či více algoritmů které spolu dobře fungují a velký problem je jejich validace a verifikace, zkus navhrnout nějaké řešení verifikace

## Drawbacks, todos
-  [ ] TODO: TADY POPIŠ například ŽE PRO MOC DIMENZÍ KDYŽ BY JICH BYLO HODNĚ STEJNÝCH TAK JE TO NAPRD, když by se to lišilo jen v jedné tak je to naprd...

## Conclusion







<!--stackedit_data:
eyJoaXN0b3J5IjpbODkyNTIwODAxLDE5NzEyODQzNDAsOTkwNj
kwOTI3LDEwMDQ0ODUzNTYsLTY3NzY2MDQxMywtMTcwMDUxNjQ1
OSwtMTA2NjA2OTk2OSwxMDUyNzc5NzY1LC0xNTY5ODc0MDMyLD
g0NTI1MjgxNCwtMTk4OTI5Mzg0MCwxMTA5Mjg1MjA2LDIxMDE3
NTQ4MSwyNTM3MDEzMzQsLTE1NzI4NDg3OTMsMTk2MzAxNjE3Ny
wtODYwMTYzNzkxLC0xOTYwNzA5OTkyLDE2MjM5MDQ1MzMsMjA5
Njg2OTM3MV19
-->