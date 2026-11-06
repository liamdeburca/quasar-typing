from typing import Annotated

from pydantic import Field

type RightAscension = Annotated[float, Field(ge=0.0, lt=360.0)]
type Declination = Annotated[float, Field(ge=-90.0, le=90.0)]
type Redshift = Annotated[float, Field(ge=0.0)]
type Distance = Annotated[float, Field(ge=0.0)]