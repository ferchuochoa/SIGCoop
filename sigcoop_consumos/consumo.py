from trytond.model import ModelSQL, ModelView, fields


class Consumo(ModelSQL, ModelView):
    "Consumo"
    __name__ = 'sigcoop_consumos.consumo'

    id_suministro = fields.Many2One('sigcoop_usuario.suministro', 'Suministro', required=True)
    id_medidor = fields.Char('Medidor', required=True)
    periodo = fields.Char('Periodo', required=True)
    fecha_anterior = fields.Date('Fecha lec. anterior', required=True)
    lectura_anterior = fields.BigInteger('Lectura anterior', required=True)
    fecha_actual = fields.Date('Fecha lec. actual', required=True)
    lectura_actual = fields.BigInteger('Lectura actual', required=True)
    consumo_neto = fields.BigInteger('Consumo Neto', required=True)

    

