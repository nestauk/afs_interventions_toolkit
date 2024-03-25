import pandas as pd
from nesta_ds_utils.loading_saving import S3
from afs_interventions_toolkit import S3_BUCKET


def get_template_data(name: str) -> pd.DataFrame:
    """Get the template data for the parenting interventions.

    Args:
    name (str): The name of the template data file to get.

    Returns:
    pd.DataFrame: The template data for the parenting interventions.
    """
    return S3.download_obj(
        bucket=S3_BUCKET,
        path_from=f"data/templates/{name}.csv",
        download_as="dataframe",
        kwargs_reading={"engine": "python"},
    )
