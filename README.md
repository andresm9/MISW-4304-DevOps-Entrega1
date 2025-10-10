# Introduccion

Para ejecutar el microservicio:

```bash
python application.py
```

## Endpoint

```GET /blacklists/<string:email>```

Devuelve ```{"exist":false}``` si el correo indicado en la URL no se encuentra en la base de datos

```POST /blacklists/```
Permite registrar un Correo en la lista negra.

#### Request Body
```
{
    "email": "test@example.com",
    "app_uuid": "{{$uuid}}",
    "blocked_reason": "Example Reason"
}
```
