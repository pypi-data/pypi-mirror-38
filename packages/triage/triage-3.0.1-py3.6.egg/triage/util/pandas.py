from functools import partial
import pandas as pd
import logging


def downcast_matrix(df, indices):
    logging.info('Downcasting matrix. Starting memory usage: %s', df.memory_usage())
    new_df = df\
        .apply(partial(pd.to_numeric, downcast='float'))\
        .apply(partial(pd.to_numeric, downcast='integer'))\
        .set_index(indices)

    logging.info('Downcasted matrix. Final memory usage: %s', new_df.memory_usage())
    return new_df
