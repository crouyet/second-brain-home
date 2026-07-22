---
name: meal-prep-recordatorios-semanales
description: Domingos 9am: crea en Notion Tareas los recordatorios con fecha de domingo (Chefcito), martes (bajar carne) y miércoles (cocinar+portionar)
---

Hoy es domingo. Calculá la fecha de HOY (domingo), del martes y del miércoles de esta semana.

Usá el conector de Notion (servidor dc69f0e5-f9ac-43af-9363-25b9215ce1db). Antes de crear nada, consultá la base Tareas (data source `{{TAREAS_COLLECTION_ID}}`) filtrando por esas 3 fechas de Due para chequear si ya existen tareas con esos nombres — si ya existen, no dupliques, saltealas.

Creá las que falten:

1. Domingo (Due = hoy): Task name "Chefcito: polvitos + salad bar + snack fácil", Status "TO-DO", Priority "Medium", Tags ["🪫 Low Batery"], icon 🥣, Summary "Checklist completo en vault/Projects/Chefcito/Recetas.md. Elegir 1 snack sin horno de la lista, o dátiles + frutos secos si no hay tiempo."
2. Martes (Due = fecha del martes): Task name "Bajar carne del freezer + chequear verduras", Status "TO-DO", Priority "Medium", Tags ["⏲️ -5 mins"], icon 🥩, Summary "Sin esto el miércoles no sale completo. 2 min."
3. Miércoles (Due = fecha del miércoles): Task name "Cocinar y portionar: guiso + suprema + carne de pastura", Status "TO-DO", Priority "High", Tags ["🏙️ Fuera de casa"], icon 🍲, Summary "Día de la chica. Deja la semana armada: lunes guiso, martes suprema, jueves carne de pastura, viernes sobras. Si sobra tiempo: legumbre + 1 snack de horno de Recetas.md."

Contexto: sistema de meal prep semanal de la usuaria documentado en vault/Projects/Casa/README.md y vault/Projects/Chefcito/Recetas.md — reemplaza las viandas por delivery. Estas tareas con fecha son lo que hace que aparezcan en Notion Calendar con anticipación, para que nunca llegue a la hora de comer sin nada armado. No hace falta avisarle por Telegram salvo que algo falle — es silencioso, las tareas simplemente aparecen en su Calendar.

Si es una semana de viaje o excepción conocida (por ejemplo la semana del 28/7 al 2/8, viaje al Delta), NO crees ninguna de las 3 tareas esa semana — se puede detectar chequeando eventos de Google Calendar con el conector de calendar si hay un evento de viaje esos días.