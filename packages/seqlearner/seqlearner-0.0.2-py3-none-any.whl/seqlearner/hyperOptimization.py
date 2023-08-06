import numpy as np
import pandas as pd

import tensorflow as tf
import matplotlib.pyplot as plt
import keras

from keras.layers import Input, Dense, Dropout, BatchNormalization
from keras.models import Model
from keras.callbacks import History, CSVLogger
from hyperopt import hp
from hyperas import optim
from hyperas.distributions import choice, uniform

"""
    Created by Mohsen Naghipourfar on 11/13/18.
    Email : mn7697np@gmail.com or naghipourfar@ce.sharif.edu
    Website: http://ce.sharif.edu/~naghipourfar
    Github: https://github.com/naghipourfar
    Skype: mn7697np
"""

embedding_dimensions = [5 * i for i in range(1, 21)]
word_lengths = [3, 4, 5, 6, 7, 8, 9, 10]
neighbor_length = [] # ?


