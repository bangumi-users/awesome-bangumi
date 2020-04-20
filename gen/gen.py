from typing import List, Dict, Optional

import yarl
import yaml
import jinja2
import pydantic


class Image(pydantic.BaseModel):
    description: str
    url: str


class Item(pydantic.BaseModel):
    name: str = ""
    url: pydantic.AnyHttpUrl
    description: str = ""
    repo: Optional[pydantic.AnyHttpUrl]
    scm_host = {"github.com": "Github"}

    @property
    def repo_url(self) -> Optional[pydantic.AnyHttpUrl]:
        if self.repo:
            return self.repo
        if self.url.host in self.scm_host:
            return self.url

    @property
    def badge(self) -> str:
        url = self.repo_url
        if not url:
            return ""
        img_url = yarl.URL(f"https://img.shields.io/github/last-commit{url.path}")
        if url.host in self.scm_host:
            img_url = img_url.with_query({"logo": self.scm_host[url.host]})
        slug = url.path[1:]
        return f"[![{slug}]({img_url})]({url})"


class Awesome(pydantic.BaseModel):
    items: Dict[str, List[Item]]


with open("./gen/a.jinja2", encoding="utf8") as f:
    template = jinja2.Template(f.read())

with open("./awesome.yaml", encoding="utf") as f:
    raw_data = yaml.safe_load(f)
    data = Awesome.parse_obj(raw_data)
    with open("./readme.md", "w", encoding="utf8") as f:
        f.write(template.render(data=data.items))
