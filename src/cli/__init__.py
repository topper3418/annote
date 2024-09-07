from .parser import parser


def parse_and_run():
    args = parser.parse_args()
    args.func(args)

