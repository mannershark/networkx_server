from flask import Flask, request
import networkx as nx
import logging
import importlib
import inspect
import pydoc
import types

app = Flask(__name__)


@app.route('/healthcheck')
def healthcheck():
    return "ok!", 200


@app.route('/nx/<string:function>')
def run_nx_function(function):
    try:
        nx_function = get_function(function)
        assert isinstance(nx_function, types.FunctionType)
    except AssertionError as e:
        return f"[network.{function}] is not a function", 400
    except Exception as e:
        print(e)
        return f"[network.{function}] not found", 404

    documenter = pydoc.HTMLDoc()
    return documenter.docroutine(nx_function)


def get_function(path: str):
    module_and_function = path.rsplit(".", 1)
    function_name = module_and_function[-1]
    module_name = "networkx"
    if len(module_and_function) != 1:
        module_name += f".{module_and_function[0]}"
    module = importlib.import_module(module_name)
    return getattr(module, function_name)
