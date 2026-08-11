---
categories: [permanent-note]
subjects: [sistema, cocina, compras]
status: active
---

# Modelo de estado de la cocina

Cómo el sistema sabe qué hay en tu cocina sin mentirte. Es el modelo que usan `/compras`
(qué comprar) y `/chefcito` (qué cocinar), y existe porque **planificar contra estado
supuesto** era la causa raíz de casi todos los errores del sistema: recomendar recalentar
algo que ya se había comido, mandar a comprar lo que estaba en la despensa, planificar
recetas cuyos ingredientes recién se compraban la semana siguiente.

## El principio que ordena todo

> **Nunca inferir "disponible". Solo se infiere hacia abajo.**

El sistema puede *degradar* confianza solo (algo viejo pasa a dudoso, algo usado pasa a
agotado), pero para afirmar que algo **está** necesita un evento real: una compra
confirmada o vos diciéndolo. El error clásico es que el sistema "recuerde" que había,
cuando lo único que sabe es que **hubo**.

## 1. Productos — máquina de estados

Un campo de stock en texto libre (`"queda poco"`, `"pedido en camino"`, `"se terminó?"`)
mezcla estado, cantidad, razón y sustituto en un solo string, y cada agente lo interpreta
distinto. Por eso el estado es un enum y el resto vive aparte.

| Campo | Valores | Para qué |
|---|---|---|
| `estado` | `desconocido` · `disponible` · `bajo` · `agotado` · `pedido` · `pausado` | el estado, y nada más |
| `estado_desde` | fecha ISO | sin esto la vejez del dato no se puede calcular |
| `notas` | texto libre | el "por qué" y los matices, fuera del campo de estado |

**`desconocido` es un estado legítimo**, no un hueco: para un producto del catálogo que
nunca se registró, ni `disponible` ni `agotado` son honestos. Asumir `agotado` hace
recomprar cosas que ya tenías.

**Transiciones — cada una con un único dueño.** Si dos agentes pueden hacer la misma
transición, se pisan:

| De → A | Evento que la dispara | Dueño |
|---|---|---|
| `disponible` → `bajo`/`agotado` | efecto declarado de un plan que llegó a Done | `/chefcito` |
| cualquiera → cualquiera | vos lo decís | **vos — siempre gana** |
| `agotado` → `pedido` | `/compras` crea la tarea del comercio | `/compras` |
| `pedido` → `disponible` | esa tarea pasa a **Done** | `/compras` |
| `pedido` → `agotado` | la tarea cierra pero no se consiguió | `/compras` |
| → `pausado` | decisión explícita de no reponer | vos |

## 2. `dudoso` — otra dimensión, no otro estado

`dudoso` **convive** con el estado, no lo reemplaza. Son dos ejes:

- **estado** = qué creemos que pasa con el producto
- **dudoso** = cuánta confianza le tenemos a esa creencia — **se calcula, no se guarda**

| | fresco | dudoso |
|---|---|---|
| **disponible** | hay, lo sé | *creo* que hay — puede haberse terminado sin que nadie lo anote |
| **agotado** | no hay, lo sé | figura agotado hace rato — puede que ya se haya comprado |

**Para qué sirve la marca**: un producto dudoso es exactamente un producto que hay que
confirmar para poder decidir, y por eso es el candidato natural de la pregunta semanal.
Sin esta marca, la pregunta tendría que ser el catálogo entero o un recorte arbitrario.

## 3. `rol` — cómo se consume, y por eso a quién se le pregunta

No todos los productos se consumen igual, y tratarlos igual llena la pregunta semanal de
ruido. **Una lista con ruido se deja de leer.**

| `rol` | Qué significa | Cómo decae la confianza | Un `agotado` de este rol |
|---|---|---|---|
| `constante` | siempre está (sal, aceite, huevos, ajo) | **no decae con el tiempo.** Solo cambia por un evento | va a la lista siempre: si no está, falta |
| `rotacion` | se consume dentro del ciclo (verdura, fruta, proteína, lácteos) | decae a los `tolerancia_dias` | va a la lista según el mapa de días |
| `esporadico` | se compra **si una receta lo pide Y si ese día tiene buena pinta** | no decae | **NO va a la lista solo** — solo si el menú lo pide |

**Por qué no alcanza `frecuencia`**: mezcla comportamientos opuestos bajo la misma
etiqueta. "Trimestral" contiene tanto la sal y la cúrcuma (que están siempre) como la
salsa picante y el azafrán (que se usan cuando toca). Misma cadencia de compra,
decaimiento de confianza distinto.

**Por qué esto NO viola "nunca inferir disponible"**: `rol` no dice qué hay, dice **a qué
velocidad envejece el dato**. Que tengas un kilo de sal sigue siendo cierto en 60 días;
que tengas un pepino, no. Un `constante` nunca registrado sigue siendo `desconocido` y
hay que confirmarlo una vez — lo que deja de hacer es volver a caducar después.

**`esporadico` no es "raro", es "opcional".** El caso que lo revela: verduras como el
brócoli o la berenjena salen `agotado` y se van derecho a la lista — pero no se compran
porque falten, se compran si una receta las pide y si el puesto ese día las tiene lindas.
Es una decisión subjetiva en el momento, no una reposición.

**`constante` se gana de dos formas, no una**: por frecuencia (un ingrediente que aparece
en decenas de recetas) o por densidad funcional (uno que aparece en una sola receta, pero
es la receta que más te aporta). Si el criterio fuera solo contar, la segunda se cae.

## 4. `origen` — comprado o cocinado

**Un preparado recurrente es un producto que se repone cocinando en vez de comprando.**
Misma máquina de estados, mismo `rol`, misma `tolerancia_dias`, mismo diff. Lo único que
cambia es **a dónde va el gap**:

| `origen` | El gap de un `agotado` sale como |
|---|---|
| `comprado` (default) | una línea de la lista de compras, con comercio y día |
| `cocinado` | un paso del bloque de prep — **`/compras` lo ignora por completo** |

Esto es lo que hace que "que siempre haya algo sano para picar" deje de ser una intención
escrita en un documento y pase a ser un estado con vencimiento que aparece solo cuando se
acaba.

**Por qué no un archivo aparte**: la pregunta "¿hay?" y la transición "se acabó → hay que
reponerlo" son idénticas para un frasco de tahini y para un tupper de legumbres cocidas.
Partirlo en dos sistemas duplicaría el motor para no compartir nada.

## 5. Planificación — el plan declara, el Done confirma

Patrón: **efecto esperado con commit / rollback.**

Al planificar, cada plato declara qué consume y cómo (`agota` o `baja`). Eso se guarda
como *esperado* y **no se aplica**:

- **La tarea NO llega a Done** → *rollback*: no pasó nada, ningún producto cambia de
  estado. El error es asumir que el menú se cumplió.
- **Llega a Done** → *commit*: se aplican los efectos declarados.

### ¿Se terminó o solo bajó? Tres estrategias, de más barata a más cara

1. **Que lo declare la receta al planificar.** El agente ya está mirando receta e
   inventario juntos: si la receta pide 1kg de tomate y hay ½, declara `agota`. Cubre la
   mayoría y cuesta cero — la información está justo ahí.
2. **Heurística por frecuencia, y solo para degradar.** Si la cantidad habitual alcanza
   para N usos y ya hubo N, el producto pasa a **dudoso**, nunca a `agotado`. Inferir "no
   hay" es tan malo como inferir "hay": manda a comprar de más.
3. **Preguntar — pero solo lo que cambia una decisión.** Entra lo que el menú propuesto
   necesita, más 1-2 por rotación. Lo dudoso que nadie va a usar esta semana espera turno.

### El caso especial que elimina una familia entera de errores

**Comida cocinada: default `agota` siempre.** Si no decís que quedó, no hay. No hace falta
declarar nada ni preguntar.

## 6. Normalización y equivalencias

Los ingredientes de las recetas son strings sueltos (`"2 tazas de manteca de sésamo"`).
Sin mapear string → ingrediente canónico, el cruce contra el inventario falla por el
nombre: manda a comprar manteca de sésamo teniendo las semillas.

**Sustituir no es parecerse**: es una relación con dirección y contexto. Es una **tabla
curada que se gana con el uso**, no un algoritmo:

| Falta | Sirve | Contexto |
|---|---|---|
| Manteca de un fruto seco / semilla | El mismo, molido | es literalmente lo mismo |
| Queso duro específico | Cualquier queso duro | ensaladas, gratinar |
| Un endulzante líquido | Otro | repostería, misma proporción |
| Un pescado azul chico | Otro de la misma familia | el punto es el omega-3 y el calcio de la espina, no la especie |

**Regla general**: antes de mandar un ingrediente a comprar, chequear si es **derivable de
algo que ya hay** (mantecas ← semillas, harinas ← granos molidos, leches vegetales, purés).

## 7. La lista de confirmación semanal

El chequeo que cierra el loop: sin él, `dudoso` se acumula y el modelo se degrada solo.

**Qué entra** (6-8 ítems, nunca más — una lista de 30 no se contesta, y una lista sin
contestar es peor que no preguntar porque deja datos viejos disfrazados de nuevos):

1. Los `dudoso` de rol `rotacion` que el menú propuesto necesita.
2. Proteína del freezer: contable, de alto impacto, cambia semana a semana.
3. Rotación: 1-2 `dudoso` más viejos aunque no se usen esta semana.

**Qué NO entra**: comida cocinada de la semana anterior (default `agota`), lo comprado
recién, y todo lo confirmado hace menos de `tolerancia_dias`. Tampoco los `constante` y
`esporadico` nunca registrados: esos son **un barrido de inventario de una sola vez**
(una confirmación por producto en su vida), no una pregunta recurrente. Meterlos ahí tapa
los perecederos, que es lo único que cambia semana a semana.

**Formato — numerada, se responde con números.**

```
Chequeo rápido antes del menú 🧊
1) Pescado blanco
2) Dátiles
3) Almendras
4) Tomate
Decime los números de lo que SÍ tenés. Lo que no menciones lo doy por agotado.
```

El default de la no-respuesta es el seguro: lo que no se menciona se marca agotado, nunca
disponible — el principio de no inferir hacia arriba, aplicado también al silencio.

## Qué habría evitado cada pieza

| Error real del sistema | Pieza que lo ataja |
|---|---|
| Recomendar comida que ya se había comido | default `agota` en comida cocinada |
| Planificar 3 recetas con ingredientes sin comprar | ranking por cobertura + regla "lo que se cocina sale de lo que YA está" |
| Un ítem borrado del inventario → recomprado | `estado` + `estado_desde` (borrar deja de ser posible: hay que transicionar) |
| Recomprar secos de despensa que sí estaban | `dudoso` derivado → pregunta, en vez de asumir faltante |
| Mandar a comprar una manteca teniendo las semillas | normalización + tabla de equivalencias |
| Un pedido que nunca se hizo, invisible durante meses | `pedido` dudoso = **pedido fantasma** → va a la pregunta, nunca se ignora en silencio |
| La lista semanal llena de cosas que no se pensaban comprar | `rol: esporadico` |
| Quedarse sin nada sano para picar | `origen: cocinado` con vencimiento |
