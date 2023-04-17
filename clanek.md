# Cluster Anomaly Detection in Time Series Data - work title

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
- **here we describe the domain!! - aneb jak ta data vypadají - co je cílem**
 

## Methods

The very first task is to thoroughly analyze the domain of the given problem.
The inappropriate choice of the selected solution could lead to undesirable results.
Having the problem already described, we are now able to analyze and establish a learning process. 

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

- [ ] TODO: TADY NAPIŠ JAKOBY ŽE ISOLATION FOREST NENI NOVELTY, ALE IDK...

### Isolation Forest
- [ ] TODO: TADY napíšeme něco jakože by nás zajímalo jestli si s tím poradí isolation forest, napíšeme že se často používá právě na outlier detection ale z toho co vysvětlíme bude jasné, že se dá použít na novelty

Isolation Forest ([1](https://doi.org/10.1016/j.engappai.2022.105730 "article 1"), [2](https://doi.org/10.1016/j.patcog.2023.109334 "article 2")) is an outlier detection, semi-supervised ensemble algorithm. 
This generally leads to an ensemble method called Isolation Forest ([1](https://doi.org/10.1016/j.engappai.2022.105730 "article 1"), [2](https://doi.org/10.1016/j.patcog.2023.109334 "article 2")).
This approach is well known to successfully isolate outliers by using recursive partitioning (forming a tree-like structure) to decide whether the analyzed particle is an anomaly or not.
The less partitions required to isolate the more probable it is for a particle to be an anomaly.

Despite its famousness, there are a few drawbacks.
First, there is a large number of hyperparameters to work with.
The Scikit-Learn platform (scikit-learn.org) offers several implemented, documented and tested machine-learning open-source algorithms.
Its implementation of Isolation Forest has, in time of writing this text, 8 hyperparameters which need to be explicitly chosen and tuned.
Figure X shows the differences of cluster time series analysis when performed on different hyperparameters.
As we can see the results are quite distinct. 


- [ ] TODO: vložit data z isolation forestu. - dva obrazky pod sebou s různými HYPERPARAMETRY

This kind of issue is widely known amongst AutoML community.
Some tools have already been implemented that try to deal with the issue of automatic hyperparameter tuning, namely H20 (h2o.ai) or AutoGluon (auto.gluon.ai). 

Second, the outlier detection approach is not capable to completely isolate out all of the anomalies. For this experiment, we prepared a dataset containing 25% anomalies and tested the behavior of the Isolation Forest, with contamination parameter set to 0.25 (=25% anomalies). The result of the experiment shows Figure X.

![](https://raw.githubusercontent.com/chazzka/clanekcluster/master/code/figures/isolation1.svg)
> Figure X, Isolation Forest with 25% of contamination.


The last problem is with the unsupervised separation itself.
Consider data polluted by anomalies in close to 1:1 ratio.
Even human will find it nearly impossible to differentiate between these two classes when given plotted dataset.
Finding the line itself is obvious.
Deciding which observations are anomalies, without some domain knowledge on the other hand is close to impossible.
Consider data shown in Figure 4.

- [ ] TODO: Figure 4 vložit nějaká těžce separovatelná data, třeba pul napul.

- [ ] TODO: otázka, je teda vubec možné ho použít? tady s Honzou vysvětlíme jak vlastně funguje ten IF, a ukážeme že si myslím že jo, použijeme ho jako novelty a ukážeme že to šlo

###  How to separate non anomalies
Using the data domain knowledge, some constraints usually arise.
As described in the introductory section, we expect the sensors to produce linear-like data, with minor deviations within the *y* axis.
These deviations do not follow any specific pattern and are completely random.
However, the errors report some kind of observable behavior.
This is usually the case when performing cluster analysis.
The main constraint that is crucial for this task is the cluster forming pattern.
The task could become straightforward if we divide it into subordinate tasks.
First of them is to use the knowledge to separate non-anomalies (not yet clusters).
Doing so, the data that is left are anomalies-only where the task of finding anomaly clusters only becomes less challenging. 

####  Unsupervised Isolation Forest
výš jsme si popsali jak funguje unsupervised separae (na naše data ne), ještě zkusíme jak funguje isolation forest na naše data

- [ ] TODO:. isolation forest označil data jako anomalie ale byly to validní data (např více lineárních urovní, které jsou však OK)

- [ ] TODO: vložit obrázek kde je více lineárních randomů, a pak nějaké clustery, tak ten unsupervised z toho bude samozřejmě zmatený

However, the major drawback in our particular problem were real world disturbances of the time series data.
Figure 2 shows the misconduct of the Isolation Forest algorithm when applied on the dataset with such disturbances, represented by the *gaps* in Figure 2.
This raises a question, whether should we preprocess the data first to remove those gaps somehow, and then use the Isolation Forest algorithm to find the anomalies.
However, there would still be the problem with the cluster-only separation remaining for the reasons described in the introduction section of this article. 



### finding the right clustering algorithm, TUNING OF DB SCAN
- tady už stačí asi že prostě to není těžký ukol, vezmeme jen obyčejný DB scan a bác. oba algoritmy jsou jednoduché ale síla je v jejich kooperaci idk

### automl hyperparameter tuning for IF - v jinem članku

## experiments
- [ ] TODO: TADY SE TO UŽ ZKOMBINUJE, ukaž obrázky, ukaž jak jde měnit parametry a bude to mít jiné výslekdy, více se zvýrazní clustery, méně atp...

## Results and discussion
- tady můžeme zkusit tabulku kde budeme ukazovat kolik procent anomálií to našlo apt možná porovnán s nějakým buď expertem nebo nějakými referenčními olabelovanými daty
- zde napíšeme co se povedlo, jak to neni vubec lehke najit dva či více algoritmů které spolu dobře fungují a velký problem je jejich validace a verifikace, zkus navhrnout nějaké řešení verifikace
## Conclusion




<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE5NTUxMjM1NjAsLTE5NDA4MTY0MjMsLT
EzNDMxMDE2NjksLTExOTg3Mjk0MDMsMTYxNDMyMzMzMCwtNTk0
Mjg5NjI3LC02MTMxMTY1NjcsLTg0MDg5NzIwOCw5NzY1NDg0OC
wtMTUzMjU3NDQzMiwtOTQ5ODA2MDE3LC0xOTQ5MjQ4ODUxXX0=

-->