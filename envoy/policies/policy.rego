package envoy.authz.allow

default allow = false

# Login без авторизации
allow {
  endswith(input.request.http.path, "/login")
}

# Users (любой путь внутри users)
allow {
  input.request.http.method == "GET"
  regex.match("^/users(/.*)?$", input.request.http.path)
  payload := decode_jwt(input.request.http.headers.authorization)
  payload.role == "USER"
}

# Orders (любой путь внутри orders)
allow {
  input.request.http.method == "GET"
  regex.match("^/orders(/.*)?$", input.request.http.path)
  payload := decode_jwt(input.request.http.headers.authorization)
  payload.role == "USER"
}

# Admin (любой путь внутри admin)
allow {
  input.request.http.method == "GET"
  regex.match("^/admin(/.*)?$", input.request.http.path)
  payload := decode_jwt(input.request.http.headers.authorization)
  payload.role == "ADMIN"
}

decode_jwt(token) = payload {
  [_, payload, _] := io.jwt.decode(token)
} else = {}

default response = {
  "allowed": false,
  "status_code": 403,
  "headers": {"content-type": "application/json"},
  "body": "{\"reason\": \"Forbidden\"}"
}

response = {
  "allowed": true,
  "status_code": 200,
  "headers": {"content-type": "application/json"}
} {
  allow
}
