import numpy as np
import pandas as pd
import pickle
import string
from sklearn.preprocessing import scale
from sklearn.metrics import precision_recall_curve, average_precision_score
import matplotlib.pyplot as plt
import random
import seaborn as sns

##Simulating single expression level, would have to equalize distribution of mean expressins between classes if simulating multiple expression levels

class simulate:
    """
    Generates a properly formulated simulated circadian dataset for testing.


    This class takes user specifications on dataset size along with the number and frequency of batch effects and levels of background noise and outputs a simulated dataset along with a key showing which rows represent truly circadian data.


    Parameters
    ----------
    tpoints : int
        
    nrows : int

    nreps : int

    tpoint_space : int
        
    pcirc : float

    plin : float

    phase_prop : float

    phase_noise : float

    amp_noise : float


    Attributes
    ----------

    simdf : dataframe

    Simulated data without noise.

    simndf : dataframe

    Simulated data with noise.

    """

    def __init__(self, tpoints=24, nrows=1000, nreps=3, tpoint_space=2, pcirc=.4, plin=.4, phase_prop=.5, phase_noise=.05, amp_noise=.35,  rseed=0):
        """
        Simulates circadian, linear and constitutive data and saves as a properly formatted example .csv file.

        

        """

        np.random.seed(rseed)
        self.tpoints = int(tpoints)
        self.nreps = int(nreps)
        self.nrows = int(nrows)
        self.tpoint_space = int(tpoint_space)
        self.pcirc = float(pcirc)
        self.plin = float(plin)
        self.phase_prop = float(phase_prop)
        self.phase_noise = float(phase_noise)
        self.amp_noise = float(amp_noise)

        #procedurally generate column names
        self.cols = []
        for i in range(self.tpoints):
            for j in range(self.nreps):
                self.cols.append(
                    ("{0:0=2d}".format(self.tpoint_space*i+self.tpoint_space))+'_'+str(j+1))

        #randomly determine which rows are circadian
        self.const = np.random.binomial(1, (1-self.pcirc-self.plin), self.nrows)
        #generate a base waveform
        base = np.arange(0, (4*np.pi), (4*np.pi/self.tpoints))
        #simulate data
        self.sim = []
        phases = []
        trend_types = np.random.binomial(1, self.pcirc, len(np.where(~self.const)[0]))
        for ind, val in enumerate(self.const):
            if val == 0:
                if trend_types[ind] == 1:
                    temp = []
                    p = np.random.binomial(1, self.phase_prop)
                    phases.append(p)
                    for j in range(self.nreps):
                        temp.append(np.sin(base+np.random.normal(0, self.phase_noise, 1) + np.pi*p)+np.random.normal(0, self.amp_noise, self.tpoints))
                    self.sim.append([item for sublist in zip(*temp) for item in sublist])
                else:
                    phases.append('nan')
                    temp = []
                    for j in range(self.nreps):
                        temp.append((1/(self.tpoints*self.tpoint_space))*np.arange(0, (self.tpoints*self.tpoint_space),
                                              self.tpoint_space)+np.random.normal(0, self.amp_noise, self.tpoints)-.5)
                    self.sim.append([item for sublist in zip(*temp) for item in sublist])
            else:
                phases.append('nan')
                self.sim.append(np.random.normal(
                    0, self.amp_noise, (self.tpoints*self.nreps)))
        
        self.sim = np.array(self.sim)

    def write_output(self, out_name='simulated_data_with_noise.txt'):
        """

        out_name : str

        output file stem

        """

        self.out_name = str(out_name)
        self.simndf = pd.DataFrame(self.sim, columns=self.cols)
        self.simndf.index.names = ['#']
        self.simndf.to_csv(out_name, sep='\t')

        pd.DataFrame(self.const, columns=['Const'], index=self.simndf.index).to_csv(out_name[:-4]+'_true_classes.txt', sep='\t')


class analyze:
    def __init__(self):
        self.true_classes = pd.DataFrame()
        self.merged = pd.DataFrame()

    def add_classes(self, filename_classes, rep=0):
        tc = pd.read_csv(filename_classes, index_col=0, sep='\t')
        tc['rep'] = rep
        self.true_classes = pd.concat([self.true_classes,tc])

    def add_data(self, filename_pirs, tag, rep=0):
        ranks = pd.read_csv(filename_pirs, index_col=0, sep='\t')
        ranks['method'] =  tag
        ranks['rep'] = rep
        ranks['score'].fillna(ranks['score'].max(), inplace=True)
        if self.merged.empty:
            self.merged = ranks
        else:
            self.merged = pd.concat([self.merged, ranks])

    def generate_pr_curve(self):
        self.curves = pd.DataFrame(columns=['precision','recall','method'])
        for rep, res in self.merged.groupby('rep'):
            for name, group in res.groupby('method'):
                pr = pd.merge(self.true_classes[self.true_classes['rep']==rep], group, right_index=True, left_index=True, how='inner')
                precision, recall, _ = precision_recall_curve(pr['Const'].values, 1/pr['score'].values, pos_label=1)
                temp = pd.DataFrame()
                temp['precision'] = precision
                temp['recall'] = recall
                temp['method'] = name
                temp['rep'] = rep
                self.curves = pd.concat([self.curves,temp])
        sns.lineplot(x='recall', y='precision', hue='method', units='rep', estimator=None, data=self.curves)
        plt.plot([0, 1], [np.mean(self.true_classes['Const']), np.mean(self.true_classes['Const'])], color='r', linestyle=':')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision Recall Comparison')
        plt.legend(loc="center right")
        plt.savefig('PR.png')
        plt.close()


    def calculate_auc(self):
        out = {}
        for j in self.tags.keys():
            fpr, tpr, thresholds = pr_curve(self.merged[self.tags[j]]['Const'].values, (self.merged[self.tags[j]]['score'].values), pos_label=1)
            out[j] = auc(fpr, tpr)
        self.pr_auc = out
