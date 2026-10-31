"""Fold the project-type gates out of a leaf template's template/ directory.

A leaf template's projects are always Standard, so in its template/ sources
`is_template` and `is_extensible` are always false and `is_standard` always true.
This rewrites every `{% if %}`/`{% elif %}` that tests them: a branch that can't
render goes, a branch that always renders loses its tags, and a mixed condition
keeps only the part that still varies (`is_template or using_github` becomes
`using_github`). Path names fold the same way. Rendering a folded file gives
the same output as rendering the original, whitespace control included.

Usage: python fold_leaf_gates.py <template directory>
"""

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import jinja2
from jinja2 import nodes

KNOWN = {"is_template": False, "is_extensible": False, "is_standard": True}
TEMPLATE_SUFFIX = ".jinja"

# A raw block, a comment, a statement, or an expression, with its whitespace-control
# markers. A raw block's content is never parsed.
_TAG = re.compile(
    r"(?P<raw>\{%(?P<raw_l>-?)\s*raw\s*-?%\}.*?\{%-?\s*endraw\s*(?P<raw_r>-?)%\})"
    r"|(?P<comment>\{#(?P<c_l>-?).*?(?P<c_r>-?)#\})"
    r"|(?P<stmt>\{%(?P<s_l>-?)\s*(?P<body>.*?)\s*(?P<s_r>-?)%\})"
    r"|(?P<expr>\{\{(?P<e_l>-?).*?(?P<e_r>-?)\}\})",
    re.DOTALL,
)
_ENV = jinja2.Environment()  # noqa: S701 (parses expressions only; renders nothing)


@dataclass(eq=False)
class Piece:
    """Literal text between two tags."""

    text: str


@dataclass(eq=False)
class Tag:
    """A tag kept verbatim, or the head of an if-construct branch."""

    raw: str
    lstrip: bool
    rstrip: bool
    left: Piece | None = None
    right: Piece | None = None
    keyword: str = ""
    condition: str = ""


@dataclass(eq=False)
class IfBlock:
    """An if/elif/else/endif construct and its branch bodies."""

    branches: list[tuple[Tag, list]] = field(default_factory=list)
    endif: Tag | None = None


def _lex(source: str) -> list:
    items: list = []
    position = 0
    for match in _TAG.finditer(source):
        items.append(Piece(source[position : match.start()]))
        if match["raw"]:
            tag = Tag(match[0], bool(match["raw_l"]), bool(match["raw_r"]))
        elif match["comment"]:
            tag = Tag(match[0], bool(match["c_l"]), bool(match["c_r"]))
        elif match["expr"]:
            tag = Tag(match[0], bool(match["e_l"]), bool(match["e_r"]))
        else:
            keyword, _, condition = match["body"].partition(" ")
            tag = Tag(match[0], bool(match["s_l"]), bool(match["s_r"]))
            tag.keyword, tag.condition = keyword, condition.strip()
        items.append(tag)
        position = match.end()
    items.append(Piece(source[position:]))
    for index, item in enumerate(items):
        if isinstance(item, Tag):
            item.left, item.right = items[index - 1], items[index + 1]
    return items


def _parse(items: list) -> list:
    """Nest the flat item list into IfBlocks.

    Returns:
        The top-level body.

    Raises:
        ValueError: if an `{% if %}` has no `{% endif %}`.

    """
    root: list = []
    stack: list[tuple[IfBlock, list]] = []
    body = root
    for item in items:
        keyword = getattr(item, "keyword", "")
        if keyword == "if":
            block = IfBlock()
            body.append(block)
            stack.append((block, body))
            body = []
            block.branches.append((item, body))
        elif keyword in ("elif", "else"):
            body = []
            stack[-1][0].branches.append((item, body))
        elif keyword == "endif":
            block, body = stack.pop()
            block.endif = item
        else:
            body.append(item)
    if stack:
        raise ValueError("unclosed {% if %}")
    return root


def _tests_known(node: nodes.Node) -> bool:
    names = [node, *node.find_all(nodes.Name)]
    return any(isinstance(n, nodes.Name) and n.name in KNOWN for n in names)


def _simplify(node: nodes.Node) -> bool | nodes.Node:
    """Substitute KNOWN into a condition.

    Returns:
        True or False when the condition no longer varies, else the reduced node.

    Raises:
        ValueError: if a project-type name sits inside anything but and/or/not.

    """
    if isinstance(node, nodes.Name) and node.name in KNOWN:
        return KNOWN[node.name]
    if isinstance(node, nodes.Not):
        inner = _simplify(node.node)
        return (not inner) if isinstance(inner, bool) else nodes.Not(inner)
    if isinstance(node, (nodes.And, nodes.Or)):
        absorbing = isinstance(node, nodes.Or)  # True absorbs `or`; False absorbs `and`
        left, right = _simplify(node.left), _simplify(node.right)
        if absorbing in (left, right):
            return absorbing
        if isinstance(left, bool):
            return right
        if isinstance(right, bool):
            return left
        return type(node)(left, right)
    if _tests_known(node):
        raise ValueError(f"can't fold a project-type gate inside {node!r}")
    return node


def _emit(node: nodes.Node, parent: type | None = None) -> str:
    if isinstance(node, nodes.Name):
        return node.name
    if isinstance(node, nodes.Not):
        return "not " + _emit(node.node, nodes.Not)
    if isinstance(node, (nodes.And, nodes.Or)):
        word = " and " if isinstance(node, nodes.And) else " or "
        text = _emit(node.left, type(node)) + word + _emit(node.right, type(node))
        return text if parent in (None, type(node)) else f"({text})"
    raise ValueError(f"can't write {node!r} back as a condition")


def _condition(text: str) -> bool | str | None:
    """Fold one condition.

    Returns:
        True or False when it no longer varies, the reduced condition text when
        it changed, or None when it tests none of KNOWN.

    """
    test = _ENV.parse("{% if " + text + " %}{% endif %}").body[0].test
    if not _tests_known(test):
        return None
    folded = _simplify(test)
    return folded if isinstance(folded, bool) else _emit(folded)


def _retag(tag: Tag, keyword: str, condition: str | None) -> Tag:
    """Copy `tag` with a new keyword and condition, keeping its markers and neighbors.

    Returns:
        The new tag.

    """
    head = f"{keyword} {condition}" if condition else keyword
    raw = (
        "{%"
        + ("-" if tag.lstrip else "")
        + f" {head} "
        + ("-" if tag.rstrip else "")
        + "%}"
    )
    return Tag(
        raw, tag.lstrip, tag.rstrip, tag.left, tag.right, keyword, condition or ""
    )


def _choose(block: IfBlock) -> list[tuple[Tag | None, list]]:
    """Fold each branch condition of `block`.

    Returns:
        The branches that can still render, each under its (possibly rewritten)
        tag; a single branch under None when it always renders and needs no tags.

    """
    kept: list[tuple[Tag | None, list]] = []
    for tag, branch in block.branches:
        value = True if tag.keyword == "else" else _condition(tag.condition)
        if value is False:
            continue
        if value is True:
            if not kept:
                return [(None, branch)]
            otherwise = tag if tag.keyword == "else" else _retag(tag, "else", None)
            kept.append((otherwise, branch))
            break
        keyword = "elif" if kept else "if"
        condition = tag.condition if value is None else value
        unchanged = (keyword, condition) == (tag.keyword, tag.condition)
        kept.append((tag if unchanged else _retag(tag, keyword, condition), branch))
    return kept


def _fold(body: list, dropped: list[Tag]) -> list:
    """Fold every IfBlock in `body`, recording each tag it removes in `dropped`.

    Returns:
        The folded body, as Pieces and Tags.

    """
    out: list = []
    for item in body:
        if not isinstance(item, IfBlock):
            out.append(item)
            continue
        kept = _choose(item)
        kept_ids = {id(tag) for tag, _ in kept}
        dropped.extend(tag for tag, _ in item.branches if id(tag) not in kept_ids)
        if not kept or kept[0][0] is None:
            dropped.append(item.endif)
            for _, branch in kept:
                out.extend(_fold(branch, dropped))
            continue
        for tag, branch in kept:
            out.append(tag)
            out.extend(_fold(branch, dropped))
        out.append(item.endif)
    return out


def _strip(text: str, *, left: bool, right: bool) -> str:
    if left:
        text = text.lstrip()
    if right:
        text = text.rstrip()
    return text


def _marker_holds(
    neighbor: object, beyond: object, own: Piece | None, stripped: set[int]
) -> bool:
    """Whether a kept tag's strip marker still strips exactly what it did.

    It does when the piece now beside the tag is either the tag's own piece or one
    that side gets stripped anyway, and the strip stops inside it: at text, or at
    the tag beyond it. Past a dropped tag, the next piece would be stripped too.

    Returns:
        True to keep the marker.

    """
    return (
        isinstance(neighbor, Piece)
        and (bool(neighbor.text.strip()) or not isinstance(beyond, Piece))
        and (neighbor is own or id(neighbor) in stripped)
    )


def _at(items: list, index: int) -> object:
    return items[index] if 0 <= index < len(items) else None


def fold(source: str) -> str:
    """Fold the project-type gates out of one template file's source.

    Jinja strips at lex time, so a `{%-` always strips its own left piece, whatever
    renders. A dropped tag's stripping is applied to its pieces by hand. A kept tag
    keeps its marker while it strips the same text it did (see _marker_holds);
    otherwise the strip is applied by hand and the marker removed.

    Returns:
        The folded source.

    """
    items = _lex(source)
    dropped: list[Tag] = []
    out = _fold(_parse(items), dropped)
    dropped_ids = {id(tag) for tag in dropped}
    strip_left: set[int] = set()
    strip_right: set[int] = set()
    for tag in (
        item for item in items if isinstance(item, Tag) and id(item) in dropped_ids
    ):
        if tag.lstrip:
            strip_right.add(id(tag.left))
        if tag.rstrip:
            strip_left.add(id(tag.right))
    for index, item in enumerate(out):
        if not isinstance(item, Tag):
            continue
        before, after = _at(out, index - 1), _at(out, index + 1)
        # A marker that holds does the stripping itself, so its neighbor stays as
        # written; one that doesn't is removed and its own piece stripped by hand.
        if item.lstrip:
            if _marker_holds(before, _at(out, index - 2), item.left, strip_right):
                strip_right.discard(id(before))
            else:
                strip_right.add(id(item.left))
                item.raw = item.raw[:2] + item.raw[3:]
        if item.rstrip:
            if _marker_holds(after, _at(out, index + 2), item.right, strip_left):
                strip_left.discard(id(after))
            else:
                strip_left.add(id(item.right))
                item.raw = item.raw[:-3] + item.raw[-2:]
    return "".join(
        item.raw
        if isinstance(item, Tag)
        else _strip(
            item.text, left=id(item) in strip_left, right=id(item) in strip_right
        )
        for item in out
    )


def fold_directory(root: Path) -> None:
    """Fold every template file's contents and every path name under `root`."""
    for path in sorted(root.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if path.is_file() and path.name.endswith(TEMPLATE_SUFFIX):
            source = path.read_bytes().decode("utf-8")
            folded = fold(source)
            if folded != source:
                path.write_bytes(folded.encode("utf-8"))
        name = fold(path.name)
        if name != path.name:
            path.rename(path.with_name(name))


if __name__ == "__main__":
    fold_directory(Path(sys.argv[1]))
