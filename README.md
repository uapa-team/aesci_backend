# aesci_backend

## Instalación del backend (Funciona tanto en Windows como en Linux)

0. En caso de no tener Python, instalarlo la versión 3.X desde [la página oficial](https://www.python.org/downloads/).

1. Descargar o clonar el repositorio. Preferiblemente en la rama Develop.

2. En la carpeta principal, crear un entorno virtual:

`python -m venv tutorial-env` ⚠️¹²

3. Activar entorno virtual

`tutorial-env\Scripts\activate.bat`

En Linux, usar este comando:

`source ./bin/activate`

4. Instalar este primer lote de librerias:

    ```
    pip install django
    pip install djangorestframework
    pip install djangorestframework-simplejwt
    pip install django-cors-headers
    ```
    
5. Instalar la libreria LDAP manualmente

    5.1. Colocar el comando `python --version` para encontrar la versión de Python instalada en el computador.
    
    5.2. Dirigirse a [esta página](https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-ldap) y descargar el binario correspondiente a la versión de Python utilizada y a la arquitectura del computador (32 o 64 bits).
    
    5.3. Desde la misma terminar que se está trabajano, instalar el archivo medidante el comando `pip install <DIRECCIÓN>/python_ldap‑3.3.1‑cp39‑cp39‑win_amd64.whl` o dirigirse a la carpeta donde se encuentra el archivo y probar `pip install python_ldap‑3.3.1‑cp39‑cp39‑win_amd64.whl` (no colocarle comillas al nombre del archivo). Por ejemplo, para un computador con arquitectura de 64 bits y Python 3.9 instalado, el archivo a descargar será `python_ldap‑3.3.1‑cp39‑cp39‑win_amd64.whl`

    5.4. En caso de que aparezca un error acerca de que no se soporta el wheel, verificar que las especificaciones del computador (x32 o x64 bits) y la versión de Python correspondan con el nombre del archivo descargado.
    
6.  Instalar este segundo lote de librerias:
    
    ```
    pip install django_auth_ldap ⚠️³
    pip install psycopg2
    pip install drf_spectacular
    pip install requests
    pip install pydrive
    ```

7. Conectarse a la VPN

    7.1. En Windows: En caso de no tener instalada la VPN, buscar en el Drive compartido de la UAPA un archivo llamado `VPN_Cisco.msi` para instalar Cisco Any Connect.

    7.2. Una vez instalado, permite el acceso a redes no seguras.
    
    7.3. Logearse con las credenciales de la UN.

8. Abrir otra terminal y correr

`ssh -L 5432:127.0.0.1:5432 uapapp-admin@168.176.26.202`

9. Verificar que las siguientes variables de entorno estén asignadas. Éstas se encuentran en el Bitwarden.

    ```
    AESCI_DB_USER      
    AESCI_DB_HOST
    AESCI_DB_NAME
    AESCI_DB_PASS
    AESCI_LDAP
    URL_API
    SECRET_KEY
    CLIENT_ID
    CLIENT_SECRET
    STUDENT_FOLDER
    ```
    
En Linux, utilizar el comando `export NOMBRE_VARIABLE="valor"`, en Windows usar el comando `setx NOMBRE_VARIABLE="valor"` o directamente configurarlas en el panel de control.

10. Reemplazar el archivo `credentials.json` con los datos que aparecen en el Bitwarden.

11. Correr el comando

`python manage.py runserver`⚠️¹⁴⁵

## ⚠️ Problemas comunes ⚠️

<!-- Aquí van los problemas comunes que se encuentren -->

### 1. La terminal/consola no reconoce el comando python

Por lo general se usa `python3` cuando se tienen varias versiones de Python en la máquina.

### 2. La terminal/consola no reconoce ni el comando python3 ni python y me aparece la Windows Store

Esto se debe porque al momento de instalar Python, en la primera pestaña, no se agregó el PATH de Python.

### 3. Sale un error que dice que la base de datos no tiene usuario o contraseña

Reiniciar el computador y volver a correr el back. Este error sólo debería aparecer la primera vez que se instala el backend.

### 4. El back corre pero me aparece un mensaje de advertencia sobre de que existen migraciones

**NO APLICAR MIGRACIONES.** El back te funcionará pero probablemente no estés en la rama indicada, probablemente estás en la rama **main**, es necesario cambiarse a la rama **develop** para lo cual, primero se cancela el back (Ctrl + C) y luego se utiliza el comando `git checkout develop`. En caso de haber aplicado migraciones comunicarse inmediatamente con la persona encargada del back.

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

`python manage.py runserver`⚠️¹

## Utilidades del back

### Swagger (Petitions documentation)

1. En el navegador colocar la dirección

`http://127.0.0.1:8000/docs`

Aquí se pueden revisar todas las peticiones y endpoints que existen dentro del proyecto. Complementar esta documentación con la existente en Postman.

### Djando Admin (Users administration)

1. En el navegador colocar la dirección

`http://127.0.0.1:8000/admin`

2. Logearse con un usuario con permisos de administrador

Dentro de la pestaña es posible mirar cada una de los objetos creados (estudiantes, profesores, tareas, cursos, etc).

- Para crear usuarios primero se crean **en los roles** y luego ya aparece **en users**. Para borrar se borra primero **en users** y luego otra vez **en el rol**.
- Para el Login no basta crear los usuarios en Django Admin, es necesario que sean cuentas reales porque se autentican con el LDAP. Para eso usamos tres (3) cuentas de pruebas (las dos de la UAPA y una personal) para los tres tipos de usuario: Admin, profesor y estudiante.

## Contacto

UAPA - autoevalua_fibog@unal.edu.co

## TO DO 📢

- Como instalar la DB y mirar datos desde ahí.
- ¿Cómo desplegar el back?
