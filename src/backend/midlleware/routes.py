"Lista das rotas publicas e privadas (path e metodo)"

#Rotas que não exigem token
PUBLIC_ROUTES = [
    {"path": "/auth/register", "method": "POST"},
    {"path": "/auth/login", "method": "POST"},

    {"path": "/events", "method": "GET"},
    {"path": "/events/{id}", "method": "GET"},

    {"path": "/posts", "method": "GET"},
    {"path": "/posts/{id}", "method": "GET"},

    {"path": "/forms", "method": "GET"},

    {"path": "/attendance/{ra}", "method": "GET"},
]

#Rotas que exigem token de admin
PRIVATE_ROUTES = [
    {"path": "/admin/events", "method": "GET"},
    {"path": "/admin/events", "method": "POST"},
    {"path": "/admin/events/{id}", "method": "GET"},
    {"path": "/admin/events/{id}", "method": "PUT"},
    {"path": "/admin/events/{id}", "method": "DELETE"},

    {"path": "/admin/posts", "method": "GET"},
    {"path": "/admin/posts", "method": "POST"},
    {"path": "/admin/posts/{id}", "method": "GET"},
    {"path": "/admin/posts/{id}", "method": "PUT"},
    {"path": "/admin/posts/{id}", "method": "DELETE"},

    {"path": "/admin/forms", "method": "GET"},
    {"path": "/admin/forms", "method": "POST"},
    {"path": "/admin/forms/{id}", "method": "GET"},
    {"path": "/admin/forms/{id}", "method": "PUT"},
    {"path": "/admin/forms/{id}", "method": "DELETE"},

    {"path": "/admin/committees", "method": "GET"},
    {"path": "/admin/committees", "method": "POST"},
    {"path": "/admin/committees/{id}", "method": "GET"},
    {"path": "/admin/committees/{id}", "method": "PUT"},
    {"path": "/admin/committees/{id}", "method": "DELETE"},

    {"path": "/admin/students", "method": "GET"},
    {"path": "/admin/students", "method": "POST"},
    {"path": "/admin/students/{id}", "method": "GET"},
    {"path": "/admin/students/{id}", "method": "PUT"},
    {"path": "/admin/students/{id}", "method": "DELETE"},

    {"path": "/admin/meetings", "method": "GET"},
    {"path": "/admin/meetings", "method": "POST"},
    {"path": "/admin/meetings/{id}", "method": "GET"},
    {"path": "/admin/meetings/{id}", "method": "PUT"},
    {"path": "/admin/meetings/{id}", "method": "DELETE"},

    {"path": "/admin/attendances", "method": "GET"},
    {"path": "/admin/attendances", "method": "POST"},
    {"path": "/admin/attendances/{id}", "method": "GET"},
    {"path": "/admin/attendances/{id}", "method": "PUT"},
    {"path": "/admin/attendances/{id}", "method": "DELETE"},

    {"path": "/admin/users", "method": "GET"},
    {"path": "/admin/users", "method": "POST"},
    {"path": "/admin/users/{id}", "method": "GET"},
    {"path": "/admin/users/{id}", "method": "PUT"},
    {"path": "/admin/users/{id}", "method": "DELETE"},
]
