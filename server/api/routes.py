from flask import Flask, request, Response, jsonify
from . import registrar
import json, base64
from server import app, zk




@app.route("/Service/<string:serviceName>")
def get_service(serviceName):
    print(zk.get_children("RoomR/Services/"), flush=True)
    if zk.exists("RoomR/Services/" + serviceName):
        data, stat = zk.get("RoomR/Services/" + serviceName)
        print(data, flush=True)
        return Response(response=data.decode("utf-8"))
    return Response(response="No service found with name: " + serviceName, status=404)


@app.route("/")
def test():
    print(zk.get_children("RoomR/Services/"), flush=True)
    return Response(response="TEST", status=200)

      






