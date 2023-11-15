# Settings are loaded from settings.json file
from pydantic import Field
from pydantic_yaml import parse_yaml_file_as
from typing import Dict, List, Optional, Union, Tuple
from pydantic.dataclasses import dataclass
import json

OUTFILE = "data/model.json"
SETTINGS_FILE = "settings.yaml"

AXES = ["system_1", "phase"]

@dataclass
class FunctionalUnit :
    formula: Union[str, int, float] = "1"
    unit: Optional[str] = None

@dataclass
class Settings :

    project : str
    """Project name"""

    database :str
    """Database name"""

    root_activity: str
    """Name or code of root activity of the inventory"""

    impacts : Dict[str, Tuple[str, ...]]
    """Dictionnary of "Impact name => ('tuple', 'key') """

    functional_units : Dict[str, FunctionalUnit]
    """Dictionnary of functional units"""

    axes: List[str] = Field(default_factory=lambda: [])
    """Optional list of axes (Total by default) """


settings:Settings = parse_yaml_file_as(Settings, SETTINGS_FILE)

# Add "Total" axe (None)
if not None in settings.axes:
    settings.axes.append(None)


