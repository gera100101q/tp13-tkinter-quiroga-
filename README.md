# IPET 249 - Desafío de Mecanografía ⌨️

**Alumno:** Gerardo Quiroga
**Curso:** 6° G - Laboratorio de Aplicaciones II - IPET N°249
**TP N°13:** Desarrollo de Aplicación de Escritorio con Tkinter

## Opción elegida: Prueba de Mecanografía (Typing Test)

Aplicación de escritorio que mide la velocidad de tipeo (palabras por minuto) y la precisión del usuario, mostrándole una frase aleatoria que debe reproducir exactamente en un campo de texto.

### Funcionamiento

1. El usuario elige una categoría de frases (Tecnología, Motivación, Curiosidades o Todas) desde un `Combobox`.
2. Al presionar **"Iniciar Prueba"**, se elige una frase aleatoria del arreglo base (12 frases en total, todas de 15+ palabras), arranca el cronómetro y se habilita el campo de texto. El botón de inicio se deshabilita para que no se pueda re-disparar el cronómetro mientras la prueba está en curso.
3. A medida que el usuario escribe, una barra de progreso (`ttk.Progressbar`) muestra cuánto lleva avanzado, y cualquier carácter mal tipeado tiñe el texto de rojo como advertencia visual (y queda contado como error para el cálculo de precisión).
4. Al completar la frase **exactamente** (validación sin margen de error), se detiene el cronómetro y se muestran: tiempo total, palabras por minuto (WPM) y precisión (%).
5. **"Reiniciar"** vuelve la app a su estado inicial; **"Salir"** pide confirmación antes de cerrar.

## Requisitos técnicos cumplidos

| Requisito | Cómo se resolvió |
|---|---|
| Ventana 800x600, título, fondo institucional | `root.geometry("800x600")`, `root.title(...)`, `root.configure(bg=COLOR_FONDO)` |
| Identidad IPET 249 | Paleta propia (azul marino, dorado, crema) + emblema en `assets/emblema_ipet249.png` |
| `pack()` + `grid()` justificados | `pack()` para las 3 macro-secciones verticales (encabezado, contenido, pie); `grid()` dentro del contenido para alinear el formulario en filas y columnas |
| 3+ eventos distintos | Clic de mouse (botones), teclado (`<KeyRelease>` y `<Return>` en el Entry), ventana (`protocol("WM_DELETE_WINDOW", ...)`) |
| 3+ Labels dinámicas | Frase actual, tiempo, WPM, precisión, instrucciones |
| 3+ Botones independientes | Iniciar Prueba, Reiniciar, Salir |
| Entry | Campo de tipeo, habilitado solo durante la prueba |
| 2+ componentes `ttk` | `ttk.Combobox` (categoría) y `ttk.Progressbar` (avance) |
| Manejo de excepciones | `try/except` al cargar el emblema (`TclError`/`FileNotFoundError`) y al elegir frase de una categoría |

## Instalación y ejecución

Requiere Python 3 con Tkinter (incluido por defecto en la mayoría de las instalaciones de Python en Windows/Mac; en Linux puede requerir `sudo apt install python3-tk`).

```bash
git clone <url-del-repositorio>
cd tp13-tkinter-quiroga
python main.py
```

No requiere instalar dependencias externas (solo usa la librería estándar de Python: `tkinter`, `random`, `time`, `os`).

## Capturas de pantalla

**Prueba en curso** (categoría "Todas", tipeo parcial con barra de progreso):

![Captura de la app en ejecución](assets/captura_pantalla.png)

**Prueba finalizada** (métricas calculadas):

![Captura con resultado final](assets/captura_resultado.png)

> La segunda captura fue generada con un script de testing que tipea la frase instantáneamente (por eso el WPM se ve irreal); en un uso real con una persona tipeando, el valor refleja la velocidad genuina.

## Declaración sobre Inteligencia Artificial

Ver [`IA_LOG.md`](./IA_LOG.md) para el detalle completo de herramienta, prompts exactos, fundamentación y verificación.

**Resumen:** se usó Claude (Anthropic) como asistente para generar la estructura completa de la aplicación, siguiendo el estilo de trabajo de resolución directa ya adoptado para esta materia. El código fue generado por la IA y verificado ejecutándolo en un entorno real (Tkinter + Xvfb), simulando rondas completas de tipeo correctas y con errores para confirmar que la lógica de precisión, WPM, bloqueo de botones y cierre de ventana funciona como se espera. **Gerardo debe revisar y poder explicar cada función antes de la entrega**, tal como exige la consigna del TP.
