import pandas as pd
from nesta_ds_utils.loading_saving import S3
from afs_interventions_toolkit import S3_BUCKET


def get_interventions() -> pd.DataFrame:
    """Get the list of parenting interventions.

    Returns:
    pd.DataFrame: The list of parenting interventions.
    """
    return S3.download_obj(
        bucket=S3_BUCKET,
        path_from=f"data/public_data/interventions_eif_rating.csv",
        download_as="dataframe",
        kwargs_reading={"engine": "python"},
    )
