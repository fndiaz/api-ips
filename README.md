# ip-ranges
External IPs 

## List IPs
```
curl --request GET 'https://ip-ranges.example.com.br'
```

## List IPs by Service
```
curl --request GET 'https://ip-ranges.example.com.br/service/NAME_SERVICE'
```

## Add IP
```
curl --request POST 'https://ip-ranges.example.com.br/' \
--header 'Content-Type: application/json' \
--data-raw '{
	"ip": "8.8.8.8/32",
    "service": "name-service",
    "token":"JAhMkQj2THxL25Ty"
}'
```

## Delete IP
```
curl --location --request POST 'https://ip-ranges.example.com.br/delete' \
--header 'Content-Type: application/json' \
--data-raw '{
      "ip": "8.8.8.8/32",
      "service": "name-service",
     "token":"JAhMkQj2THxL25Ty"
	
}'
```
