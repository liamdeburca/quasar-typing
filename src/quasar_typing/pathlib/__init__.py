from .path import Path_

AbsolutePath    = Path_[True,  None]
NewAbsolutePath = Path_[True,  False]
RelativePath    = Path_[False, None]
NewRelativePath = Path_[False, False]

AnyFilePath         = Path_[None,  None,  'file']
AbsoluteFilePath    = Path_[True,  True,  'file']
NewAbsoluteFilePath = Path_[True,  False, 'file']
RelativeFilePath    = Path_[False, True,  'file']
NewRelativeFilePath = Path_[False, False, 'file']

AnyDirPath         = Path_[None,  None,  'dir']
AbsoluteDirPath    = Path_[True,  True,  'dir']
NewAbsoluteDirPath = Path_[True,  False, 'dir']
RelativeDirPath    = Path_[False, True,  'dir']
NewRelativeDirPath = Path_[False, False, 'dir']

AnyFITSPath         = Path_[None,  None,  '.fits']
AbsoluteFITSPath    = Path_[True,  True,  '.fits']
NewAbsoluteFITSPath = Path_[True,  False, '.fits']
RelativeFITSPath    = Path_[False, True,  '.fits']
NewRelativeFITSPath = Path_[False, False, '.fits']