# Respuestas de fundamentos (sin IA)

## Python
Comportamiento del codigo original, corrección y casos comprobados:

el return estaba dentro del for, por lo que la funcion terminaba despues del primer pedido y devolví none si la lista estaba vacia, lo moví fuera del ciclo y comprobé que devuelve 2 con dos pedidos pendientes y 0 con una lista vacia

## SQL
Consulta parametrizada para listar pedidos pendientes y por qué no concatenar datos:

conn.execute("SELECT * FROM pedidos WHERE estado = ?",("pendiente",))

el ? permite pasar el estado como parámetro, asi evito concatenar valores en la consulta

## HTTP
Diferencia entre 400, 404 y 422 en este contrato:

400: un valor no cumple las reglas, como un estado desconocido o un cliente formado solo por espacios

404: el pedido solicitado no existe

422: faltan campos obligatorios o tienen tipos incorrectos, como enviar {} al crear un pedido. Probé el endpoint POST /pedidos enviando un objeto vacio {}. La API respondió 422 porque faltaban los campos obligatorios cliente y descripcion

## React
Problema del fragmento, solución sin mutación y caso id inexistente:

el codigo modifica directamente el estado y usa el mismo arreglo, por lo que react podria no actualizar la pantalla y ambién falla si no encuentra el ID

lo corregiria con map, creando un arreglo nuevo y una copia del pedido que quiera cambiar, asi no modifico el estado original y si el ID no existe, no cambia ningún pedido ni se produce un error

## Vite / Next.js
Diferencia entre estas herramientas y dónde se ejecuta cada fetch en este ejercicio:

Vite sirve para desarrollar y compilar la aplicación React. En este proyecto, consulta la API desde el navegador.

Next.js es un framework de React que también permite ejecutar código en el servidor. La página /resumen consulta la API desde ese servidor para mostrar los conteos de pedidos.

Son dos aplicaciones separadas que usan la misma API de Python.
