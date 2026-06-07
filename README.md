# TalentFlow Bot

## Descripción

TalentFlow es un chatbot desarrollado en Python utilizando la API de Telegram. Su objetivo es automatizar el proceso de preselección de candidatos para el área de Recursos Humanos, permitiendo la recopilación de datos personales, disponibilidad laboral y recepción de currículums vitae en formato PDF.

El sistema reemplaza tareas manuales de carga de información, reduce errores administrativos y centraliza la información de los postulantes en un único repositorio.

---

## Funcionalidades

* Registro de candidatos mediante Telegram.
* Validación de datos ingresados.
* Captura de:

  * Nombre
  * Apellido
  * DNI
  * Fecha de nacimiento
  * Correo electrónico
  * Provincia
  * Ciudad
  * Remuneración pretendida
  * Disponibilidad horaria
* Recepción de CV en formato PDF.
* Almacenamiento de CVs en una carpeta local.
* Persistencia de información en archivo CSV.
* Gestión inicial del estado del candidato (PENDIENTE).

---

## Tecnologías Utilizadas

* Python 3
* Telegram Bot API
* python-telegram-bot
* Expresiones Regulares (Regex)
* Archivo CSV para persistencia de datos

---

## Estructura del Proyecto

TalentFlowBot/

├── bot.py

├── token.txt

├── candidatos.csv

├── README.md

└── cvs/

---

## Requisitos

* Python 3.10 o superior
* Cuenta de Telegram
* Token generado mediante BotFather

---

## Instalación

### 1. Clonar el repositorio

git clone https://github.com/usuario/TalentFlowBot.git

cd TalentFlowBot

### 2. Crear entorno virtual

Windows:

python -m venv .venv

### 3. Activar entorno virtual

PowerShell:

.venv\Scripts\Activate.ps1

Git Bash:

source .venv/Scripts/activate

### 4. Instalar dependencias

pip install python-telegram-bot

### 5. Configurar token

Crear un archivo llamado:

token.txt

y colocar dentro el token generado por BotFather.

Ejemplo:

123456789:ABCDEFxxxxxxxxxxxxxxxxxxxxxxxx

### 6. Crear carpeta para CVs

cvs

### 7. Crear archivo candidatos.csv

Agregar la siguiente cabecera:

telegram_id;nombre;apellido;dni;fecha_nacimiento;email;provincia;ciudad;remuneracion_pretendida;disponibilidad_inicio;disponibilidad_fin;cv;estado_candidato

---

## Ejecución

Ejecutar el siguiente comando:

python bot.py

Si la ejecución es correcta se visualizará:

Bot iniciado correctamente...

---

## Flujo de Uso

1. El usuario inicia el bot mediante /start.
2. El sistema solicita información personal.
3. El sistema valida cada dato ingresado.
4. El usuario adjunta su CV en formato PDF.
5. El sistema almacena la información.
6. El candidato queda registrado con estado PENDIENTE.

---

## Máquina de Estados

INICIO

↓

NOMBRE

↓

APELLIDO

↓

DNI

↓

FECHA_NACIMIENTO

↓

EMAIL

↓

PROVINCIA

↓

CIUDAD

↓

REMUNERACION

↓

DISPONIBILIDAD_INICIO

↓

DISPONIBILIDAD_FIN

↓

CV

↓

FINALIZADO

---

## Estados del Candidato

* PENDIENTE
* APROBADO
* RECHAZADO

---

## Autor

Adalberto Jesus Navas Piazza

Proyecto académico desarrollado para la materia Organización Empresarial.
