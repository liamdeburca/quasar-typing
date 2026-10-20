import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter

_import_structure: dict[str, list[str]] = {
    "optimize": [
        "OptimizeResultType",
    ],
    "sparse": [
        "CSRArray",
        "CSRMatrix",
        "DIAArray",
        "DIAMatrix",
        "SparseArray",
        "SparseMatrix",
    ],
    "stats": [
        "RVContinuous",
        "RVContinuousFrozen",
        "RVHistogram",
    ],
}

if TYPE_CHECKING:
    from .optimize import OptimizeResultType  # noqa: F401
    from .sparse import (  # noqa: F401
        CSRArray,
        CSRMatrix,
        DIAArray,
        DIAMatrix,
        SparseArray,
        SparseMatrix,
    )
    from .stats import (  # noqa: F401
        RVContinuous,
        RVContinuousFrozen,
        RVHistogram,
    )
else:
    sys.modules[__name__] = LazyImporter(
        __name__,
        __file__,
        _import_structure,
    )
