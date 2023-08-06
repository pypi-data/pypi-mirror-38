import vaex.dataset
from vaex.serialize import register
import numpy as np
from . import generate
from .state import HasState
from traitlets import Dict, Unicode, List, Int, CFloat, CBool, Any, Tuple


def dot_product(a, b):
    products = ['%s * %s' % (ai, bi) for ai, bi in zip(a, b)]
    return ' + '.join(products)


@register
class StateTransfer(HasState):
    state = Dict()

    def transform(self, dataset):
        copy = dataset.copy()
        self.state = dict(self.state, active_range=[copy._index_start, copy._index_end])
        copy.state_set(self.state)
        return copy


@register
@generate.register
class PCA(HasState):
    '''Transform a set of features using a Principal Component Analysis'''

    # title = Unicode(default_value='PCA', read_only=True).tag(ui='HTML')
    features = List(Unicode()).tag(ui='SelectMultiple')
    n_components = Int(default_value=2).tag(ui='IntText')
    prefix = Unicode(default_value="PCA_")
    eigen_vectors_ = List(List(CFloat())).tag(output=True)
    eigen_values_ = List(CFloat()).tag(output=True)
    means_ = List(CFloat()).tag(output=True)

    def fit(self, dataset, column_names=None, progress=False):
        assert self.n_components <= len(self.features), 'cannot have more components than features'
        C = dataset.cov(self.features, progress=progress)
        eigen_values, eigen_vectors = np.linalg.eigh(C)
        indices = np.argsort(eigen_values)[::-1]
        self.means_ = dataset.mean(self.features, progress=progress).tolist()
        self.eigen_vectors_ = eigen_vectors[:, indices].tolist()
        self.eigen_values_ = eigen_values[indices].tolist()

    def transform(self, dataset, n_components=None):
        n_components = n_components or self.n_components
        copy = dataset.copy()
        name_prefix_offset = 0
        eigen_vectors = np.array(self.eigen_vectors_)
        while self.prefix + str(name_prefix_offset) in copy.get_column_names(virtual=True, strings=True):
            name_prefix_offset += 1

        expressions = [copy[feature]-mean for feature, mean in zip(self.features, self.means_)]
        for i in range(n_components):
            v = eigen_vectors[:, i]
            expr = dot_product(expressions, v)
            name = self.prefix + str(i + name_prefix_offset)
            copy[name] = expr
        return copy


@register
@generate.register
class LabelEncoder(HasState):
    '''Encode labels with integer value between 0 and num_classes-1.'''

    # title = Unicode(default_value='Label Encoder', read_only=True).tag(ui='HTML')
    features = List(Unicode()).tag(ui='SelectMultiple')
    prefix = Unicode(default_value="label_encoded_").tag(ui='Text')
    labels_ = List(List()).tag(output=True)

    def fit(self, dataset):
        labels = []
        for i in self.features:
            labels.append(np.unique(dataset.evaluate(i)).tolist())
        self.labels_ = labels

    def transform(self, dataset):
        copy = dataset.copy()
        for i, v in enumerate(self.features):
            name = self.prefix + v
            labels = np.unique(dataset.evaluate(v))
            if len(np.intersect1d(labels, self.labels_[i])) < len(labels):
                diff = np.setdiff1d(labels, self.labels_[i])
                raise ValueError("%s contains previously unseen labels: %s" % (v, str(diff)))
            # copy[name] = np.searchsorted(self.labels[i], v)
            copy.add_virtual_column(name, 'searchsorted({x}, {v})'.format(x=self.labels_[i], v=v))
        return copy


@register
@generate.register
class OneHotEncoder(HasState):
    '''Encode categorical labels according ot the One-Hot scheme.'''

    # title = Unicode(default_value='One-Hot Encoder', read_only=True).tag(ui='HTML')
    features = List(Unicode()).tag(ui='SelectMultiple')
    prefix = Unicode(default_value='').tag(ui='Text')
    uniques_ = List(List()).tag(output=True)
    one = Any(1)
    zero = Any(0)

    def fit(self, dataset):
        '''
        Method that fits the labels according to the One-Hot scheme.

        :param dataset: a vaex dataset
        '''

        uniques = []
        for i in self.features:
            expression = vaex.dataset._ensure_strings_from_expressions(i)
            unique = dataset.unique(expression)
            unique = np.sort(unique)  # this can/should be optimized with @delay
            uniques.append(unique.tolist())
        self.uniques_ = uniques

    def transform(self, dataset):
        '''
        Method that applies the the fitted one-hot encodings to a vaex dataset.

        :param dataset: a vaex dataset
        :return copy: a shallow copy of the input vaex dataset that includes the encodings
        '''

        copy = dataset.copy()
        # for each feature, add a virtual column for each unique entry
        for i, feature in enumerate(self.features):
            for j, value in enumerate(self.uniques_[i]):
                column_name = self.prefix + feature + '_' + str(value)
                copy.add_virtual_column(column_name, 'where({feature} == {value}, {one}, {zero})'.format(
                                        feature=feature, value=repr(value), one=self.one, zero=self.zero))
        return copy


@register
@generate.register
class StandardScaler(HasState):
    '''Will translate and scale a set of features using its mean and standard deviation'''

    # title = Unicode(default_value='Standard Scaler', read_only=True).tag(ui='HTML')
    features = List(Unicode()).tag(ui='SelectMultiple')
    prefix = Unicode(default_value="standard_scaled_").tag(ui='Text')
    with_mean = CBool(default_value=True).tag(ui='Checkbox')
    with_std = CBool(default_value=True).tag(ui='Checkbox')
    mean_ = List(CFloat()).tag(output=True)
    std_ = List(CFloat()).tag(output=True)

    def fit(self, dataset):

        mean = dataset.mean(self.features, delay=True)
        std = dataset.std(self.features, delay=True)

        @vaex.delayed
        def assign(mean, std):
            self.mean_ = mean.tolist()
            self.std_ = std.tolist()

        assign(mean, std)
        dataset.executor.execute()

    def transform(self, dataset):
        copy = dataset.copy()
        for i in range(len(self.features)):
            name = self.prefix+self.features[i]
            expression = copy[self.features[i]]
            if self.with_mean:
                expression = expression - self.mean_[i]
            if self.with_std:
                expression = expression / self.std_[i]
            copy[name] = expression
        return copy


@register
@generate.register
class MinMaxScaler(HasState):
    '''Will scale a set of features from [min, max] to [0, 1)'''

    # title = Unicode(default_value='MinMax Scaler', read_only=True).tag(ui='HTML')
    features = List(Unicode()).tag(ui='SelectMultiple')
    # feature_range = List(CFloat()).tag(ui='FloatRangeSlider')
    feature_range = Tuple(default_value=(0,1)).tag().tag(ui='FloatRangeSlider')
    prefix = Unicode(default_value="minmax_scaled_").tag(ui='Text')
    fmax_ = List(CFloat()).tag(output=True)
    fmin_ = List(CFloat()).tag(output=True)

    def fit(self, dataset):
        assert len(self.feature_range) == 2, 'feature_range must have 2 elements only'
        minmax = dataset.minmax(self.features)
        self.fmin_ = minmax[:, 0].tolist()
        self.fmax_ = minmax[:, 1].tolist()

    def transform(self, dataset):
        copy = dataset.copy()

        for i in range(len(self.features)):
            name = self.prefix + self.features[i]
            a = self.feature_range[0]
            b = self.feature_range[1]
            expr = copy[self.features[i]]
            expr = (b-a)*(expr-self.fmin_[i])/(self.fmax_[i]-self.fmin_[i]) + a
            copy[name] = expr
        return copy
