# Simulador Interactivo de Transmisión de Datos con Contexto Real - UNEMI

Simulador desarrollado en **Python** para la asignatura **Comunicación de Datos**, que permite visualizar de manera interactiva cómo se transmite información digital mediante señales analógicas, incorporando conceptos fundamentales de la Unidad 3 y ejemplos de aplicaciones del mundo real.

---

## Descripción

Este proyecto simula el proceso de transmisión de datos utilizando una interfaz gráfica desarrollada con **Tkinter**, mostrando paso a paso la conversión de caracteres a código ASCII, su representación binaria y la transmisión mediante señales digitales y analógicas.

Además, incorpora ejemplos cotidianos como WhatsApp, Netflix, llamadas celulares, controles infrarrojos y transacciones bancarias para facilitar la comprensión de los conceptos estudiados en clase.

---

## Características

* Interfaz gráfica intuitiva.
* Conversión de caracteres a código ASCII.
* Representación binaria de 8 bits.
* Visualización simultánea de:

  * Señal digital.
  * Señal analógica.
* Barra de progreso de transmisión.
* ⏯ Controles para:

  * Iniciar transmisión.
  * Pausar.
  * Reanudar.
  * Detener.
  * Reiniciar.

* Simulación de ruido en el canal (SNR).
* Simulación de errores de bits.
* Verificación mediante paridad.
* Exportación de los gráficos en formato PNG.
* Ejemplos reales de aplicaciones de redes y comunicaciones.

---

## Tecnologías utilizadas

* Python 3.x
* Tkinter
* NumPy
* Matplotlib

---

## Requisitos del sistema

### Requisitos mínimos

| Recurso             | Requerimiento mínimo |
| ------------------- | -------------------- |
| Procesador          | 1 GHz o superior     |
| Memoria RAM         | 2 GB                 |
| Espacio en disco    | 200 MB libres        |
| Conexión a Internet | No requerida         |

### Software requerido

| Componente        | Detalle                                    |
| ----------------- | ------------------------------------------ |
| Sistema Operativo | Windows 7/8/10/11 (64 bits), Linux o macOS |
| Python            | Python 3.10 o superior                     |
| Bibliotecas       | tkinter, matplotlib, numpy                 |

> **Nota:** Tkinter suele venir instalado con Python. Si utilizas Linux, puede ser necesario instalar el paquete `python3-tk`.

---
## Funcionamiento

1. Escriba un mensaje en la caja de texto.
2. Presione **Transmitir y Analizar**.
3. Observe:

   * Conversión a ASCII.
   * Conversión a binario.
   * Animación bit a bit.
   * Señal digital.
   * Señal analógica.
4. Puede modificar:

   * Nivel de ruido.
   * Velocidad de transmisión.
5. Active la simulación de errores para observar la detección mediante paridad.
6. Exporte los gráficos cuando lo desee.

---

## Conceptos aplicados

* Comunicación de datos
* Señales digitales
* Señales analógicas
* Código ASCII
* Codificación binaria
* Teorema de Nyquist
* Relación Señal/Ruido (SNR)
* Detección de errores mediante paridad
* Ancho de banda
* Transmisión de información

---

## Capturas

Se recomienda incluir imágenes como:

* Interfaz principal
* Animación de codificación ASCII
* Señal digital
* Señal analógica
* Simulación con ruido
* Detección de errores

---

## Autor

**Sofia Marquez**

Universidad Estatal de Milagro (UNEMI)

Carrera de Tecnologías de la Información

Asignatura: Comunicación de Datos

---

## Licencia

Este proyecto fue desarrollado con fines exclusivamente académicos y educativos.
