import numpy as np
from sklearn.base import ClusterMixin, BaseEstimator
from sklearn.utils import check_array
from sklearn.utils.validation import check_is_fitted, validate_data

from ktree.ntree import NTreeDynamic, NTreeStatic, NTreeMean


class TreeCluster(ClusterMixin, BaseEstimator):
    def __init__(self, limit_division: int = 1, default_distribution=None):
        self.limit_division = limit_division
        self.default_distribution = 'static' if default_distribution is None else default_distribution

    def fit(self, X: np.ndarray, y=None):
        X = check_array(X)

        self.n_features_in_ = X.shape[1]

        if self.limit_division < 1:
            raise ValueError(f"limit_division must be >= 1, got {self.limit_division}")

        if self.default_distribution == "static":
            ranges = np.array([(np.min(X[:, n]), np.max(X[:, n])) for n in range(self.n_features_in_)])
            d_tree = NTreeStatic(self.limit_division, ranges)
        elif self.default_distribution == "mean":
            d_tree = NTreeMean(self.limit_division)
        elif self.default_distribution == "dynamic":
            d_tree = NTreeDynamic(self.limit_division)
        else:
            raise ValueError(f"Unrecognized distribution: {self.default_distribution}")

        d_tree.raw_data = X

        sorted_nodes = d_tree.sort()

        labels = np.empty(X.shape[0], dtype=int)
        raw_data_sorted = []

        current_idx = 0

        for _id, node in enumerate(sorted_nodes):
            data = np.array(node.data)
            n_samples_in_node = len(data)

            labels[current_idx: current_idx + n_samples_in_node] = _id

            raw_data_sorted.append(data)
            current_idx += n_samples_in_node

        self.labels_ = labels
        self.cluster_centers_ = np.vstack(raw_data_sorted)
        self.n_clusters_ = len(sorted_nodes)

        return self

    def predict(self, X):
        check_is_fitted(self)
        X = validate_data(self, X, reset=False)
        X = check_array(X)

        if X.shape[1] != self.n_features_in_:
            raise ValueError(
                f"They were expected {self.n_features_in_} features, "
                f"received {X.shape[1]}."
            )

        distances = np.linalg.norm(
            X[:, None] - self.cluster_centers_[None, :], axis=2
        )

        return np.argmin(distances, axis=1)

    def fit_predict(self, X, y=None):
        return self.fit(X, y).labels_
