import locale
import readline

from argparse import ArgumentParser

from . import constants
from . import utils
from . import dictionaries
from .completer import DictCompleter


def check_zdict_dir_and_db():
    utils.create_zdict_dir_if_not_exists()
    utils.create_zdict_db_if_not_exists()


def user_set_encoding_and_is_utf8():
    # Check user's encoding settings
    try:
        (lang, enc) = locale.getdefaultlocale()
    except ValueError:
        print("Didn't detect your LC_ALL environment variable.")
        print("Please export LC_ALL with some UTF-8 encoding.")
        return False
    else:
        if enc != "UTF-8":
            print("zdict only works with encoding=UTF-8, ")
            print("but you encoding is: {} {}".format(lang, enc))
            print("Please export LC_ALL with some UTF-8 encoding.")
            return False
    return True


def get_command_line_args():
    # parse args
    parser = ArgumentParser(prog='zdict')

    parser.add_argument(
        'words',
        metavar='word',
        type=str,
        nargs='*',
        help='Words for searching its translation'
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version='%(prog)s-' + constants.VERSION
    )

    parser.add_argument(
        "-d", "--disable-db-cache",
        default=False,
        action="store_true",
        help="Temporarily not using the result from db cache.\
              (still save the result into db)"
    )

    parser.add_argument(
        "-t", "--query-timeout",
        type=float,
        default=5.0,
        action="store",
        help="Set timeout for every query. default is 5 seconds."
    )

    parser.add_argument(
        "-sp", "--show-provider",
        default=False,
        action="store_true",
        help="Show the dictionary provider of the queried word"
    )

    parser.add_argument(
        "-su", "--show-url",
        default=False,
        action="store_true",
        help="Show the url of the queried word"
    )

    parser.add_argument(
        "-dt", "--dict",
        default="yahoo",
        action="store",
        choices=list(filter(lambda attr: not attr.startswith('_'), dir(dictionaries))),
        help="Choose the dictionary you want. (default: yahoo)"
    )

    parser.add_argument(
        "-V", "--verbose",
        default=False,
        action="store_true",
        help="Show more information for the queried word.\
        (If the chosen dictionary have implemented verbose related functions)"
    )

    return parser.parse_args()


def interactive_mode(zdict, args):
    # configure readline and completer
    readline.parse_and_bind("tab: complete")
    readline.set_completer(DictCompleter().complete)
    zdict.loop_prompt(args)

def execute_zdict(args):
    zdict = getattr(dictionaries, args.dict)()

    if args.words:
        for w in args.words:
            zdict.lookup(w, args)
    else:
        interactive_mode(zdict, args)

def main():
    if user_set_encoding_and_is_utf8():
        check_zdict_dir_and_db()
        args = get_command_line_args()
        execute_zdict(args)
    else:
        exit()
