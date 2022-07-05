#!/bin/bash

# Start the first process
python3 run_client.py --ip $1 &
      
# Start the second process
python3 run_server.py --ip $1 --collection $2 &

# Start the third process
python3 -m http.server --d dist/ 8001 
  
   
