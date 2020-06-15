from typing import List, Dict, Optional, Union

import yarl
import yaml
import jinja2
import pydantic

SCM_HOST = {"github.com": "Github"}


class Image(pydantic.BaseModel):
    image: pydantic.AnyHttpUrl
    description: str = ""

    def render(self):
        return f"![{self.description}]({self.image})"


class Badge(Image):
    link: Optional[pydantic.AnyHttpUrl] = None

    @classmethod
    def from_repo(cls, url):
        if not url:
            raise ValueError(f"{url} is not a valid github repo url")
        img_url = yarl.URL(f"https://img.shields.io/github/last-commit{url.path}")
        if url.host in SCM_HOST:
            img_url = img_url.with_query({"logo": SCM_HOST[url.host]})
        slug = url.path[1:]
        return cls.parse_obj({"description": slug, "image": str(img_url), "link": url})

    def render(self):
        if self.link:
            return f"[{super().render()}]({self.link})"
        return super().render()


class Item(pydantic.BaseModel):
    name: str = ""
    url: pydantic.AnyHttpUrl
    description: str = ""
    repo: Optional[pydantic.AnyHttpUrl]
    badges: List[Union[pydantic.AnyHttpUrl, Badge]] = []

    @property
    def repo_url(self) -> Optional[pydantic.AnyHttpUrl]:
        if self.repo:
            return self.repo
        if self.url.host in SCM_HOST:
            return self.url

    @property
    def badge(self) -> str:
        url = self.repo_url
        if not url:
            return ""
        return Badge.from_repo(self.repo_url).render()

    def get_badges(self):
        c = []
        for badge in self.badges:
            if isinstance(badge, str):
                c.append(Badge(image=badge))
            else:
                c.append(badge)
        if self.repo_url:
            c.append(Badge.from_repo(self.repo_url))
        return c


class Awesome(pydantic.BaseModel):
    items: Dict[str, List[Item]]


with open("./gen/template.jinja2", encoding="utf8") as f:
    template = jinja2.Template(f.read())

with open("./awesome.yaml", encoding="utf") as f:
    raw_data = yaml.safe_load(f)
    data = Awesome.parse_obj(raw_data)
    print(template.render(data=data.items))
