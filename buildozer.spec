[app]

# (str) Título de tu aplicación
title = Radar WiFi Familiar

# (str) Nombre del paquete (sin espacios)
package.name = radarwififamiliar

# (str) Dominio del paquete
package.domain = org.radarwifi

# (list) Archivos incluidos en el paquete (añadimos app, templates y static)
source.include_exts = py,png,jpg,kv,atlas,html,json,txt

# (list) Directorio de código fuente
source.dir = .

# (list) Requerimientos de la aplicación (Python y Flask)
requirements = python3,kivy

# (str) Versión de la aplicación
version = 1.0

# (list) Permisos necesarios en Android para escanear red y usar Wi-Fi
android.permissions = INTERNET, ACCESS_WIFI_STATE, ACCESS_NETWORK_STATE

# (str) Orientación soportada
orientation = portrait

[buildozer]

# (int) Nivel de log (0 = error solo, 1 = informativo, 2 = debug)
log_level = 2

# (int) Modo de advertencia para root
warn_on_root = 1