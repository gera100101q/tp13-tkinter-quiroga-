# -*- coding: utf-8 -*-
"""
main.py - Desafío de Mecanografía (Typing Test)
TP N°13 - Laboratorio de Aplicaciones II - Gerardo Quiroga - 6° G - IPET N°249

Aplicación de escritorio con Tkinter que mide velocidad (WPM) y precisión
de tipeo contra frases aleatorias.
"""

import os
import random
import time
import tkinter as tk
from tkinter import ttk, messagebox

# ============================================================
# Paleta institucional IPET 249
# ============================================================
COLOR_FONDO = "#F5F1E8"       # crema institucional
COLOR_HEADER = "#16213E"      # azul marino
COLOR_ACENTO = "#F2C14E"      # dorado (girasol del escudo)
COLOR_TEXTO = "#16213E"
COLOR_TEXTO_CLARO = "#F5F1E8"
COLOR_EXITO = "#4C9A4C"
COLOR_ERROR = "#D64550"

FUENTE_TITULO = ("Segoe UI", 18, "bold")
FUENTE_NORMAL = ("Segoe UI", 11)
FUENTE_FRASE = ("Consolas", 13)
FUENTE_METRICA = ("Segoe UI", 12, "bold")

RUTA_EMBLEMA = os.path.join(os.path.dirname(__file__), "assets", "emblema_ipet249.png")

# ============================================================
# Arreglo base de frases (>= 10, cada una de 15+ palabras)
# Cada frase está etiquetada por categoría para el filtro del Combobox.
# ============================================================
FRASES_BASE = [
    {"categoria": "Tecnología", "texto": "La inteligencia artificial está cambiando la forma en que las personas trabajan y aprenden cada día."},
    {"categoria": "Tecnología", "texto": "Python es un lenguaje de programación versátil que se utiliza en ciencia de datos, automatización y desarrollo web."},
    {"categoria": "Tecnología", "texto": "Los sistemas operativos modernos permiten ejecutar múltiples procesos al mismo tiempo sin que el usuario lo note."},
    {"categoria": "Tecnología", "texto": "Aprender a programar requiere práctica constante, paciencia y la capacidad de aceptar errores como parte del proceso."},
    {"categoria": "Tecnología", "texto": "Las interfaces gráficas permiten que cualquier persona pueda interactuar con una computadora sin conocer código."},
    {"categoria": "Motivación", "texto": "El esfuerzo diario y la constancia son más importantes que la inteligencia a la hora de alcanzar una meta."},
    {"categoria": "Motivación", "texto": "Cada error que cometemos mientras aprendemos algo nuevo es una oportunidad para mejorar un poco más."},
    {"categoria": "Motivación", "texto": "Nadie nace sabiendo escribir rápido en un teclado, la velocidad se construye con práctica repetida y paciencia."},
    {"categoria": "Motivación", "texto": "Los grandes proyectos siempre comienzan con un primer paso pequeño que parece insignificante al principio."},
    {"categoria": "Curiosidades", "texto": "El zorro marrón salta rápidamente sobre el perro perezoso mientras el sol se esconde detrás de las montañas."},
    {"categoria": "Curiosidades", "texto": "Las bibliotecas antiguas guardaban miles de libros escritos a mano antes de que existiera la imprenta moderna."},
    {"categoria": "Curiosidades", "texto": "Un teclado QWERTY fue diseñado originalmente para evitar que las teclas mecánicas de las máquinas de escribir se trabaran."},
]

CATEGORIAS = ["Todas"] + sorted({frase["categoria"] for frase in FRASES_BASE})


# ============================================================
# Estado de la aplicación
# ============================================================
def crear_estado():
    return {
        "frase_actual": "",
        "prueba_activa": False,
        "tiempo_inicio": None,
        "errores": 0,
        "longitud_anterior": 0,
        "tarea_cronometro": None,
    }


# ============================================================
# Funciones de lógica
# ============================================================
def elegir_frase(categoria):
    """Elige una frase aleatoria del arreglo base, filtrada por categoría."""
    if categoria == "Todas":
        candidatas = FRASES_BASE
    else:
        candidatas = [f for f in FRASES_BASE if f["categoria"] == categoria]
    return random.choice(candidatas)["texto"]


def calcular_wpm(frase, segundos_transcurridos):
    """Palabras por minuto = (cantidad de palabras / minutos transcurridos)."""
    if segundos_transcurridos <= 0:
        return 0.0
    cantidad_palabras = len(frase.split())
    minutos = segundos_transcurridos / 60
    return round(cantidad_palabras / minutos, 1)


def calcular_precision(frase, errores):
    """Precisión = porcentaje de caracteres tipeados correctamente
    en el primer intento, sin contar las correcciones realizadas."""
    if len(frase) == 0:
        return 100.0
    precision = (1 - errores / len(frase)) * 100
    return max(0.0, round(precision, 1))


# ============================================================
# Aplicación principal
# ============================================================
class AppMecanografia:
    def __init__(self, root):
        self.root = root
        self.estado = crear_estado()
        self.emblema_img = None  # referencia viva para que no la borre el garbage collector

        self._configurar_ventana()
        self._cargar_emblema()
        self._construir_interfaz()

        # --- Evento de ventana: confirmar antes de cerrar ---
        self.root.protocol("WM_DELETE_WINDOW", self.confirmar_salida)

    # ------------------------------------------------------
    def _configurar_ventana(self):
        self.root.title("IPET 249 - Desafío de Mecanografía")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_FONDO)

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Institucional.Horizontal.TProgressbar",
                          troughcolor=COLOR_FONDO, background=COLOR_ACENTO,
                          bordercolor=COLOR_HEADER, lightcolor=COLOR_ACENTO,
                          darkcolor=COLOR_ACENTO)
        estilo.configure("TCombobox", fieldbackground=COLOR_FONDO)

    def _cargar_emblema(self):
        """Carga el emblema institucional. Si el archivo no existe o Tkinter
        no puede leerlo, la app sigue funcionando sin romperse (fallback de texto)."""
        try:
            self.emblema_img = tk.PhotoImage(file=RUTA_EMBLEMA)
            # Reducimos el tamaño si la imagen es muy grande
            factor = max(1, self.emblema_img.width() // 56)
            if factor > 1:
                self.emblema_img = self.emblema_img.subsample(factor, factor)
        except (tk.TclError, FileNotFoundError) as error:
            print(f"Aviso: no se pudo cargar el emblema ({error}). Se usará un ícono de texto.")
            self.emblema_img = None

    # ------------------------------------------------------
    def _construir_interfaz(self):
        # --- pack(): se usa para las 3 macro-secciones verticales de la
        # ventana (encabezado, contenido, pie), porque son bloques simples
        # que se apilan de arriba hacia abajo. ---
        self._construir_encabezado()
        self._construir_contenido()   # usa grid() internamente
        self._construir_pie()

    def _construir_encabezado(self):
        header = tk.Frame(self.root, bg=COLOR_HEADER, height=70)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)

        if self.emblema_img is not None:
            lbl_logo = tk.Label(header, image=self.emblema_img, bg=COLOR_HEADER)
        else:
            lbl_logo = tk.Label(header, text="🏫", font=("Segoe UI", 28), bg=COLOR_HEADER, fg=COLOR_ACENTO)
        lbl_logo.pack(side="left", padx=16, pady=8)

        lbl_titulo = tk.Label(header, text="IPET 249 - Desafío de Mecanografía",
                               font=FUENTE_TITULO, bg=COLOR_HEADER, fg=COLOR_TEXTO_CLARO)
        lbl_titulo.pack(side="left", pady=8)

    def _construir_contenido(self):
        contenido = tk.Frame(self.root, bg=COLOR_FONDO, padx=30, pady=20)
        contenido.pack(side="top", fill="both", expand=True)

        # --- grid(): usado para alinear en columnas el formulario
        # (etiquetas, selector, entrada y métricas), porque necesitamos
        # que todo quede prolijamente alineado en filas y columnas. ---

        # Etiqueta descriptiva (Label #1)
        self.lbl_instrucciones = tk.Label(
            contenido, text="Elegí una categoría, presioná \"Iniciar Prueba\" y escribí la frase exactamente como aparece:",
            font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO, wraplength=720, justify="left")
        self.lbl_instrucciones.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        # --- ttk avanzado #1: Combobox de categoría ---
        tk.Label(contenido, text="Categoría:", font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(
            row=1, column=0, sticky="w")
        self.combo_categoria = ttk.Combobox(contenido, values=CATEGORIAS, state="readonly", width=20)
        self.combo_categoria.set(CATEGORIAS[0])
        self.combo_categoria.grid(row=1, column=1, sticky="w", padx=(8, 0))

        # Frase objetivo (Label #2, dinámica)
        self.lbl_frase = tk.Label(
            contenido, text="Presioná \"Iniciar Prueba\" para comenzar...",
            font=FUENTE_FRASE, bg="#FFFFFF", fg=COLOR_TEXTO, wraplength=720,
            justify="left", padx=12, pady=12, relief="solid", borderwidth=1)
        self.lbl_frase.grid(row=2, column=0, columnspan=3, sticky="we", pady=16)

        # Entrada de texto (Entry) - deshabilitada hasta iniciar la prueba
        self.entry_tipeo = tk.Entry(contenido, font=FUENTE_FRASE, width=70, state="disabled")
        self.entry_tipeo.grid(row=3, column=0, columnspan=3, sticky="we", pady=(0, 6))
        # --- Evento de teclado: validar en vivo mientras se escribe ---
        self.entry_tipeo.bind("<KeyRelease>", self.al_tipear)
        # --- Evento de teclado (distinto): Enter intenta validar manualmente ---
        self.entry_tipeo.bind("<Return>", self.al_presionar_enter)

        # --- ttk avanzado #2: Progressbar de avance de tipeo ---
        self.barra_progreso = ttk.Progressbar(
            contenido, style="Institucional.Horizontal.TProgressbar",
            orient="horizontal", length=720, mode="determinate", maximum=100)
        self.barra_progreso.grid(row=4, column=0, columnspan=3, sticky="we", pady=(0, 16))

        # Métricas dinámicas (Labels #3, #4, #5)
        metricas = tk.Frame(contenido, bg=COLOR_FONDO)
        metricas.grid(row=5, column=0, columnspan=3, sticky="w")

        self.lbl_tiempo = tk.Label(metricas, text="⏱️ Tiempo: 00:00", font=FUENTE_METRICA, bg=COLOR_FONDO, fg=COLOR_TEXTO)
        self.lbl_tiempo.grid(row=0, column=0, padx=(0, 24))

        self.lbl_wpm = tk.Label(metricas, text="📊 WPM: 0", font=FUENTE_METRICA, bg=COLOR_FONDO, fg=COLOR_TEXTO)
        self.lbl_wpm.grid(row=0, column=1, padx=(0, 24))

        self.lbl_precision = tk.Label(metricas, text="✅ Precisión: 0%", font=FUENTE_METRICA, bg=COLOR_FONDO, fg=COLOR_TEXTO)
        self.lbl_precision.grid(row=0, column=2)

    def _construir_pie(self):
        pie = tk.Frame(self.root, bg=COLOR_FONDO, pady=16)
        pie.pack(side="bottom", fill="x")

        # Botón #1: Iniciar Prueba
        self.btn_iniciar = tk.Button(
            pie, text="Iniciar Prueba", font=FUENTE_NORMAL, bg=COLOR_ACENTO, fg=COLOR_HEADER,
            activebackground=COLOR_HEADER, activeforeground=COLOR_TEXTO_CLARO,
            relief="flat", padx=16, pady=8, command=self.iniciar_prueba)
        self.btn_iniciar.pack(side="left", padx=(30, 10))

        # Botón #2: Reiniciar
        self.btn_reiniciar = tk.Button(
            pie, text="Reiniciar", font=FUENTE_NORMAL, bg=COLOR_HEADER, fg=COLOR_TEXTO_CLARO,
            activebackground=COLOR_ACENTO, activeforeground=COLOR_HEADER,
            relief="flat", padx=16, pady=8, command=self.reiniciar_prueba)
        self.btn_reiniciar.pack(side="left", padx=10)

        # Botón #3: Salir
        self.btn_salir = tk.Button(
            pie, text="Salir", font=FUENTE_NORMAL, bg=COLOR_ERROR, fg=COLOR_TEXTO_CLARO,
            activebackground="#A6333C", activeforeground=COLOR_TEXTO_CLARO,
            relief="flat", padx=16, pady=8, command=self.confirmar_salida)
        self.btn_salir.pack(side="right", padx=(10, 30))

    # ------------------------------------------------------
    # Manejadores de eventos / lógica de la prueba
    # ------------------------------------------------------
    def iniciar_prueba(self):
        """Evento de clic: arranca una nueva ronda de tipeo."""
        try:
            categoria = self.combo_categoria.get()
            frase = elegir_frase(categoria)
        except (IndexError, ValueError) as error:
            # Manejo básico de excepciones: categoría sin frases disponibles
            messagebox.showerror("Error", f"No se pudo iniciar la prueba: {error}")
            return

        self.estado = crear_estado()
        self.estado["frase_actual"] = frase
        self.estado["prueba_activa"] = True
        self.estado["tiempo_inicio"] = time.time()

        self.lbl_frase.config(text=frase)
        self.entry_tipeo.config(state="normal", fg=COLOR_TEXTO)
        self.entry_tipeo.delete(0, tk.END)
        self.entry_tipeo.focus_set()
        self.barra_progreso["value"] = 0
        self.lbl_wpm.config(text="📊 WPM: 0")
        self.lbl_precision.config(text="✅ Precisión: 0%")

        # Bloqueamos el botón de inicio para que no se pueda re-disparar
        # el cronómetro mientras ya hay una prueba en curso.
        self.btn_iniciar.config(state="disabled")

        self._actualizar_cronometro()

    def _actualizar_cronometro(self):
        if not self.estado["prueba_activa"]:
            return
        segundos = int(time.time() - self.estado["tiempo_inicio"])
        minutos, segs = divmod(segundos, 60)
        self.lbl_tiempo.config(text=f"⏱️ Tiempo: {minutos:02d}:{segs:02d}")
        self.estado["tarea_cronometro"] = self.root.after(1000, self._actualizar_cronometro)

    def al_tipear(self, event):
        """Evento de teclado: se dispara con cada tecla soltada en el Entry."""
        if not self.estado["prueba_activa"]:
            return

        texto_actual = self.entry_tipeo.get()
        objetivo = self.estado["frase_actual"]

        # Actualizamos la barra de progreso según cuánto lleva escrito
        progreso = min(len(texto_actual), len(objetivo))
        porcentaje = (progreso / len(objetivo)) * 100 if objetivo else 0
        self.barra_progreso["value"] = porcentaje

        # Detectamos si el último carácter tipeado es un error
        if len(texto_actual) > self.estado["longitud_anterior"]:
            idx = len(texto_actual) - 1
            if idx < len(objetivo) and texto_actual[idx] != objetivo[idx]:
                self.estado["errores"] += 1
                self.entry_tipeo.config(fg=COLOR_ERROR)  # advertencia visual
            else:
                self.entry_tipeo.config(fg=COLOR_TEXTO)
        self.estado["longitud_anterior"] = len(texto_actual)

        # Validación exacta: si coincide carácter por carácter, termina la prueba
        if texto_actual == objetivo:
            self.finalizar_prueba()

    def al_presionar_enter(self, event):
        """Evento de teclado alternativo: permite forzar la validación con Enter."""
        if not self.estado["prueba_activa"]:
            return
        texto_actual = self.entry_tipeo.get()
        if texto_actual == self.estado["frase_actual"]:
            self.finalizar_prueba()
        else:
            messagebox.showwarning("Todavía no coincide", "El texto ingresado no coincide exactamente con la frase. Seguí escribiendo.")

    def finalizar_prueba(self):
        self.estado["prueba_activa"] = False
        if self.estado["tarea_cronometro"] is not None:
            self.root.after_cancel(self.estado["tarea_cronometro"])

        segundos_totales = time.time() - self.estado["tiempo_inicio"]
        wpm = calcular_wpm(self.estado["frase_actual"], segundos_totales)
        precision = calcular_precision(self.estado["frase_actual"], self.estado["errores"])

        self.lbl_tiempo.config(text=f"⏱️ Tiempo: {segundos_totales:.1f}s")
        self.lbl_wpm.config(text=f"📊 WPM: {wpm}")
        self.lbl_precision.config(text=f"✅ Precisión: {precision}%")
        self.entry_tipeo.config(state="disabled")
        self.btn_iniciar.config(state="normal")

        messagebox.showinfo(
            "¡Prueba completada!",
            f"Tiempo: {segundos_totales:.1f} segundos\nWPM: {wpm}\nPrecisión: {precision}%")

    def reiniciar_prueba(self):
        """Botón: vuelve la app a su estado inicial."""
        if self.estado.get("tarea_cronometro") is not None:
            self.root.after_cancel(self.estado["tarea_cronometro"])
        self.estado = crear_estado()

        self.lbl_frase.config(text="Presioná \"Iniciar Prueba\" para comenzar...")
        self.entry_tipeo.config(state="normal", fg=COLOR_TEXTO)
        self.entry_tipeo.delete(0, tk.END)
        self.entry_tipeo.config(state="disabled")
        self.barra_progreso["value"] = 0
        self.lbl_tiempo.config(text="⏱️ Tiempo: 00:00")
        self.lbl_wpm.config(text="📊 WPM: 0")
        self.lbl_precision.config(text="✅ Precisión: 0%")
        self.btn_iniciar.config(state="normal")

    def confirmar_salida(self):
        """Evento de ventana: confirma antes de cerrar la aplicación."""
        if messagebox.askyesno("Salir", "¿Seguro que querés cerrar el Desafío de Mecanografía?"):
            if self.estado.get("tarea_cronometro") is not None:
                try:
                    self.root.after_cancel(self.estado["tarea_cronometro"])
                except tk.TclError:
                    pass
            self.root.destroy()


def main():
    root = tk.Tk()
    AppMecanografia(root)
    root.mainloop()


if __name__ == "__main__":
    main()
