import pandas as pd
from nesta_ds_utils.loading_saving import S3
from afs_interventions_toolkit import S3_BUCKET


def saving_to_s3(data: pd.DataFrame, data_name: str) -> None:
    """Save the data to S3.

    Args:
    data (pd.DataFrame): The data to save.
    data_name (str): The name of the data.
    """
    S3.upload_obj(
        obj=data,
        bucket=S3_BUCKET,
        path_to=f"data/intervention_data/{data_name}.csv",
        kwargs_writing={"index": False},
    )
