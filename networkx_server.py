from flask import Flask, request
from typing import Dict
import json
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


@app.route('/nx/<string:function>', methods=['GET'])
def document_nx_function(function):
    try:
        nx_function = get_function_from_path(function)
    except AssertionError as e:
        return f"[network.{function}] is not a function", 400
    except Exception as e:
        print(e)
        return f"[network.{function}] not found", 404

    documenter = pydoc.HTMLDoc()
    return documenter.docroutine(nx_function)


@app.route('/nx/<string:function>', methods=['POST'])
def run_nx_function(function):
    try:
        nx_function = get_function_from_path(function)
    except AssertionError as e:
        return f"[network.{function}] is not a function", 400
    except Exception as e:
        print(e)
        return f"[network.{function}] not found", 404
    params = load_parameters(request.data)

    result = nx_function(**params)
    return str(result)


def get_function_from_path(path: str):
    module_and_function = path.rsplit(".", 1)
    function_name = module_and_function[-1]
    module_name = "networkx"
    if len(module_and_function) != 1:
        module_name += f".{module_and_function[0]}"
    module = importlib.import_module(module_name)
    function = getattr(module, function_name)
    assert isinstance(function, types.FunctionType)
    return function


def load_parameters(data) -> Dict:
    param_dict = json.loads(data)
    if param_dict.get("G"):
        param_dict["G"] = nx.node_link_graph(param_dict.get("G"))
    return param_dict
