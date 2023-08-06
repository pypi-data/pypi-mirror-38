import antlr4  # type: ignore
import pybars
from pybars3_extensions import helpers

from thriftgen.model.file_loader import FileLoader

from thriftgen.parser.ThriftLexer import ThriftLexer
from thriftgen.parser.ThriftParser import ThriftParser

import argparse


def main() -> None:
    parser = argparse.ArgumentParser("Thrift generator for simple people.")

    parser.add_argument("--out",
                        required=True,
                        help="output file")
    parser.add_argument("--template",
                        required=True,
                        help="template file to use")
    parser.add_argument("thrift_files",
                        metavar="file.thrift",
                        nargs=1,
                        help="thrift file to process")

    args = parser.parse_args()

    for file_name in args.thrift_files:
        with open(file_name, 'r', encoding='utf-8') as f:
            lexer = ThriftLexer(antlr4.InputStream(f.read()))

        token_stream = antlr4.CommonTokenStream(lexer)

        thrift_parser = ThriftParser(token_stream)

        tree_walker = antlr4.ParseTreeWalker()

        file_loader = FileLoader(name=file_name)
        tree_walker.walk(file_loader, thrift_parser.document())

        model = file_loader.thrifty_file

        # ====================================================
        # generate the file
        # ====================================================
        with open(args.template, 'r', encoding='utf-8') as template_file:
            template = template_file.read()

        hbs = pybars.Compiler().compile(source=template)
        with open(args.out, 'w', encoding='utf-8') as output_file:
            output_file.write(hbs(model, helpers=helpers))


if __name__ == '__main__':
    main()
