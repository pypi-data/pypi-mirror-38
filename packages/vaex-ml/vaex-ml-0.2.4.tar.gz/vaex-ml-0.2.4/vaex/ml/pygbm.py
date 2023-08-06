import vaex
import pygbm
import numpy as np
import vaex.serialize
from . import state
import traitlets
import pygbm.binning


class VaexBinMapper(traitlets.HasTraits):
    max_bins = traitlets.CInt(255)
    random_state = traitlets.Any()
    subsample = traitlets.CInt(int(1e5))
    features = traitlets.List(traitlets.Unicode())

    def fit(self, dataset):
        self.bin_thresholds_ = []
        for feature in self.features:
            X = dataset[feature].values.reshape((-1, 1)).astype(np.float32)
            midpoints = pygbm.binning.find_binning_thresholds(
                X, self.max_bins, subsample=self.subsample,
                random_state=self.random_state)[0]
            self.bin_thresholds_.append(midpoints)
        self.bin_thresholds_

    def transform(self, dataset):
        N = len(dataset)
        M = len(self.features)
        # fortran order so 1 column is contiguous in memory
        binned = np.zeros((N, M), dtype=np.uint8, order='F')
        for m, feature in enumerate(self.features):
            X = dataset[feature].values.reshape((-1, 1)).astype(np.float32)
            binned1 = pygbm.binning.map_to_bins(X, binning_thresholds=self.bin_thresholds_)
            assert binned1.shape[1] == 1
            binned[:,m] = binned1[:,0]
        return binned

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)

        

@vaex.serialize.register
class PyGBMModel(state.HasState):

    features = traitlets.List(traitlets.Unicode())
    num_round = traitlets.CInt()
    param = traitlets.Dict()
    prediction_name = traitlets.Unicode(default_value='pygbm_prediction')
    learning_rate = traitlets.Float(0.1)
    max_iter = traitlets.Int(10)
    max_bins = traitlets.Int(255)
    max_leaf_nodes = traitlets.Int(31)
    random_state = traitlets.Int(0)
    verbose = traitlets.Int(1)
    prediction_name = traitlets.Unicode(default_value='pygbm_prediction')
 

    def fit(self, dataset, label):
        bin_mapper = VaexBinMapper(max_bins=self.max_bins, random_state=self.random_state, features=self.features)
        self.pygbm_model = pygbm.GradientBoostingMachine(
                            learning_rate=self.learning_rate,
                            max_iter=self.max_iter,
                            max_bins=self.max_bins,
                            max_leaf_nodes=self.max_leaf_nodes,
                            random_state=self.random_state,
                            scoring=None,
                            verbose=self.verbose,
                            validation_split=None,
                            bin_mapper=bin_mapper)
        # y = dataset[label].values
        if not hasattr(label, 'values'):
            label = dataset[label]
        y = label.values.astype(np.float32)
        self.pygbm_model.fit(dataset, y)
    
    def predict(self, dataset):
        data = np.vstack([dataset[k].values for k in self.features]).T
        return self.pygbm_model.predict(data)

    def __call__(self, *args):
        data = np.vstack([arg.astype(np.float32) for arg in args]).T.copy()
        return self.pygbm_model.predict(data)

    def transform(self, dataset):
        copy = dataset.copy()
        lazy_function = copy.add_function('pygbm_prediction_function', self)
        expression = lazy_function(*self.features)
        copy.add_virtual_column(self.prediction_name, expression, unique=False)
        return copy


@vaex.serialize.register
class PyGBMClassifier(PyGBMModel):
    def __call__(self, *args):
        return np.argmax(super(PyGBMClassifier, self).__call__(*args), axis=1)
    def predict(self, dataset, copy=False):
        return np.argmax(super(PyGBMClassifier, self).predict(dataset, copy=copy), axis=1)
