import json
import numpy as np
import pandas as pd
from os import path
from collections import Counter, defaultdict
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def non_empty_string(string):
    if isinstance(string, str):
        return len(string) > 0
    return string is None or np.isnan(string)


def get_type(values):

    def inner(one_value):
        if isinstance(one_value, (bool, np.bool, np.bool_)):
            return "bool"
        elif isinstance(one_value, str):
            # decide between a string and enum
            # simple heuristic: % of unique elements after removing empty strings
            # non_empty = list(filter(non_empty_string, values))
            # if len(non_empty) > 0:
            #     perc_unique = 100.0 * len(set(non_empty)) / len(non_empty)
            #     if 0.0 < perc_unique < 50.0:
            #         return "enum"
            return "string"
        else:
            # is numeric -- decide between int and float by attempting a bit shift (raises Exception for float)
            try:
                one_value >> 2
                return "int32"
            except Exception:
                return "float"

    # choose the mode of the returned type on a random subset of the values
    subset = np.random.choice(values, size=int(0.2 * len(values)))
    types = list(map(inner, subset))
    return pd.Series(types).value_counts().sort_values().index[0]


def get_types(records):
    df = pd.DataFrame(records)
    return {
        col: get_type(df[col])
        for col in df.columns
    }


def write_proto_file(types, out_fn):
    with open(out_fn, 'w') as fp:
        fp.write(
            "// [START declaration]\n"
            "syntax = \"proto3\";\n"
            "// [END declaration]\n"
            "\n"
            "// [START messages]\n"
            "message Transaction {\n"
        )

        for i, (name, _type) in enumerate(types.items()):
            fp.write("    {} {} = {};\n".format(_type, name, i + 1))

        fp.write(
            "}\n"
            "// [END messages]\n"
        )


def protofy(records, out_fn):
    types = get_types(records)
    write_proto_file(types, out_fn)


def get_clargs():
    # create the parser
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(dest="data_file",
        help="Path to json file with top-level key 'data' whose value is a list of JSON records.")
    parser.add_argument("-o", "--proto-file", required=False, default=None,
        help="Path where the created protocol file should be written. If not given, will be the <data file>.proto")

    # parse the arguments
    args = parser.parse_args()

    # create args.proto_file if not provided
    if not args.proto_file:
        args.proto_file = "{}.proto".format(path.splitext(path.basename(args.data_file))[0])
    print(args.proto_file)

    return args


if __name__ == '__main__':
    args = get_clargs()
    with open(args.data_file) as fp:
        txns = json.load(fp)['data']
    protofy(txns, args.proto_file)
