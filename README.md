# DashCardioCLA
Monitoreo y análisis del Programa de Gestión de Patología Cardiovascular de EPS SURA. Control de topes CUPS, seguimiento de facturación e indicadores de calidad.
README.md — PGP Cardiovascular Dashboard
🫀 PGP Cardiovascular — Dashboard EPS SURA
Sistema de monitoreo, análisis y reportes del Programa de Gestión de Patología Cardiovascular para EPS SURAMERICANA S.A.

Permite a los equipos clínicos y administrativos hacer seguimiento en tiempo real de la facturación de procedimientos cardiovasculares, detectar alertas de topes de CUPS y visualizar indicadores de calidad del programa.

📋 Tabla de Contenidos
Descripción
Arquitectura del Proyecto
Requisitos
Instalación
Archivos Requeridos
Uso del Sistema
Módulos
Lógica de Procesamiento
Estructura de Código
Personalización
Flujo de Datos
Troubleshooting
Roadmap
Licencia
📝 Descripción
El dashboard transforma los archivos crudos exportados desde el sistema GHIPS y la Nota Técnica PGP en tableros interactivos que permiten:

Filtrar facturación por aseguradora, fecha, tipo de procedimiento y CUPS específico
Controlar topes mensuales de cada procedimiento con semáforos de alerta (🟢 Normal / 🟡 Alerta / 🔴 Crítico)
Visualizar evolución temporal de valores y volumenes
Descargar reportes en CSV (listado completo y resumen mensual)
Monitorear indicadores de calidad del PGP (oportunidad, rehospitalizaciones, ejecución financiera)
🏗️ Arquitectura del Proyecto
pgp-cardio-dashboard/
│
├── app2.py # Aplicación principal (Streamlit)
├── cardiopgp.py # Notebook de referencia (lógica original Colab)
├── requirements.txt # Dependencias del proyecto
├── README.md # Este archivo
│
├── data/ # (Opcional) Archivos de datos locales
│ ├── NOTA TECNICA AMBULATORIA PGP CARDIO.xlsx
│ └── df_fgrab.csv
│
└── output/ # (Opcional) Reportes generados
├── resumen_mensual_cups.csv
└── listado_completo_cups_pgp.csv
