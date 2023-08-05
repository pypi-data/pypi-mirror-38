from scipy.stats import logistic
from numpy import tanh

SIGMOIDE = lambda x: logistic.cdf(x)
HIPERBOLICA = lambda x: tanh(x)

