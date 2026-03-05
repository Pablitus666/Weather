# 📦 Weather v1.0 — High-Performance Async Weather Engine

🎉 **Primer Lanzamiento Estable — Edición Profesional de Alto Rendimiento**

Esta versión marca el debut oficial de **Weather**, una solución de escritorio que trasciende el concepto de script meteorológico convencional. Diseñada bajo principios de **Arquitectura Limpia** y **Programación Asíncrona**, esta herramienta ofrece una experiencia de usuario fluida, segura y técnicamente superior.

---

## 🔧 Innovaciones Técnicas en v1.0

Este lanzamiento representa la culminación de un proceso de ingeniería senior, destacando:

*   **Motor Meteorológico Asíncrono:** Implementación de un cliente `httpx.AsyncClient` persistente con *connection pooling*, garantizando peticiones ultra-rápidas y un manejo eficiente de la concurrencia sin bloquear la interfaz.
*   **Arquitectura MVC Desacoplada:** Estructura modular que separa estrictamente la lógica de red, los modelos inmutables y la capa de presentación para una estabilidad excepcional.
*   **Robustez Industrial:** Sistema de manejo de excepciones tipadas y logging rotativo (2MB x 3 backups) preparado para entornos de producción.
*   **Seguridad de Grado Profesional:**
    *   **Firma Digital SHA256:** Binarios firmados por **Walter Pablo Téllez Ayala** para una ejecución íntegra y auténtica en Windows.
    *   **Desacoplamiento de Secretos:** Gestión inteligente de API Keys mediante variables de entorno y archivos `.env` externos.
*   **Internacionalización Nativa:** Soporte dinámico para 9 idiomas con detección automática del locale del sistema operativo.
*   **Build OneFile Portable:** Ejecutable único de alta densidad que embebe todos los recursos, activos gráficos y el entorno de ejecución.

---

## 🚀 Guía de Despliegue

Los componentes esenciales para una experiencia segura se encuentran en la sección de **Assets**:

### 🌦️ Weather (`Weather.exe`) 🏃
*   **Estado:** Versión Final Estable.
*   **Uso:** Ejecutable autónomo (Portable). Descargar y ejecutar.
*   **Ventaja:** No requiere instalación ni dependencias externas.

### 🛡️ Certificado Público (`.cer`)
*   **Propósito:** Permite la verificación manual de la identidad del autor y la integridad del binario a través de las propiedades del sistema en Windows.

---

## ✨ Especificaciones de Software

*   🖼️ **UI HiDPI:** Optimizada para monitores 4K con escalado dinámico de fuentes e imágenes.
*   📁 **Persistencia Inteligente:** Almacenamiento local de preferencias en directorios de sistema (`AppData`).
*   🧪 **Calidad Garantizada:** Lógica de negocio validada mediante una suite de tests automatizados con `pytest`.
*   📍 **Feedback Visual:** Iconografía meteorológica HD y efectos de relieve dinámico en la interfaz.

---

## 👨‍💻 Autor y Visión

**Walter Pablo Téllez Ayala**  
Software Developer  
📍 Bolivia 🇧🇴  

© 2026 — Weather Professional Tooling

---

📥 **Descarga el ejecutable `Weather.exe` en la sección Assets situada al final de esta página.**
