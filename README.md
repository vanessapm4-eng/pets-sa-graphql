#  Pets API - GraphQL

## Descripción
API desarrollada utilizando GraphQL para la gestión de información de mascotas, permitiendo consultar y manipular datos de manera eficiente mediante un único endpoint.

A diferencia de las APIs REST, GraphQL permite solicitar exactamente los datos necesarios en una sola petición, optimizando el consumo de información.

## ¿Qué es GraphQL?
GraphQL es un lenguaje de consultas para APIs que permite a los clientes definir qué datos necesitan, evitando el envío de información innecesaria y reduciendo múltiples solicitudes.

## Funcionalidades
- Consulta de mascotas (Query)
- Creación de registros (Mutation)
- Actualización de datos
- Eliminación de registros

## Operaciones GraphQL

### Query 
```graphql
query {
  mascotas {
    nombre
    edad
  }
}
```
## Mutation 
```
mutation {
  crearMascota(nombre: "Luna", edad: 3) {
    id
    nombre
  }
}
```
Estado del proyecto: 
Proyecto académico en desarrollo

## Autor
Vanessa Palacios
