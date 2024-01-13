from dataclasses import dataclass
from pathlib import Path

import solara

# Declare reactive variables at the top level. Components using these variables
# will be re-executed when their values change.
sentence = solara.reactive("Solara makes our team more productive.")
word_limit = solara.reactive(10)


# in case you want to override the default order of the tabs
# route_order = ["/", "settings", "chat", "clickbutton", "technicalanaly", "dashboard"]
route_order = ["/"]

public_path = Path(__file__).parent.parent.joinpath("public")

groups = list(public_path.iterdir())
groups.sort(key=lambda x: int(x.name.replace(".md", "")))


@dataclass(frozen=True)
class GroupInfo:
    path: Path
    votes: tuple[bool | None, bool | None, bool | None] = (None, None, None)


@dataclass(frozen=True)
class GroupList:
    groups: list[GroupInfo]


state = solara.reactive(GroupList(groups=[GroupInfo(path=g) for g in groups]))


@solara.component
def GroupItem(group_info: GroupInfo, current_selection: solara.Reactive):
    # with solara.Row(justify="start"):
    solara.Button(
        f"Group {group_info.path.name.replace('.md', '')}",
        outlined=True,
        color="primary",
        style={"width": "100px"},
        on_click=lambda: current_selection.set(group_info.path),
    )
    # for v in group_info.votes:
    #     solara.Button(icon_name="mdi-checkbox-blank-circle-outline", text=True)


@solara.component
def Page():
    current_selection = solara.use_reactive(state.value.groups[0].path)

    with solara.Sidebar():
        with solara.Column():
            for group in state.value.groups:
                GroupItem(group, current_selection)

    with solara.Column(style={"padding-top": "30px"}):
        solara.Title("Minswap Catalyst Fund 11")
        with open(current_selection.value) as fr:
            solara.Markdown(fr.read())
