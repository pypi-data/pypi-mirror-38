# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals, absolute_import

def plot_importance(
    feature_names=[], 
    feature_importances=[], 
    max_num_features=20,
    title='Feature Importances', 
    ):
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib

    matplotlib.rc('font', **{'family' : 'SimHei'})

    (pd.Series(feature_importances, index=feature_names)
        .nlargest(max_num_features).sort_values()
        .plot(kind='barh')) 

    plt.title(title)
    plt.show()

if __name__ == '__main__':
    pass



