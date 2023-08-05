PIRS: Prediction Interval Ranking Score
=======================================

PIRS provides a means for identifying constitutive expression from time series data.  The software was designed for transcriptomic or proteomic data, but can be applied to any quantitative time series data. There is only one class 
rank, which performs the ranking.

----------
Motivation
----------

The issue of identifying increasing, decreasing or even cyclical patterns in time series data is well studied.  Little effort has been devoted to screening for stable expression.  Identifying constitutive expression is especially 
important when selecting reference genes which are later assumed to be stably expressed for purposes such as qPCR.  In the past many 'constitutively expressed' reference genes have later been identified to have circadian or other 
dynamic expression patterns.  PIRS provides for the systematic screening of expression profiles from high throughput time series to identify those which are truly constitutively expressed.

--------
Features
--------

* Prescreening of profiles for differential expression using ANOVA

* Ranking of peptides based on linear regression prediction intervals

-------------
Example Usage
-------------

```python
from PIRS import simulations, rank

simulation = simulations.simulate()
simulation.write_output(path_to_data)

data = rank.ranker(path_to_data)
sorted_data = data.pirs_sort(path_to_output)
```

------------
Installation
------------

pip install pirs

-------------------------------------
The Prediction Interval Ranking Score
-------------------------------------

How does PIRS identify constitutive expression?  Before answering this question, we should consider what characterizes constitutive expression.  We would expect such expression to be characterized by similar means across all 
timepoints and low variance relative to average expression for replicate timepoints.  How do we combine these two qualities into a single metric though?  In order to identify constitutive expression PIRS uses the 
prediction intervals from linear regressions.  A constitutive expression profile would be expected to have a narrow prediction interval which stays close to the overall mean of expression.  In contrast an upward or downward trend 
in expression would have a narrow prediction interval which would be farther from the mean expression at the beginning and end of the time series.  Lastly circadian or other dynamic expression centered on the mean expression would 
be expected to have wide prediction intervals which are far from the mean across the whole time series.  Each of these cases is pictured below:

![ImageRelative](data/illustration.png "illustration")

After calculating the prediction intervals PIRS simply considers the sum of squared errors between the upper and lower bounds of the interval and the mean expression across all the observed time points.  This value is then scaled 
relative to the mean expression producing the final score. 

### A Note on Data Formatting
PIRS expects input files to be formatted as tab seperated.  The first column should indicate the transcript or protein identifier.  The header should start with '#' and the rest of the header should be of the form 02_1 for data with
the first number indicating the timepoint and the second the replicate.  Single digit timepoints should include the leading zero for 
formatting. Missing values should be indicated by the string 'NULL'.  Example data file:

| # | 00_1 | 00_2 | 00_3 | 02_1 | 02_2 | 02_3 |
|---|---|---|---|---|---|---|
| ID | data | data | data | data | data | data |

###Performance
Using the included simulation utilities we can compare the preformance of PIRS to more frequently used standard deviation (SD) based metrics.  To generate a set of simulations, rank by both PIRS and SD and compare precision recall curves, we can run:

```python
from PIRS import simulations, rank

simulation = simulations.simulate()
simulation.write_output()

data = rank.ranker('simulated_data_with_noise.txt')
sorted_data = data.pirs_sort("pirs_scores.txt")

old_data = rank.rsd_ranker('simulated_data_with_noise.txt')
old_sorted_data = old_data.rsd_sort('rsd_scores.txt')

analysis = simulations.analyze()
analysis.add_classes('simulated_data_with_noise_true_classes.txt')
analysis.add_data('pirs_scores.txt','PIRS')
analysis.add_data('rsd_scores.txt','SD/RSD')
analysis.generate_pr_curve()
```

Which produces a figure like this:

![ImageRelative](data/PR.png "PR")

PIRS clearly outperforms a SD based metric, however it is useful to run several simulations to determine if this improved performance is consistent:

```python
from PIRS import simulations, rank

for i in range(20):
    simulation = simulations.simulate(rseed=i)
    simulation.write_output("sim_"+str(i)+".txt")
    data = rank.ranker("sim_"+str(i)+".txt")
    sorted_data = data.pirs_sort("pirs_"+str(i)+".txt")
    old_data = rank.rsd_ranker("sim_"+str(i)+".txt")
    old_sorted_data = old_data.rsd_sort("rsd_"+str(i)+".txt")


analysis = simulations.analyze()
for i in range(20):
    analysis.add_classes("sim_"+str(i)+"_true_classes.txt",rep=i)
    analysis.add_data("pirs_"+str(i)+".txt",'PIRS',rep=i)
    analysis.add_data("rsd_"+str(i)+".txt",'SD/RSD',rep=i)


analysis.generate_pr_curve()
```
Which produces something like this:

![ImageRelative](data/multi_PR.png "multi_PR")

### Further Exploration

If you'd like to explore the impact of varying simulated data parameters on the performance of PIRS, all you have to do is supply additional parameters during the simulation step.

* points = NUMBER OF TIMEPOINTS
* nrows = NUMBER OF ROWS OF DATA
* nreps = NUMBER OF REPLICATES
* tpoint_space = AMOUNT OF TIME BETWEEN TIMEPOINTS
* pcirc = PROBABILITY OF A ROW BEING CIRCADIAN
* plin = PROBABILITY OF A ROW HAVING A LINEAR TREND
* phase_prop = PROPORTION OF CIRCADIAN ROWS IN EACH PHASE GROUP (two phases of expression)
* phase_noise = AMOUNT OF VARIABILITY IN PHASE WITHIN PHASE GROUPS OF CIRCADIAN ROWS
* amp_noise = AMOUNT OF BIOLOGICAL VARIABILITY IN EXPRESSION

```
simulation = simulations.simulate(tpoints, nrows, nreps, tpoint_space, pcirc, plin, phase_prop, phase_noise, amp_noise)
```

----
TO DO
----

* Add API reference on readthedocs.

----
Built With
----

* numpy
* pandas
* scipy 
* sklearn 
* tqdm
* seaborn

-------
License
-------

© 2017 Alexander M. Crowell: BSD-3
