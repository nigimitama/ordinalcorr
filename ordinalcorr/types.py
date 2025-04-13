from typing import Union, Sequence, TypeAlias, TypeVar
import numpy as np

T = TypeVar("T", int, float)
ArrayLike: TypeAlias = Union[Sequence[T], np.ndarray[T]]
