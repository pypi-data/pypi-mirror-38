import os
import re
import json
import yaml
import argparse
import subprocess
import collections


parser = argparse.ArgumentParser(fromfile_prefix_chars="@")
parser.add_argument("scriptpath")
parser.add_argument("--test", action="store_true", default=False)
parser.add_argument("--python", type=str, default="python")
parser.add_argument("--run-module", action="store_true", default=False)
parser.add_argument("--module-path", type=str, default=None)
parser.add_argument("--args", type=str, action="append", default=[])
parser.add_argument("--precedence", type=str, default="commandline",
                    choices=["commandline", "configfile"],
                    help="indicates argument precedence in case of argument "
                         "conflicts. 1) commandline: command-line arguments "
                         "will have higher importance. 2) configfile: config "
                         "file arguments will have higher importance.")


def dict_to_argv(dic: dict):
    argv = []
    for k, v in dic.items():
        assert isinstance(k, str)
        arg = f"--{k}"
        if v is None:
            continue
        elif isinstance(v, str):
            argv.append(arg)
            argv.append(v)
        elif isinstance(v, collections.Sequence):
            for val in v:
                argv.append(arg)
                argv.append(str(val))
        elif isinstance(v, bool):
            if v:
                argv.append(arg)
        else:
            argv.append(arg)
            argv.append(str(v))
    return argv


def parse_argv(argv: list):
    argv = [a for a in argv]
    args = {}
    key = None
    val = None

    def flush(key, val):
        if key is None:
            return key, val
        if val is None:
            val = True
        args[key] = val
        return None, None

    while argv:
        arg = argv.pop(0)
        if arg.startswith("--"):
            key, val = flush(key, val)
            key = arg[2:]
        else:
            val = arg
            key, val = flush(key, val)
    return args


def load_args(path):
    filename = os.path.basename(path)

    if "." in filename:
        extname = os.path.splitext(filename)[-1]
    else:
        extname = None

    if extname == ".json":
        load_cls = json.load
    elif extname == ".yml":
        load_cls = yaml.load
    else:
        raise ValueError(f"unknown extension: {extname}")

    with open(path, "r") as f:
        args = load_cls(f)

    argv = dict_to_argv(args)
    return argv


def prepare_argv(args):
    argv = []
    for arg_path in args.args:
        arg_dir = os.path.dirname(os.path.realpath(arg_path))
        arg_name = os.path.basename(os.path.realpath(arg_path))
        cargv = load_args(arg_path)
        cargv = [
            v.replace("{%config-dir%}", arg_dir)
             .replace("{%working-dir%}", os.getcwd())
             .replace("{%config-name%}", arg_name)
             .replace("{%module-name%}", args.scriptpath)
            if isinstance(v, str) else v
            for v in cargv
        ]
        argv.extend(cargv)
    return argv


def resolve_vars(argv, vars):
    format_pat = re.compile(r"{[a-zA-Z0-9\-_]+\}")
    delta = True
    while delta:
        delta = False
        for i in range(len(argv)):
            arg = argv[i]
            if format_pat.search(arg) is not None:
                arg_f = arg.format(**vars)
                delta = arg_f != arg
                argv[i] = arg_f

    return argv


def push_pythonpath(env, path):
    env["PYTHONPATH"] = f"{path}:" + env.get("PYTHONPATH", "")
    return env


def run_script(parser):
    args, misc_argv = parser.parse_known_args()
    argdict = parse_argv(prepare_argv(args))
    misc_argdict = parse_argv(misc_argv)

    if args.precedence == "commandline":
        argdict.update(misc_argdict)
    elif args.precedence == "configfile":
        misc_argdict.update(argdict)
        argdict = misc_argdict
    else:
        raise ValueError(f"unrecognized precedence type: {args.precedence}")

    argv = dict_to_argv(argdict)
    argv = resolve_vars(argv, argdict)
    env = os.environ.copy()
    if args.run_module:
        env = push_pythonpath(env, args.module_path)
        argv = [args.python, "-m", args.scriptpath] + argv
    else:
        argv = [args.python, args.scriptpath] + argv
    if args.test:
        print(" ".join(argv))
    else:
        subprocess.call(argv, env=env)


if __name__ == "__main__":
    run_script(parser)