# Adoptar IA hoy: cómo usar la presentación

Charla de la Semana de la Empleabilidad 2026, en la Universidad de La Frontera. Lunes 28 de septiembre a las 15:00, 40 minutos.

## Qué abrir

- **`deck/index.html`**: la presentación completa. Funciona sin internet porque las fuentes y las fotos van dentro del archivo.
- **`deck/media/demo-ia.mp4`**: el video de la demo. Debe quedar siempre al lado del HTML, en la carpeta `deck/media/`.
- **`deck/media/reel-java.mp4`**: el reel de Camila aprendiendo Java (slide 3), con su imagen de portada `reel-java-poster.jpg`.
- **`GUION.md`**: el guion completo de los tres relatores. Sirve para ensayar y como respaldo impreso.

Para llevar la charla en un pendrive, copia la carpeta `deck/` completa (con `media/` adentro).

## Teclas

| Tecla | Acción |
|---|---|
| → · Espacio · Enter · PageDown · clic | Avanzar (fragmento o slide) |
| ← · PageUp · Backspace | Retroceder |
| Home / End | Primera / última slide |
| **P** | Abre la **ventana del presentador** (y arranca el cronómetro) |
| T | Muestra u oculta el cronómetro en la pantalla del público |
| N | Muestra el guion en la misma página, por si el navegador bloquea la ventana del presentador |
| O | Índice de todas las slides |
| F | Pantalla completa |
| L | Tema claro u oscuro |
| ? | Ayuda |
| Esc | Cierra índice, ayuda o notas |

El cronómetro arranca con el primer avance o al presionar P.

## Ventana del presentador (P)

Muestra:
- la slide actual y quién la presenta, con el color de cada relator;
- el tiempo total y el desvío respecto del plan: verde si van adelantados, rojo si van atrasados;
- el desvío del bloque del relator actual (Camila 15 min, Jorge 13, Gonzalo 12);
- la siguiente slide y el guion completo, con acotaciones y la indicación de cuándo avanzar;
- el aviso **«RELEVO → Jorge / Gonzalo»** 30 segundos antes de cada cambio de relator.

Con dos pantallas, lleva la ventana del presentador al notebook y la presentación en pantalla completa (F) al proyector. Las flechas también funcionan desde la ventana del presentador.

## Antes de la charla (5 minutos)

1. Abrir `deck/index.html` en Chrome o Edge y presionar **P**. Si el navegador bloquea la ventana emergente, permitirla para ese archivo.
2. Ir a la slide 16 (demo), avanzar una vez y confirmar que el video se reproduce.
3. Presionar **Home** para volver al inicio y **F** para la pantalla completa en el proyector.
4. El cronómetro se reinicia con doble clic sobre el reloj.

## Reel de Camila (slide 3)

- Aparece con un avance y se reproduce **con sonido** (dura 46 s; la idea es dejarlo correr 15 a 20 s).
- Si avanzas desde la ventana del presentador, el navegador puede bloquear el audio. En ese caso el reel arranca en silencio y muestra «Clic para activar el sonido»: un clic sobre el video lo activa. Para evitarlo, avanza ese slide desde la ventana principal.
- Al pasar al slide siguiente, el reel se detiene y vuelve al inicio.

## Demo de Jorge (slide 16)

- **Por defecto:** el video se reproduce con un avance. No tiene audio; Jorge narra encima (ver `GUION.md`, J5).
- **En vivo (opcional):** seguir `demo-en-vivo/LEEME.md`. El CSV es una encuesta **ficticia** de 300 egresados, generada con `demo-en-vivo/generar_datos.py`.
- Si el video no carga, la slide muestra un respaldo con el prompt. El mensaje clave es «Supuestos a validar».

## Pendientes antes del lunes

- `[PERSONALIZAR]` Slide G2: la anécdota de Gonzalo (30 a 40 segundos), en el guion y en las notas.
- `[VALIDAR con Gonzalo]` Slide G3: confirmar que el ejemplo «ticket → proceso → cliente → región» representa su realidad.
- `[PERSONALIZAR]` Slide G8: el contacto (LinkedIn o red) de cada relator, en `deck/src/index.src.html`.
- Camila: revisar que sus textos y tiempos le acomoden (su docx era de 20 minutos y aquí tiene 15).

## Editar la presentación

El HTML final se genera. No hay que editar `deck/index.html` directamente:

1. Editar `deck/src/index.src.html`.
2. Ejecutar `python deck/build.py`, que vuelve a incrustar las fuentes, las fotos y el póster del video.
