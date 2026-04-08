import graphene
from graphene_django import DjangoObjectType
from .models import Mascota, Cliente, Medicamento


class MedicamentoType(DjangoObjectType):
    class Meta:
        model = Medicamento
        fields = ('id', 'nombre', 'descripcion', 'dosis')


class ClienteType(DjangoObjectType):
    class Meta:
        model = Cliente
        fields = ('id', 'cedula', 'nombres', 'apellidos', 'direccion', 'telefono')


class MascotaType(DjangoObjectType):
    class Meta:
        model = Mascota
        fields = ('id', 'identificacion', 'nombre', 'raza', 'edad', 'peso', 'cliente', 'medicamento')


# Consultas para leer datos

class Query(graphene.ObjectType):

    # Mascotas
    todas_las_mascotas = graphene.List(MascotaType)
    mascota_por_id = graphene.Field(MascotaType, id=graphene.Int(required=True))

    # Clientes
    todos_los_clientes = graphene.List(ClienteType)
    cliente_por_id = graphene.Field(ClienteType, id=graphene.Int(required=True))

    # Medicamentos
    todos_los_medicamentos = graphene.List(MedicamentoType)
    medicamento_por_id = graphene.Field(MedicamentoType, id=graphene.Int(required=True))

    #  RESOLVERS de Queries 

    def resolve_todas_las_mascotas(root, info):
        return Mascota.objects.select_related('cliente', 'medicamento').all()

    def resolve_mascota_por_id(root, info, id):
        try:
            return Mascota.objects.get(pk=id)
        except Mascota.DoesNotExist:
            return None

    def resolve_todos_los_clientes(root, info):
        return Cliente.objects.all()

    def resolve_cliente_por_id(root, info, id):
        try:
            return Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            return None

    def resolve_todos_los_medicamentos(root, info):
        return Medicamento.objects.all()

    def resolve_medicamento_por_id(root, info, id):
        try:
            return Medicamento.objects.get(pk=id)
        except Medicamento.DoesNotExist:
            return None


# MUTATIONS - Crear, Editar y Eliminar datos


class CrearMascota(graphene.Mutation):
    class Arguments:
        identificacion = graphene.String(required=True)
        nombre         = graphene.String(required=True)
        raza           = graphene.String(required=True)
        edad           = graphene.Int(required=True)
        peso           = graphene.Float(required=True)
        cliente_id     = graphene.Int(required=True)
        medicamento_id = graphene.Int()

    mascota = graphene.Field(MascotaType)
    ok      = graphene.Boolean()

    def mutate(root, info, identificacion, nombre, raza, edad, peso, cliente_id, medicamento_id=None):
        cliente = Cliente.objects.get(pk=cliente_id)
        medicamento = Medicamento.objects.get(pk=medicamento_id) if medicamento_id else None
        mascota = Mascota.objects.create(
            identificacion=identificacion,
            nombre=nombre, raza=raza, edad=edad, peso=peso,
            cliente=cliente, medicamento=medicamento
        )
        return CrearMascota(mascota=mascota, ok=True)


class EditarMascota(graphene.Mutation):
    class Arguments:
        id     = graphene.Int(required=True)
        nombre = graphene.String()
        raza   = graphene.String()
        edad   = graphene.Int()
        peso   = graphene.Float()

    mascota = graphene.Field(MascotaType)
    ok      = graphene.Boolean()

    def mutate(root, info, id, nombre=None, raza=None, edad=None, peso=None):
        try:
            mascota = Mascota.objects.get(pk=id)
            if nombre: mascota.nombre = nombre
            if raza:   mascota.raza   = raza
            if edad:   mascota.edad   = edad
            if peso:   mascota.peso   = peso
            mascota.save()
            return EditarMascota(mascota=mascota, ok=True)
        except Mascota.DoesNotExist:
            return EditarMascota(mascota=None, ok=False)


class EliminarMascota(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, id):
        try:
            Mascota.objects.get(pk=id).delete()
            return EliminarMascota(ok=True)
        except Mascota.DoesNotExist:
            return EliminarMascota(ok=False)


class CrearCliente(graphene.Mutation):
    class Arguments:
        cedula    = graphene.String(required=True)
        nombres   = graphene.String(required=True)
        apellidos = graphene.String(required=True)
        direccion = graphene.String(required=True)
        telefono  = graphene.String(required=True)

    cliente = graphene.Field(ClienteType)
    ok      = graphene.Boolean()

    def mutate(root, info, cedula, nombres, apellidos, direccion, telefono):
        cliente = Cliente.objects.create(
            cedula=cedula, nombres=nombres, apellidos=apellidos,
            direccion=direccion, telefono=telefono
        )
        return CrearCliente(cliente=cliente, ok=True)


class EliminarCliente(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, id):
        try:
            Cliente.objects.get(pk=id).delete()
            return EliminarCliente(ok=True)
        except Cliente.DoesNotExist:
            return EliminarCliente(ok=False)


class CrearMedicamento(graphene.Mutation):
    class Arguments:
        nombre      = graphene.String(required=True)
        descripcion = graphene.String(required=True)
        dosis       = graphene.String(required=True)

    medicamento = graphene.Field(MedicamentoType)
    ok          = graphene.Boolean()

    def mutate(root, info, nombre, descripcion, dosis):
        medicamento = Medicamento.objects.create(
            nombre=nombre, descripcion=descripcion, dosis=dosis
        )
        return CrearMedicamento(medicamento=medicamento, ok=True)


class EliminarMedicamento(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, id):
        try:
            Medicamento.objects.get(pk=id).delete()
            return EliminarMedicamento(ok=True)
        except Medicamento.DoesNotExist:
            return EliminarMedicamento(ok=False)




class Mutation(graphene.ObjectType):
    crear_mascota      = CrearMascota.Field()
    editar_mascota     = EditarMascota.Field()
    eliminar_mascota   = EliminarMascota.Field()
    crear_cliente      = CrearCliente.Field()
    eliminar_cliente   = EliminarCliente.Field()
    crear_medicamento  = CrearMedicamento.Field()
    eliminar_medicamento = EliminarMedicamento.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)