from __future__ import print_function
from flask import Flask, request
import json
import senti
import tfidf
import Cluster
import sys


app=Flask(__name__);

@app.route("/")
def main():
    return "Welcome!"


@app.route('/Review/', methods=['POST'])
def Review():
  obj = {}
  obj["id"] = request.values.get("id")
  obj["userID"] = request.values.get("userID")
  obj["reviewID"] = request.values.get("reviewID")
  obj["productID"] = request.values.get("productID")
  obj["rating"] = request.values.get("rating")
  obj["reviewText"] = request.values.get("reviewText")
  
  print( json.dumps(obj), file=sys.stderr)
  
  ret = senti.solve(obj["reviewText"],obj["rating"]); 
  ret["rev_id"] = obj["id"]
  
  return json.dumps(ret)

@app.route('/TFIDF/', methods=['POST'])
def TFIDF():
  content = request.get_json()
  reviews = []
  for data in content:
    reviews.append( data['reviewerText'] )
  
  print( reviews, file=sys.stderr)
    
  features = tfidf.solve(reviews)
  ret = []
  for d in features:
    ret.append( { 'Feature': d, 'Score' : features[d] } )
    
  return json.dumps( ret )
  

@app.route('/Cluster/', methods=['POST'])
def ClusterText():
  content = request.get_json()
  
  return Cluster.solve(content)
  
  
if __name__ == "__main__":
    app.run(host='0.0.0.0')
  
