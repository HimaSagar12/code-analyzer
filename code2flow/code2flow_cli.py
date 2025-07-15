#!/usr/bin/env python3

import argparse
import logging
import os
import sys

from code2flow.engine import code2flow, generate_image, LANGUAGES

def main():
    parser = argparse.ArgumentParser(
        description="Generate flow charts from your source code.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        'sources', metavar='sources', nargs='+',
        help='source code file/directory paths.'
    )
    parser.add_argument(
        '--output', '-o', default='output.png',
        help='output image file path (e.g., output.png).'
    )
    parser.add_argument(
        '--language', choices=LANGUAGES.keys(),
        help='process this language and ignore all other files. If omitted, '
             'use the suffix of the first source file.'
    )
    parser.add_argument(
        '--hide-legend', action='store_true',
        help='Omit the legend from the output.'
    )
    parser.add_argument(
        '--no-grouping', action='store_true',
        help='Don\'t group functions into namespaces in the final output.'
    )
    parser.add_argument(
        '--no-trimming', action='store_true',
        help='Show all functions/namespaces whether or not they connect to anything.'
    )
    parser.add_argument(
        '--skip-parse-errors', action='store_true',
        help='Skip files that the language parser fails on.'
    )
    parser.add_argument(
        '--quiet', '-q', action='store_true',
        help='Suppress most logging.'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Add more logging.'
    )

    args = parser.parse_args()

    level = logging.INFO
    if args.verbose and args.quiet:
        raise AssertionError("Passed both --verbose and --quiet flags")
    if args.verbose:
        level = logging.DEBUG
    if args.quiet:
        level = logging.WARNING

    logging.basicConfig(format="Code2Flow: %(message)s", level=level)

    try:
        file_groups, all_nodes, edges = code2flow(
            raw_source_paths=args.sources,
            language=args.language,
            hide_legend=args.hide_legend,
            no_grouping=args.no_grouping,
            no_trimming=args.no_trimming,
            skip_parse_errors=args.skip_parse_errors,
            # subset_params and lang_params are not exposed via CLI for simplicity
        )

        generate_image(
            file_groups,
            all_nodes,
            edges,
            args.output,
            hide_legend=args.hide_legend,
            no_grouping=args.no_grouping
        )
        logging.info(f"Flowchart generated successfully as {args.output}")

    except AssertionError as e:
        logging.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
