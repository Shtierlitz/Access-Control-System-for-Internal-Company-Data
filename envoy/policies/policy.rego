package envoy.authz

default allow = false

# login — доступен всем
allow {
  startswith(input.request.http.path, "/login")
}

# users — доступ с любой ролью
allow {
  token := input.request.http.headers.authorization
  [_, payload, _] := io.jwt.decode(token)
  role := payload["role"]
  startswith(input.request.http.path, "/users")
}

# orders — только USER
allow {
  token := input.request.http.headers.authorization
  [_, payload, _] := io.jwt.decode(token)
  role := payload["role"]
  startswith(input.request.http.path, "/orders")
  role == "USER"
}

# admin — только ADMIN
allow {
  token := input.request.http.headers.authorization
  [_, payload, _] := io.jwt.decode(token)
  role := payload["role"]
  startswith(input.request.http.path, "/admin")
  role == "ADMIN"
}
