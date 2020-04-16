from typing import Set, List, Dict, Optional

import yaml
import jinja2
import pydantic

category: Set[str] = set()
with open("./gen/a.jinja2", encoding="utf8") as f:
    template = jinja2.Template(f.read())


class Item(pydantic.BaseModel):
    name: str = ""
    url: pydantic.AnyHttpUrl
    description: str = ""


class Awesome(pydantic.BaseModel):
    items: Dict[str, List[Item]]


with open("./awesome.yaml", encoding="utf") as f:
    raw_data = yaml.safe_load(f)
    data = Awesome.parse_obj(raw_data)
    with open("./readme.md", "w", encoding="utf8") as f:
        f.write(template.render(data=data.items))
