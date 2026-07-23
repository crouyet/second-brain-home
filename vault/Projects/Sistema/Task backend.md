# Task backend — nota de diseño

El sistema es **Notion-first**: ~11 skills/scheduled-tasks hablan directo con las tools del
connector de Notion y asumen su modelo (collection ids, props `Due`/`Status`/`Priority`/`Tags`,
Reflections con agregación, Habits como tracker diario). No hay capa de abstracción de backend.

**Portabilidad hoy:** adaptable con laburo dirigido, no con un toggle. Como los skills son prompts
en markdown (no código), "reescribir" es editar instrucciones — un Claude lo hace en el setup.
- **Tareas** → mapean bien a otra herramienta (Trello: card=tarea, due date=`Due`, lista=`Status`,
  labels=`Priority`/`Tags`).
- **Reflections y Habits** → NO encajan en herramientas tipo kanban: necesitan una DB con campos.
  Un usuario de otra herramienta termina híbrido (Tareas afuera, Habits/Reflections en Notion o
  markdown del vault).

**La jugada mínima futura (YAGNI hasta que haya demanda real):** NO abstraer todo. Un solo doc
`Projects/Sistema/task-backend.md` declarativo (`herramienta = X`, mapeo de campos) que los ~4
skills de tareas (`planificar`, `ahora`, `revision`, `meal-prep`) consulten en vez de asumir Notion.
Un archivo, no un refactor. Recién cuando alguien lo pida.
