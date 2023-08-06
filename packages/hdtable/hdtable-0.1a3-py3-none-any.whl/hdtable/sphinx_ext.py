from io import StringIO
import os
from typing import Dict

from docutils import nodes, statemachine
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.tables import Table
from docutils.utils import SystemMessagePropagation
import yaml

from hdtable.hdtable import Hdtable


class HdtableDirective(Table):
    final_argument_whitespace = True
    has_content = True
    option_spec = {
        "class": directives.class_option,
        "name": directives.unchanged,
        "data-source": directives.unchanged_required,
    }

    def run(self):
        if not self.content:
            warning = self.state_machine.reporter.warning(
                'Content block expected for the "%s" directive; none found.'
                % self.name,
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno,
            )
            return [warning]

        env = self.state.document.settings.env

        try:
            data_source_file = os.path.join(
                env.srcdir, self.options["data-source"]
            )
        except KeyError:
            error = self.state_machine.reporter.error(
                "The data-source option is required.",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno,
            )
            raise SystemMessagePropagation(error)

        with open(data_source_file, "r") as f:
            d = yaml.safe_load(f)

        specs = yaml.safe_load(StringIO("\n".join(self.content)))
        node = nodes.Element()
        hdtable = Hdtable(d, specs)
        self.state.nested_parse(
            statemachine.StringList(str(hdtable).splitlines()),
            self.content_offset,
            node,
        )

        if len(node) != 1 or not isinstance(node[0], nodes.table):
            error = self.state_machine.reporter.error(
                'Error parsing content block for the "%s" directive: exactly '
                "one table expected." % self.name,
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno,
            )
            return [error]

        table_node = node[0]
        table_node["classes"] += self.options.get("class", [])
        self.add_name(table_node)
        title, messages = self.make_title()

        if title:
            table_node.insert(0, title)

        return [table_node] + messages


def setup(app) -> Dict:
    app.add_directive("hdtable", HdtableDirective)

    return {"version": "0.1a2"}
