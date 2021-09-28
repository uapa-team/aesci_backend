# aesci_backend

## Instalación del backend (Funciona tanto en Windows como en Linux)

0. En caso de no tener Python, instalarlo la versión 3.X desde [la página oficial](https://www.python.org/downloads/).

1. Descargar o clonar el repositorio.

2. En la carpeta principal, crear un entorno virtual:

`python3 -m venv tutorial-env` ⚠️¹²

3. Activar entorno virtual

`source ./bin/activate`

En Windows, usar este comando:

`tutorial-env\Scripts\activate.bat`

4. Ejecutar pip con los siguientes

    ```
    pip install django
    pip install djangorestframework
    pip install djangorestframework-simplejwt
    pip install django-cors-headers
    pip install django_auth_ldap ⚠️³
    pip install psycopg2
    pip install drf_spectacular
    pip install djangorestframework-simplejwt
    pip install requests
    ```

5. Conectarse a la VPN

    5.1 En Windows: En caso de no tener instalada la VPN, buscar en el Drive compartido de la UAPA un archivo llamado `VPN_Cisco.msi` para instalar Cisco Any Connect.
    5.2 Una vez instalado, permite el acceso a redes no seguras.
    5.3 Logearse con las credenciales de la UN.

6. Abrir otra terminal y correr

`ssh -L 5432:127.0.0.1:5432 uapapp-admin@168.176.26.202`

7. Correr el comando

`python3 manage.py runserver`⚠️¹

## ⚠️ Problemas comunes ⚠️

<!-- Aquí van los problemas comunes que se encuentren -->

### 1. La terminal/consola no reconoce el comando python3

Es posible usar simplemente el comando `python`. Por lo general se usa `python3` cuando se tienen varias versiones de Python en la máquina.


### 2. La terminal/consola no reconoce ni el comando python3 ni python y me aparece la Windows Store

Esto se debe porque al momento de instalar Python, en la primera pestaña, no se agregó el PATH de Python.

### 3. Instalación de la libreria LDAP da problemas

Probablemente, el comando `pip install django_auth_ldap` genere problemas.

- Colocar el comando `python --version` para encontrar la versión de Python instalada en el computador.
- Dirigirse a [esta página](https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-ldap) y descargar el binario correspondiente a la versión de Python utilizada y a la arquitectura del computador (32 o 64 bits).
    - Por ejemplo, para un computador con arquitectura de 64 bits y Python 3.9 instalado, el archivo a descargar será `python_ldap‑3.3.1‑cp39‑cp39‑win_amd64.whl`
