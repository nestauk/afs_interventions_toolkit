import pandas as pd
from nesta_ds_utils.loading_saving import S3
from afs_interventions_toolkit import S3_BUCKET


def get_local_authorities() -> pd.DataFrame:
    """Get the list of local authorities.

    Returns:
    pd.DataFrame: The list of local authorities.
    """
    return S3.download_obj(
        bucket=S3_BUCKET,
        path_from=f"data/public_data/local_authorities_list.csv",
        download_as="dataframe",
        kwargs_reading={"engine": "python"},
    )
