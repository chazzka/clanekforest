---


---

<h1 id="cluster-anomaly-detection-in-time-series-data---work-title">Cluster Anomaly Detection in Time Series Data - work title</h1>
<h2 id="abstract">Abstract</h2>
<ul>
<li>téma</li>
<li>toto jsme udělali</li>
<li>co řešíme (řešíme problem hledání clusterů dat, ne problem nějakeho algoritmu)</li>
<li>takto</li>
<li>takto jsme to otestovali</li>
<li>toto je výsledek</li>
</ul>
<h2 id="introduction">Introduction</h2>
<ul>
<li>start with lots of refs</li>
<li>describe the problem</li>
<li>our main goal was to</li>
<li>general -&gt; specific (describe problem as a whole, then why the problems occurs, then why is it a problem for us, technical details, env. variables)</li>
<li>constribution
<strong>here we describe the domain!! - aneb jak ta data vypadají - co je cílem</strong></li>
</ul>
<h2 id="methods">Methods</h2>
<p>The very first task is to thoroughly analyze the domain of the given problem. The inappropriate choice of the selected solution could lead to undesirable results. Having the problem already described, we are now able to analyze and establish a learning process.</p><p>One could easily argue that there is an option of using pure clustering algorithms (e.g. (<a href="doi/10.5555/3001460.3001507">DBScan</a>). This, however, leads to unpleasant outcome. Such algorithms tend to view the data as a cluster-only data, despite it being irrelevant in cluster regards. Figure X shows the performance of the DBScan algorithm on previously non-processed data. Even though the algorithm did find some clusters, it would be demanding to differentiate and find the one with anomalies. Moreover, DBScan algorithm managed to split the regular observations into two clusters, due to the gap in the measurement.   This brings up the idea of algorithm cross-cooperation. Therefore, the goal is to first separate the anomalies and then try to find a cluster amongst them.</p><p><img src="https://raw.githubusercontent.com/chazzka/clanekcluster/master/clanek_figures/DBScanGap.svg" alt=""></p><blockquote>
Figure X - DBScan performance.</blockquote>
<blockquote>
TODO: Figure X vložit data z DBScanu. - jeden obrázek který ukazuje že DBScan našel nějaké clustery, ale našel je i mezi anomaliemi</blockquote>
<p>Traditional approaches for anomaly separation consist of either novelty detection or outlier detection. Novelty detection is an anomaly detection mechanism, where we search for unusual observations, which are discovered due to their differences from the rest of the data. Novelty detection is a semi-supervised anomaly-detection technique, whereas outlier detection uses unsupervised methods. This a crucial distinction, due to a fact that whereas the outlier detection is usually presented with data containing both anomalies and regular observation, it then uses mathematical models that try to make distinction between them, novelty detection on the other hand is usually presented data with little to zero anomalies (the proportion of anomalies in the dataset is called a contamination) and later, when conferred with an anomalous observation, it makes a decision. This means, that if the dataset contains observation which may look like anomalies but are still valid, the performance of unsupervised outlier detection in such case is usually unsatisfactory.</p><blockquote>
TODO: TADY NAPIŠ JAKOBY ŽE ISOLATION FOREST NENI NOVELTY, ALE IDK…</blockquote>
<h3 id="isolation-forest">1. Isolation Forest</h3>
<blockquote>
TODO: TADY nepiš že je to první volba ale napiš něco jako bylo to po experimentech nejlepší</blockquote>
<p>When stumbling upon cluster analysis with outliers problem, the first approach is usually to try some of the ready-made solutions proven by experience. This generally leads to an ensemble method called Isolation Forest (<a href="https://doi.org/10.1016/j.engappai.2022.105730" title="article 1">1</a>, <a href="https://doi.org/10.1016/j.patcog.2023.109334" title="article 2">2</a>). This approach is well known to successfully isolate outliers by using recursive partitioning (forming a tree-like structure) to decide whether the analyzed particle is an anomaly or not. The less partitions required to isolate the more probable it is for a particle to be an anomaly.
Despite its famousness, there are a few drawbacks. First, there is a large number of hyperparameters to work with. The Scikit-Learn platform (<a href="http://scikit-learn.org">scikit-learn.org</a>) offers several implemented, documented and tested machine-learning open-source algorithms. Its implementation of Isolation Forest has, in time of writing this text, 9 hyperparameters which need to be explicitly chosen and tuned. Figure 1 shows the differences of cluster time series analysis when performed on different hyperparameters. As we can see the results are quite distinct.</p><p>TODO: HONZA DOSTANE PODÍL KDYŽ SEM NACPE MATIKU</p><p><code>TODO: vložit data z isolation forestu. - dva obrazky pod sebou s různými HYPERPARAMETRY</code></p><p>This kind of issue is widely known amongst AutoML community. Some tools have already been implemented that try to deal with the issue of automatic hyperparameter tuning, namely H20 (<a href="http://h2o.ai">h2o.ai</a>) or AutoGluon (<a href="http://auto.gluon.ai">auto.gluon.ai</a>).</p><h3 id="how-to-separate-non-anomalies">2. How to separate non anomalies</h3>
<p>Using the data domain knowledge, some constraints usually arise. As described in the introductory section, we expect the sensors to produce linear-like data, with minor deviations within the <em>y</em> axis. These deviations do not follow any specific pattern and are completely random. However, the errors report some kind of observable behavior. This is usually the case when performing cluster analysis. The main constraint that is crucial for this task is the cluster forming pattern. The task could become straightforward if we divide it into subordinate tasks.
First of them is to use the knowledge to separate non-anomalies (not yet clusters). Doing so, the data that is left are anomalies-only where the task of finding anomaly clusters only becomes less challenging.</p><h4 id="unsupervised-separation-intro">2.1 Unsupervised separation intro</h4>
<p>One of the biggest tasks is drawing the line between valid data and anomalies. Although this may seem trivial at first glance, the issue is quite troublesome. Even human will find it nearly impossible to differentiate between these two classes when given plotted dataset. Finding the line itself is obvious. Deciding which observations are anomalies, without some domain knowledge on the other hand is close to impossible. Consider data shown in Figure 4.</p><p><code>TODO: Figure 4 vložit nějaká těžce separovatelná data, nejlepe tři řady.</code></p><p>Figure 4 shows example dataset without any datamining or separation with three imaginary clusters. The question is, does the middle cluster represent anomalies or non-anomalies? Can we draw a line between these three clusters somehow? The most straightforward solution - to use moving average or MSE - is not really feasible, because anomalies tend to behave randomly. This means, such method could easily misbehave, e.g., mark a large portion of anomalies as non-anomalies, as shown in Figure 5.</p><p><code>TODO: Figure 5 ukaž čáru - průměr třeba nějaký, kde to rozseklo uplně debilně.</code></p><h4 id="unsupervised-isolation-forest">2.2 Unsupervised Isolation Forest</h4>
<p>výš jsme si popsali jak funguje unsupervised separae (na naše data ne), ještě zkusíme jak funguje isolation forest na naše data</p><p>TODO:. isolation forest označil data jako anomalie ale byly to validní data (např více lineárních urovní, které jsou však OK)</p><p>TODO: vložit obrázek kde je více lineárních randomů, a pak nějaké clustery, tak ten unsupervised z toho bude samozřejmě zmatený</p><p>However, the major drawback in our particular problem were real world disturbances of the time series data. Figure 2 shows the misconduct of the Isolation Forest algorithm when applied on the dataset with such disturbances, represented by the <em>gaps</em> in Figure 2. This raises a question, whether should we preprocess the data first to remove those gaps somehow, and then use the Isolation Forest algorithm to find the anomalies. However, there would still be the problem with the cluster-only separation remaining for the reasons described in the introduction section of this article.</p><p><code>TODO: vložit data z isolation forestu. - jeden obrázek který ukazuje že IF našel anomalie i mezi správnými daty kvuli časové mezeře.</code></p><h4 id="supervised-separation">2.2 Supervised separation</h4>
<blockquote>
TODO: tady se popíše ž forest má verzi supervised, takže ho naučíme na neanomálních datech, obrázky, popis</blockquote>
<h3 id="finding-the-right-clustering-algorithm-tuning-of-db-scan">finding the right clustering algorithm, TUNING OF DB SCAN</h3>
<ul>
<li>tad už stačí asi že prostě to není těžký ukol, vezmeme jen obyčejný DB scan a bác. oba algoritmy jsou jednoduché ale síla je v jejich kooperaci idk</li>
</ul>
<h3 id="automl-hyperparameter-tuning-for-if---v-jinem-članku">automl hyperparameter tuning for IF - v jinem članku</h3>
<h2 id="experiments">experiments</h2>
<blockquote>
TODO: TADY SE TO UŽ ZKOMBINUJE, ukaž obrázky, ukaž jak jde měnit parametry a bude to mít jiné výslekdy, více se zvýrazní clustery, méně atp…</blockquote>
<h2 id="results-and-discussion">Results and discussion</h2>
<ul>
<li>tady můžeme zkusit tabulku kde budeme ukazovat kolik procent anomálií to našlo apt možná porovnán s nějakým buď expertem nebo nějakými referenčními olabelovanými daty</li>
<li>zde napíšeme co se povedlo, jak to neni vubec lehke najit dva či více algoritmů které spolu dobře fungují a velký problem je jejich validace a verifikace, zkus navhrnout nějaké řešení verifikace</li>
</ul>
<h2 id="conclusion">Conclusion</h2>

