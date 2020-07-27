# NetworkX Server
Proof of concept for providing networkx functionality as REST API.  

NetworkX implements a lot of graph algorithms, some of which are very difficult to implement. 
By setting up this NetworkX server, we can use those algorithms easily when not working in Python.  

A GET request to `localhost:5000/nx/{nx_function_name}' returns the documentation page of that function. 

A POST request, where the body contains a `kwargs` like JSON, will run the requested function and return the result. 
Graps in the input should be given in node_link format, and is only supported for parameters named `G`.  
Functions that modify or output the graph are not currently supported.  
