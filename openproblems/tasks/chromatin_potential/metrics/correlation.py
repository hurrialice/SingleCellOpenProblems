from scipy.stats import pearsonr
from scipy.stats import spearmanr
from scipy.sparse import issparse
import numpy as np
from ....tools.decorators import metric


def _correlation(adata, method="pearson"):
    if method == "pearson":
        method = pearsonr
    else:
        method = spearmanr

    cors = []
    for i in range(adata.shape[0]):
        x = (
            adata.obsm["gene_score"][i].toarray()[0]
            if issparse(adata.obsm["gene_score"])
            else adata.obsm["gene_score"][i]
        )
        y = adata.X[i].toarray()[0] if issparse(adata.X) else adata.X[i]
        cors.append(method(x, y)[0])
    cors = np.array(cors)
    adata.obs["atac_rna_cor"] = cors
    return np.median(cors[~np.isnan(cors)])


@metric(metric_name="Median Pearson correlation", maximize=True)
def pearson_correlation(adata):
    return _correlation(adata)


@metric(metric_name="Median Spearman correlation", maximize=True)
def spearman_correlation(adata):
    return _correlation(adata, method="spearman")