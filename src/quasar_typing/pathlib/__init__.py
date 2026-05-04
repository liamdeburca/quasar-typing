__all__ = [
    'AnyAbsolutePath', 'NewAbsolutePath', 'AbsolutePath',
    'AnyRelativePath', 'NewRelativePath', 'RelativePath',

    'AnyAbsoluteFilePath', 'NewAbsoluteFilePath', 'AbsoluteFilePath',
    'AnyRelativeFilePath', 'NewRelativeFilePath', 'RelativeFilePath',

    'AnyAbsoluteDirPath', 'NewAbsoluteDirPath', 'AbsoluteDirPath',
    'AnyRelativeDirPath', 'NewRelativeDirPath', 'RelativeDirPath',

    'AnyAbsoluteCSVPath', 'NewAbsoluteCSVPath', 'AbsoluteCSVPath',
    'AnyRelativeCSVPath', 'NewRelativeCSVPath', 'RelativeCSVPath',

    'AnyAbsoluteASCIIPath', 'NewAbsoluteASCIIPath', 'AbsoluteASCIIPath',
    'AnyRelativeASCIIPath', 'NewRelativeASCIIPath', 'RelativeASCIIPath',

    'AnyAbsoluteFITSPath', 'NewAbsoluteFITSPath', 'AbsoluteFITSPath',
    'AnyRelativeFITSPath', 'NewRelativeFITSPath', 'RelativeFITSPath',

    'AnyAbsoluteJSONPath', 'NewAbsoluteJSONPath', 'AbsoluteJSONPath',
    'AnyRelativeJSONPath', 'NewRelativeJSONPath', 'RelativeJSONPath',

    'AnyAbsolutePKLPath', 'NewAbsolutePKLPath', 'AbsolutePKLPath',
    'AnyRelativePKLPath', 'NewRelativePKLPath', 'RelativePKLPath',

    'AnyAbsoluteLogPath', 'NewAbsoluteLogPath', 'AbsoluteLogPath',
    'AnyRelativeLogPath', 'NewRelativeLogPath', 'RelativeLogPath',
]

from .path import Path_

_doc: str = "{} path (str or pathlib.Path) to {} file/directory"

### Paths

_doc: str = "absolute path (str or pathlib.Path) to {} file/directory"
AnyAbsolutePath = Path_[_doc.format('any'), True,  None, None]
NewAbsolutePath = Path_[_doc.format('new'), True,  False, None]
AbsolutePath = Path_[_doc.format('existing'), True,  True, None]

_doc: str = "relative path (str or pathlib.Path) to {} file/directory"
AnyRelativePath = Path_[_doc.format('any'), False, None, None]
NewRelativePath = Path_[_doc.format('new'), False, False, None]
RelativePath = Path_[_doc.format('existing'), False, True, None]

### Files

_doc: str = "absolute path (str or pathlib.Path) to {} file"
AnyAbsoluteFilePath = Path_[_doc.format('any'), True,  None, 'file']
NewAbsoluteFilePath = Path_[_doc.format('new'), True,  False, 'file']
AbsoluteFilePath = Path_[_doc.format('existing'), True,  True, 'file']

_doc: str = "relative path (str or pathlib.Path) to {} file"
AnyRelativeFilePath = Path_[_doc.format('any'), False, None, 'file']
NewRelativeFilePath = Path_[_doc.format('new'), False, False, 'file']
RelativeFilePath = Path_[_doc.format('existing'), False, True, 'file']

### Directories

_doc: str = "absolute path (str or pathlib.Path) to {} directory"
AnyAbsoluteDirPath = Path_[_doc.format('any'), True,  None, 'directory']
NewAbsoluteDirPath = Path_[_doc.format('new'), True,  False, 'directory']
AbsoluteDirPath = Path_[_doc.format('existing'), True,  True, 'directory']

_doc: str = "relative path (str or pathlib.Path) to {} directory"
AnyRelativeDirPath = Path_[_doc.format('any'), False, None, 'directory']
NewRelativeDirPath = Path_[_doc.format('new'), False, False, 'directory']
RelativeDirPath = Path_[_doc.format('existing'), False, True, 'directory']

### CSV

_doc: str = "absolute path (str or pathlib.Path) to {} CSV file"
AnyAbsoluteCSVPath = Path_[_doc.format('any'), True, None, '.csv']
NewAbsoluteCSVPath = Path_[_doc.format('new'), True, False, '.csv']
AbsoluteCSVPath = Path_[_doc.format('existing'), True, True, '.csv']

_doc: str = "relative path (str or pathlib.Path) to {} CSV file"
AnyRelativeCSVPath = Path_[_doc.format('any'), False, None, '.csv']
NewRelativeCSVPath = Path_[_doc.format('new'), False, False, '.csv']
RelativeCSVPath = Path_[_doc.format('existing'), False, True, '.csv']

### ASCII

_doc: str = "absolute path (str or pathlib.Path) to {} ASCII file"
AnyAbsoluteASCIIPath = Path_[_doc.format('any'), True, None, '.asc']
NewAbsoluteASCIIPath = Path_[_doc.format('new'), True, False, '.asc']
AbsoluteASCIIPath = Path_[_doc.format('existing'), True, True, '.asc']

_doc: str = "relative path (str or pathlib.Path) to {} ASCII file"
AnyRelativeASCIIPath = Path_[_doc.format('any'), False, None, '.asc']
NewRelativeASCIIPath = Path_[_doc.format('new'), False, False, '.asc']
RelativeASCIIPath = Path_[_doc.format('existing'), False, True, '.asc']

### FITS

_doc: str = "absolute path (str or pathlib.Path) to {} FITS file"
AnyAbsoluteFITSPath = Path_[_doc.format('any'), True, None, '.fits']
NewAbsoluteFITSPath = Path_[_doc.format('new'), True, False, '.fits']
AbsoluteFITSPath = Path_[_doc.format('existing'), True, True, '.fits']

_doc: str = "relative path (str or pathlib.Path) to {} FITS file"
AnyRelativeFITSPath = Path_[_doc.format('any'), False, None, '.fits']
NewRelativeFITSPath = Path_[_doc.format('new'), False, False, '.fits']
RelativeFITSPath = Path_[_doc.format('existing'), False, True, '.fits']

### JSON

_doc: str = "absolute path (str or pathlib.Path) to {} JSON file"
AnyAbsoluteJSONPath = Path_[_doc.format('any'), True, None, '.json']
NewAbsoluteJSONPath = Path_[_doc.format('new'), True, False, '.json']
AbsoluteJSONPath = Path_[_doc.format('existing'), True, True, '.json']

_doc: str = "relative path (str or pathlib.Path) to {} JSON file"
AnyRelativeJSONPath = Path_[_doc.format('any'), False, None, '.json']
NewRelativeJSONPath = Path_[_doc.format('new'), False, False, '.json']
RelativeJSONPath = Path_[_doc.format('existing'), False, True, '.json']

### PKL

_doc: str = "absolute path (str or pathlib.Path) to {} PKL file"
AnyAbsolutePKLPath = Path_[_doc.format('any'), True, None, '.pkl']
NewAbsolutePKLPath = Path_[_doc.format('new'), True, False, '.pkl']
AbsolutePKLPath = Path_[_doc.format('existing'), True, True, '.pkl']

_doc: str = "relative path (str or pathlib.Path) to {} PKL file"
AnyRelativePKLPath = Path_[_doc.format('any'), False, None, '.pkl']
NewRelativePKLPath = Path_[_doc.format('new'), False, False, '.pkl']
RelativePKLPath = Path_[_doc.format('existing'), False, True, '.pkl']

### Logs

_doc: str = "absolute path (str or pathlib.Path) to {} log file"
AnyAbsoluteLogPath = Path_[_doc.format('any'), True, None, '.log']
NewAbsoluteLogPath = Path_[_doc.format('new'), True, False, '.log']
AbsoluteLogPath = Path_[_doc.format('existing'), True, True, '.log']

_doc: str = "relative path (str or pathlib.Path) to {} log file"
AnyRelativeLogPath = Path_[_doc.format('any'), False, None, '.log']
NewRelativeLogPath = Path_[_doc.format('new'), False, False, '.log']
RelativeLogPath = Path_[_doc.format('existing'), False, True, '.log']