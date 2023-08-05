import argparse
import json
import sys

import yaml
try:
    from .extensionRemover import remove_extensions
except ImportError:
    from extensionRemover import remove_extensions

input_format = []


def buildArgumentParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Remove vendor extensions from an OpenAPI document.')

    # Optional arguments
    parser.add_argument('--input-file', '-i', type=argparse.FileType('r'), dest='input',
                        nargs='*', metavar='file', help='Input file(s) to read. Default is stdin.')
    parser.add_argument('--output-file', '-o', type=argparse.FileType('w'), default=sys.stdout, dest='output',
                        nargs='*', metavar='file', help='Output file(s) to write the result. Default is stdout.')

    parser.add_argument('--extension', default='x-', nargs='*',
                        help='Extensions to remove. '
                             'This expression for example, "--extension x-amazon-apigateway-integration x-amazon-apigateway-any-method" will remove these amazon extensions from the input files.'
                             'A partial input is also acceptable, "--extension x-" will remove all extensions. This is the default behavior.')

    return parser


def read_document(doc: str) -> dict:
    try:
        data = json.load(doc)
        input_format.append('json')
        return data
    except Exception:
        pass

    try:
        data = json.loads(doc)
        input_format.append('json')
        return data
    except Exception:
        pass

    data = yaml.load(doc)
    input_format.append('yaml')
    return data


def main():
    argParser = buildArgumentParser()
    args = argParser.parse_args()
    if args.input is not None:
        docs = [read_document(x) for x in args.input]
    else:
        docs = "".join(sys.stdin.readlines())
        docs = [read_document(docs)]
    processed_docs = [remove_extensions(doc, args.extension) for doc in docs]

    for i in range(len(processed_docs)):

        if input_format[i] == 'json':
            json.dump(processed_docs[i], args.output[i] if isinstance(args.output, list) else args.output, indent=2)
        else:
            yaml.dump(processed_docs[i], args.output[i] if isinstance(args.output, list) else args.output,
                      default_flow_style=False)


if __name__ == '__main__':
    main()
