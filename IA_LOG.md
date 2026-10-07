# Ficha de Transparencia del Uso de IA - TP N°13

> ⚠️ Si tuviste alguna otra interacción con la IA fuera de esta conversación (por ejemplo, para entender algo puntual del código una vez entregado), agregala como una fila más siguiendo el mismo formato.

| Campo | Interacción 1 | Interacción 2 |
|---|---|---|
| **Herramienta** | Claude (Anthropic) | Claude (Anthropic) |
| **Objetivo** | Definir el estilo de trabajo para los TPs de Laboratorio de Aplicaciones II: resolución directa y completa, sin preámbulos largos. | Elegir la temática del TP13 entre las 4 opciones propuestas en la consigna. |
| **Prompt Exacto** | "resolve diercto" (en respuesta a "¿Qué enfoque preferís para este TP?") | "Prueba de Mecanografía (Typing Test)" (selección entre las 4 opciones del enunciado) |
| **Fundamentación** | Instrucción breve pero con contexto claro, ya que venía dentro de una pregunta puntual sobre el enfoque a seguir en esta materia específica. | Selección directa y sin ambigüedad de una opción ya enumerada explícitamente en la consigna del TP. |
| **Aprendizaje** | Cómo combinar `pack()` (para las secciones macro de la ventana) y `grid()` (para alinear un formulario en filas y columnas) de forma justificada en el mismo programa, y cómo manejar con `try/except` la carga de un recurso externo (imagen) sin que la app se rompa si falta. | Diferencia entre un cronómetro ascendente (este TP, mide cuánto tardás) y un temporizador descendente (como en la opción CPS Test), y cómo calcular precisión de tipeo comparando carácter a carácter en tiempo real con el evento `<KeyRelease>`. |
| **Verificación** | Se instaló Tkinter y Xvfb (framebuffer virtual) para correr la app real sin interfaz gráfica física, y se simuló una ronda completa de tipeo sin errores, confirmando que el botón de inicio se deshabilita, el cronómetro corre, y al completar la frase se calculan WPM y precisión correctamente. | Se simuló una ronda con un error de tipeo intencional (primer carácter incorrecto) y se confirmó que el contador de errores subió a 1 y la precisión resultante (99.2% sobre 125 caracteres) coincide con la fórmula `(1 - errores/longitud) × 100`. |
