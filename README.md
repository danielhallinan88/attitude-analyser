#attitude-analyser 
gunicorn --bind 0.0.0.0:5000 wsgi:application 

#Heroku 
https://attitude-analyzer.herokuapp.com/test 

#Analysis test
curl -d '{"text":"I like coffee. He likes tea."}'  -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1.0/analyze-text  | jq

curl -d '{"text":"I like coffee. He likes tea."}'  -H "Content-Type: application/json" -X POST http://attitude-analyzer.herokuapp.com/api/v1.0/analyze-text  | jq
