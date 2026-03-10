__all__ = [
    "AbsolutePath", "NewAbsolutePath", "RelativePath", "NewRelativePath",
    "AnyFilePath", "AbsoluteFilePath", "NewAbsoluteFilePath", 
    "RelativeFilePath", "NewRelativeFilePath",
    "AnyDirPath", "AbsoluteDirPath", "NewAbsoluteDirPath", "RelativeDirPath", 
    "NewRelativeDirPath",
    "AnyFITSPath", "AbsoluteFITSPath", "NewAbsoluteFITSPath", 
    "RelativeFITSPath", "NewRelativeFITSPath",
]

from .path import Path_

_doc: str = "{} path (str or pathlib.Path) to {} file/directory"

AbsolutePath    = Path_[_doc.format('absolute', 'existing'), True,  True]
NewAbsolutePath = Path_[_doc.format('absolute', 'any'),      True,  False]
RelativePath    = Path_[_doc.format('relative', 'existing'), False, True]
NewRelativePath = Path_[_doc.format('relative', 'any'),      False, False]

_doc: str = "{} path (str or pathlib.Path) to {} file"

AnyFilePath = \
    Path_[_doc.format('any', 'any'),           None,  None,  'file']
AbsoluteFilePath = \
    Path_[_doc.format('absolute', 'existing'), True,  True,  'file']
NewAbsoluteFilePath = \
    Path_[_doc.format('absolute', 'any'),      True,  False, 'file']
RelativeFilePath = \
    Path_[_doc.format('relative', 'existing'), False, True,  'file']
NewRelativeFilePath = \
    Path_[_doc.format('relative', 'any'),      False, False, 'file']

_doc: str = "{} path (str or pathlib.Path) to {} directory"

AnyDirPath = \
    Path_[_doc.format('any', 'any'),           None,  None,  'dir']
AbsoluteDirPath = \
    Path_[_doc.format('absolute', 'existing'), True,  True,  'dir']
NewAbsoluteDirPath = \
    Path_[_doc.format('absolute', 'any'),      True,  False, 'dir']
RelativeDirPath = \
    Path_[_doc.format('relative', 'existing'), False, True,  'dir']
NewRelativeDirPath = \
    Path_[_doc.format('relative', 'any'),      False, False, 'dir']

_doc: str = "{} path (str or pathlib.Path) to {} FITS file (.fits)"

AnyFITSPath = \
    Path_[_doc.format('any', 'any'),           None,  None,  '.fits']
AbsoluteFITSPath = \
    Path_[_doc.format('absolute', 'existing'), True,  True,  '.fits']
NewAbsoluteFITSPath \
    = Path_[_doc.format('absolute', 'any'),      True,  False, '.fits']
RelativeFITSPath \
    = Path_[_doc.format('relative', 'existing'), False, True,  '.fits']
NewRelativeFITSPath \
    = Path_[_doc.format('relative', 'any'),      False, False, '.fits']