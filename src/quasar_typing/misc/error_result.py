from .any import AnyTypeGenerator
from ...decrypt.errors.error_result import ErrorResult
from ...decrypt.errors.nested.nested_result import NestedResult

ErrorResultLike = AnyTypeGenerator[ErrorResult]
NestedResultLike = AnyTypeGenerator[NestedResult]