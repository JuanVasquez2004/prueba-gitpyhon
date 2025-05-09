# banco_digital.py
# Sistema básico de operaciones bancarias con reglas de negocio

from datetime import datetime, timedelta
import random

class CuentaBancaria:
    def __init__(self, titular, saldo_inicial=0, tipo_cuenta='AHORRO'):
        self.titular = titular
        self.saldo = saldo_inicial
        self.tipo_cuenta = tipo_cuenta
        self.numero_cuenta = self.generar_numero_cuenta()
        self.ultimas_transacciones = []
        self.limite_diario = 10000000 if tipo_cuenta == 'CORRIENTE' else 5000000
        self.saldo_minimo = 20000 if tipo_cuenta == 'CORRIENTE' else 0

    def generar_numero_cuenta(self):
        return ''.join(str(random.randint(0, 9)) for _ in range(15))

    def validar_monto(self, monto):
        if not isinstance(monto, (int, float)):
            raise ValueError("El monto debe ser numérico")
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        return True

    def depositar(self, monto):
        try:
            self.validar_monto(monto)
            
            if self.tipo_cuenta == 'AHORRO' and monto > 20000000:
                raise ValueError("Límite de depósito excedido para cuenta de ahorro")
                
            self.saldo += monto
            self.registrar_transaccion('DEPOSITO', monto)
            return f"Depósito exitoso. Nuevo saldo: ${self.saldo:,.2f}"
            
        except ValueError as e:
            return f"Error en depósito: {str(e)}"

    def retirar(self, monto):
        try:
            self.validar_monto(monto)
            
            if self.saldo - monto < self.saldo_minimo:
                raise ValueError("Fondos insuficientes según saldo mínimo requerido")
                
            if monto > self.limite_diario:
                raise ValueError(f"Supera el límite diario de ${self.limite_diario:,.2f}")
                
            self.saldo -= monto
            self.registrar_transaccion('RETIRO', monto)
            return f"Retiro exitoso. Nuevo saldo: ${self.saldo:,.2f}"
            
        except ValueError as e:
            return f"Error en retiro: {str(e)}"

    def transferir(self, monto, cuenta_destino):
        try:
            self.validar_monto(monto)
            
            if self.tipo_cuenta == 'AHORRO' and len(self.ultimas_transacciones) >= 5:
                raise ValueError("Límite de transacciones mensuales excedido")
                
            if self.saldo - monto < self.saldo_minimo:
                raise ValueError("Saldo insuficiente para transferencia")
                
            # Aplicar comisión para cuentas corrientes
            if self.tipo_cuenta == 'CORRIENTE' and monto > 5000000:
                comision = monto * 0.001
                monto_total = monto + comision
            else:
                monto_total = monto
                
            self.saldo -= monto_total
            cuenta_destino.depositar(monto)
            self.registrar_transaccion('TRANSFERENCIA', monto)
            return f"Transferencia exitosa. Nuevo saldo: ${self.saldo:,.2f}"
            
        except ValueError as e:
            return f"Error en transferencia: {str(e)}"

    def registrar_transaccion(self, tipo, monto):
        transaccion = {
            'fecha': datetime.now(),
            'tipo': tipo,
            'monto': monto,
            'saldo_restante': self.saldo
        }
        self.ultimas_transacciones.append(transaccion)

    def verificar_historial_fraude(self):
        # Regla: Más de 3 transacciones grandes en menos de 1 hora
        transacciones_grandes = [t for t in self.ultimas_transacciones 
                               if t['monto'] > 5000000]
        for i in range(len(transacciones_grandes)-3):
            tiempo_transacciones = transacciones_grandes[i+3]['fecha'] - transacciones_grandes[i]['fecha']
            if tiempo_transacciones < timedelta(hours=1):
                return True
        return False

class SolicitudCredito:
    def __init__(self, cliente, ingresos_mensuales, deuda_actual, puntaje_credito):
        self.cliente = cliente
        self.ingresos_mensuales = ingresos_mensuales
        self.deuda_actual = deuda_actual
        self.puntaje_credito = puntaje_credito

    def aprobar_credito(self, monto_solicitado, plazo_meses):
        try:
            # Regla 1: Puntaje de crédito mínimo
            if self.puntaje_credito < 650:
                return False, "Puntaje de crédito insuficiente"
                
            # Regla 2: Capacidad de pago
            deuda_total = self.deuda_actual + (monto_solicitado / plazo_meses)
            if deuda_total > (self.ingresos_mensuales * 0.4):
                return False, "Relación deuda/ingreso muy alta"
                
            # Regla 3: Límites según plazo
            if plazo_meses < 6 or plazo_meses > 60:
                return False, "Plazo no válido (6-60 meses)"
                
            # Regla 4: Monto máximo según ingresos
            if monto_solicitado > (self.ingresos_mensuales * 24):
                return False, "Monto solicitado excede capacidad financiera"
                
            return True, "Crédito aprobado"
            
        except Exception as e:
            return False, f"Error en validación: {str(e)}"

if __name__ == "__main__":
    # Crear cuentas de ejemplo
    cuenta_juan = CuentaBancaria("Juan Pérez", 5000000, 'CORRIENTE')
    cuenta_maria = CuentaBancaria("María García", 1000000, 'AHORRO')

    # Simular operaciones
    print(cuenta_juan.depositar(2000000))
    print(cuenta_juan.retirar(500000))
    print(cuenta_juan.transferir(1500000, cuenta_maria))
    
    # Simular solicitud de crédito
    solicitud = SolicitudCredito(cuenta_juan, 5000000, 1000000, 720)
    aprobado, mensaje = solicitud.aprobar_credito(30000000, 12)
    print(f"\nSolicitud de crédito: {mensaje}")