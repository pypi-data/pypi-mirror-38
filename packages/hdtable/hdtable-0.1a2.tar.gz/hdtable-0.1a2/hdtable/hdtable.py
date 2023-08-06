from collections import defaultdict
from typing import Any, DefaultDict, Dict, List, Optional

import anytree

from hdtable.utils import lcmm


d_height = 2
not_found_string = "N/A"


class HdtableNode(anytree.Node):  # type: ignore
    """
    Represents a table cell.

    In the following sample table, there are 5 cells,
    with ``col 1`` and ``col 2`` being header cells.

    ::

                                   +--------+-------+
                                   | col 1  | col 2 | <─┬─ row height of ``col 2``
                                   +========+=======+ <─┘
        row height of ``xyz`` ─┬─> | xyz    | abc   |
                               ├─> |        +-------+
                               ├─> |        | def   | <─── row 5 starting row of ``def``
                               └─> +--------+-------+
                                    ││││││││
                                    └┴┴┼┴┴┴┘
                                       width of column 0

    :param column: The column index of the cell.
    :param content: The content of the cell which will be printed to table.
    :param data: The data the cell represents.
    :param row_height:
        The number of rows the cell occupy.
        For example, the ``xyz`` cell in the sample table occupies 4 rows,
        and the ``abc`` cell occupies 2 rows.
    :param starting_row:
        The first row of the cell with respect to the entire table.
    :param header: The node represents a header cell.
    """

    column: int
    content: str
    data: List[Dict]
    logical_parent: Optional[anytree.AnyNode]
    row_height: int
    starting_row: int
    header: bool

    def __init__(
        self, *args: Any, column: int = 0, header: bool = False, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.column = column
        self.header = header
        self.logical_parent = None

    @property
    def pathname(self) -> str:
        return "/".join([str(node.name) for node in self.path])


class Column:
    cells: List
    dtype: str
    index: int
    keys: List[str]
    parent: int
    width: int
    _domain: str
    _header: str

    @property
    def header(self) -> str:
        if hasattr(self, "_header") and self._header:
            return self._header
        else:
            return "{} {}".format(self.domain, self.dtype)

    @header.setter
    def header(self, header: str) -> None:
        self._header = header

    @property
    def domain(self) -> str:
        return self._domain

    @domain.setter
    def domain(self, domain: str) -> None:
        self._domain = domain

        if len(self.header) > self.width:
            self.width == 2 + len(self.header)

    def __init__(self, index: int, spec: Dict):
        self.cells = []
        self.index = index
        self.width = 0

        try:
            self.keys = spec["keys"]
        except KeyError:
            self.keys = []

        try:
            self.parent = spec["parent"]
        except KeyError:
            self.parent = 0

        try:
            self.dtype = spec["dtype"]
        except KeyError:
            self.dtype = "string"

        try:
            self.header = spec["header"]
        except KeyError:
            self.header = ""

        if self.parent > self.index:
            raise InvalidColumnSpecification(
                "A column's parent index cannot be greater than its own index."
            )

        try:
            self.domain = self.keys[0]
        except IndexError:
            if self.index == 0:
                self.domain = "root"
            else:
                self.domain = ""

    def add_cell(self, node: HdtableNode) -> None:
        self.cells.append(node)
        content_length = len(node.name)

        if content_length > self.width:
            self.width = content_length


def build_columns(specs: List[Dict]) -> List[Column]:
    """
    Build columns using column specifications.
    """

    columns: List[Column] = []

    for i in range(len(specs)):
        spec = specs[i]
        column = Column(i, spec)

        if not column.domain:
            try:
                column.domain = columns[column.parent].domain
            except IndexError:
                column.domain = "root"

        columns.append(column)

    return columns


class Hdtable:
    """
    A hierarchical data table (hdtable).

    :param data: The root data object from which all cells will be derived.
    :param headers:
        The content of the header row. Defaults to each column specification's
        last key.
    :param root:
        A special :py:class:`HdtableNode` that has column index -1 and
        no content. All cells must be descendents of the root node.
    :param widths:
        The column widths. They are computed when building the table.
    """

    columns: List[Column]
    data: Dict
    root: HdtableNode
    widths: List[int]
    _str: str

    def __init__(self, data: Dict, specs: List[Dict]) -> None:
        self.data = data
        self.columns = build_columns(specs)
        self.build_tree()

    def __str__(self) -> str:
        return self._str

    def build_table(self) -> None:
        self.root.row_height += 2
        s = [""] * (self.root.row_height + 1)

        for i, column in enumerate(self.columns):
            try:
                intersections = []
                next_column = self.columns[i + 1]
                prev_node_row_height = 0
                prev_node_starting_row = 1

                for node in next_column.cells:
                    node.starting_row = (
                        (prev_node_row_height + prev_node_starting_row)
                        if not node.header
                        else 1
                    )
                    prev_node_row_height = node.row_height
                    prev_node_starting_row = node.starting_row
                    intersections.append(
                        node.row_height + node.starting_row - 1
                    )
            except IndexError:
                intersections = []

            if column is not self.columns[0]:
                s[0] += "-" * (column.width + 2) + "+"
            else:
                s[0] += "+"

            for cell in column.cells:
                for i in range(
                    cell.starting_row, cell.starting_row + cell.row_height - 1
                ):
                    if cell is not self.root:
                        if i == cell.starting_row:
                            s[i] += " {}".format(cell.name) + " " * (
                                column.width - len(cell.name) + 1
                            )
                        else:
                            s[i] += " " * (column.width + 2)

                        s[i] += "|" if i not in intersections else "+"
                    else:
                        s[i] += "|" if i not in intersections else "+"

                if cell is not self.root:
                    c = "=" if cell.header else "-"
                    s[cell.starting_row + cell.row_height - 1] += (
                        c * (column.width + 2) + "+"
                    )
                else:
                    s[cell.starting_row + cell.row_height - 1] += "+"

        self._str = "\n".join(s)

    def build_column(self, index: int) -> None:
        column = self.columns[index]

        if index == 0:
            self.root = HdtableNode(
                "root", data=get_data(self.data, column.keys), starting_row=1
            )
            column.add_cell(self.root)
            return

        parent_header_node = self.columns[index - 1].cells[0]
        new_node = HdtableNode(
            column.header,
            column=index,
            parent=parent_header_node,
            row_height=d_height,
            starting_row=1,
            header=True,
        )
        column.add_cell(new_node)
        parent_column = self.columns[column.parent]

        for parent_cell in parent_column.cells:
            if parent_cell.header:
                continue

            data = get_data(parent_cell.data, column.keys)

            if column.dtype == "index":
                if not data:
                    new_node = HdtableNode(
                        "N/A", column=index, data=None, parent=parent_cell
                    )
                    column.add_cell(new_node)
                elif isinstance(data, list):
                    for i in range(len(data)):
                        new_node = HdtableNode(
                            str(i + 1),
                            column=index,
                            data=data[i],
                            parent=parent_cell,
                        )
                        column.add_cell(new_node)
                elif isinstance(data, dict):
                    for i, key in enumerate(data):
                        new_node = HdtableNode(
                            str(i + 1),
                            column=index,
                            data=data[key],
                            parent=parent_cell,
                        )
                        column.add_cell(new_node)
                else:
                    raise InvalidColumnSpecification(
                        "Unknown data type {} for column dtype {}".format(
                            type(data), column.dtype
                        )
                    )

            if column.dtype == "key":
                if not data:
                    new_node = HdtableNode(
                        "N/A", column=index, data=None, parent=parent_cell
                    )
                    column.add_cell(new_node)
                elif isinstance(data, dict):
                    for key, val in data.items():
                        new_node = HdtableNode(
                            key,
                            column=index,
                            data=data[key],
                            parent=parent_cell,
                        )
                        column.add_cell(new_node)
                else:
                    raise InvalidColumnSpecification(
                        "Unknown data type {} for column dtype {}".format(
                            type(data), column.dtype
                        )
                    )

            if column.dtype == "string":
                new_node = HdtableNode(
                    str(data) if data else "N/A",
                    column=index,
                    data=data,
                    parent=parent_cell,
                )
                column.add_cell(new_node)

    def build_tree(self) -> None:
        for i in range(0, len(self.columns)):
            self.build_column(i)

        self.compute_row_height(self.root)

        for col in self.columns:
            parent_groups: DefaultDict = defaultdict(list)

            for node in col.cells:
                if node.header:
                    node.row_height = d_height
                    continue

                if node is not self.root:
                    parent_groups[node.parent].append(node)

            for parent, group in parent_groups.items():
                units = sum([node.row_height for node in group])

                for node in group:
                    node.row_height = (
                        parent.row_height // units * node.row_height
                    )

        self.build_table()

    def compute_row_height(self, node: HdtableNode) -> int:
        if node.header:
            node.row_height = 0

            for child in node.children:
                self.compute_row_height(child)

            return 0

        if not node.children:
            node.row_height = 2
            return 2

        column_groups: DefaultDict = defaultdict(list)

        for n in node.children:
            column_groups[n.column].append(n)

        column_atomic_heights = []

        for column, group in column_groups.items():
            column_atomic_height = 0

            for n in group:
                n.row_height = self.compute_row_height(n)
                column_atomic_height += n.row_height

            column_atomic_heights.append(column_atomic_height)

        node.row_height = lcmm(*column_atomic_heights)
        return node.row_height


def get_data(data: Optional[Dict], keys: List[str]) -> Optional[Dict]:
    """
    Using one key at a time, access the member of ``data`` using keys.

    :param data: A dictionary containing arbitrary data.
    :param keys: A list of keys.
    """
    d = data

    for key in keys:
        if not d:
            return None

        try:
            d = d[key]
        except KeyError:
            d = None
            break

    return d


class InvalidColumnSpecification(Exception):
    pass
