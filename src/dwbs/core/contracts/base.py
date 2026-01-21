from pydantic import BaseModel, ConfigDict

class SystemContract(BaseModel):
    """Base class for all system contracts to ensure runtime validation."""
    model_config = ConfigDict(frozen=True)
