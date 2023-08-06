from typing import Set, Optional
from functools import partial
from pyspark.sql import Column
from pyspark.sql.types import StructType, StructField, ArrayType, MapType, IntegerType, DoubleType, StringType
from pyspark.sql.functions import udf
from . import combine

__all__ = [
    'SpkAnalyzedHit',
    'SpkHit',
    'SpkHits',
    'SpkCombinedHit',
    'SpkCombinedHits',
    'load_combiner',
]

SpkAnalyzedHit = StructType([
    StructField('pz', DoubleType(), nullable=False),
    StructField('px', DoubleType(), nullable=False),
    StructField('py', DoubleType(), nullable=False),
    StructField('ke', DoubleType(), nullable=False),
])

SpkHit = StructType([
    StructField('t', DoubleType(), nullable=False),
    StructField('x', DoubleType(), nullable=False),
    StructField('y', DoubleType(), nullable=False),
    StructField('as', MapType(StringType(), SpkAnalyzedHit), nullable=False),
    StructField('flag', IntegerType(), nullable=True),
])

SpkHits = ArrayType(SpkHit)

SpkCombinedHit = StructType([
    StructField('comb', SpkHits, nullable=False),
    StructField('as', MapType(StringType(), SpkAnalyzedHit), nullable=False),
])

SpkCombinedHits = ArrayType(SpkCombinedHit)


def load_combiner(r: int, white_list: Optional[Set[str]] = None) -> Column:
    if white_list is None:
        return udf(SpkCombinedHits)(partial(combine, r=r))
    return udf(SpkCombinedHits)(partial(combine, r=r, white_list=white_list))
