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

    5.1. En Windows: En caso de no tener instalada la VPN, buscar en el Drive compartido de la UAPA un archivo llamado `VPN_Cisco.msi` para instalar Cisco Any Connect.

    5.2. Una vez instalado, permite el acceso a redes no seguras.
    
    5.3. Logearse con las credenciales de la UN.

6. Abrir otra terminal y correr

`ssh -L 5432:127.0.0.1:5432 uapapp-admin@168.176.26.202`

7. Verificar que las siguientes variables de entorno estén asignadas. Éstas se encuentran en el Bitwarden.

    ```
    AESCI_DB_USER      
    AESCI_DB_HOST
    AESCI_DB_NAME
    AESCI_DB_PASS
    AESCI_LDAP
    URL_API
    SECRET_KEY
    ```
    
En Linux, utilizar el comando `export NOMBRE_VARIABLE="valor"`, en Windows usar el comando `setx NOMBRE_VARIABLE="valor"` o directamente configurarlas en el panel de control.

8. Correr el comando

`python3 manage.py runserver`⚠️¹⁴

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
- Desde la misma terminar que se está trabajano, instalar el archivo medidante el comando `pip install <DIRECCIÓN>/python_ldap‑3.3.1‑cp39‑cp39‑win_amd64.whl` o dirigirse a la carpeta donde se encuentra el archivo y probar `pip install python_ldap‑3.3.1‑cp39‑cp39‑win_amd64.whl` (no colocarle comillas al nombre del archivo)
- En caso de que aparezca un error acerca de que no se soporta el wheel, verificar que las especificaciones del computador (x32 o x64 bits) y la versión de Python correspondan con el nombre del archivo descargado.
- Una vez instalado, volver a correr el comando `pip install django_auth_ldap`, ahora no debería dar problemas y se puede seguir la instalación.

### 4. Sale un error que dice que la base de datos no tiene usuario o contraseña

Reiniciar el computador y volver a correr el back. Este error sólo debería aparecer la primera vez que se instala el backend.

## Una vez instalado, cómo correr el back

1. Activar el entorno virtual (posicionarse en la carpeta donde se creó ese entorno):

    - Linux: `source ./bin/activate`
    - Windows: `tutorial-env\Scripts\activate.bat`

2. Revisar que el entorno virtual cuente con los paquetes necesarios, para eso se puede usar el comando `pip list`.

3. Conectarse a la VPN.

4. Abrir otra terminal y correr

`ssh -L 5432:127.0.0.1:5432 uapapp-admin@168.176.26.202`

5. Revisar que las variables de entorno estén asignadas.

- En Linux: `printenv`
- En Windows: `SET`

6. Correr el comando

`python3 manage.py runserver`⚠️¹
