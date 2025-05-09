from datetime import datetime
from typing import Optional, List, Dict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import re

class BancoException(Exception):
    """Excepción base para errores bancarios"""
    pass

class SaldoInsuficienteError(BancoException):
    """Se intenta retirar más dinero del disponible"""
    pass

class LimiteDiarioExcedidoError(BancoException):
    """Se excede el límite diario de transacciones"""
    pass

class CuentaInactivaError(BancoException):
    """La cuenta está inactiva o bloqueada"""
    pass

class Transaccion:
    """Representa una transacción bancaria"""
    
    def __init__(self, tipo: str, monto: Decimal, fecha: datetime, descripcion: Optional[str] = None):
        if tipo not in ['deposito', 'retiro', 'transferencia']:
            raise ValueError("Tipo de transacción no válido")
        
        try:
            self.monto = Decimal(monto)
        except InvalidOperation:
            raise ValueError("Monto no válido")
            
        self.tipo = tipo
        self.fecha = fecha
        self.descripcion = descripcion or ""
        
    def __str__(self):
        return f"{self.tipo.capitalize()}: ${self.monto:.2f} - {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"

class CuentaBancaria:
    """Clase que representa una cuenta bancaria con validaciones"""
    
    def __init__(self, numero_cuenta: str, titular: str, saldo_inicial: Decimal = Decimal('0.00')):
        self.numero_cuenta = self._validar_numero_cuenta(numero_cuenta)
        self.titular = titular
        self.saldo = saldo_inicial
        self.transacciones: List[Transaccion] = []
        self.limite_diario = Decimal('10000.00')
        self.transacciones_hoy = 0
        self.estado = 'activa'
        self.max_transacciones_diarias = 10
        
    def _validar_numero_cuenta(self, numero: str) -> str:
        """Valida que el número de cuenta tenga el formato correcto"""
        if not re.match(r'^\d{10}$', numero):
            raise ValueError("El número de cuenta debe tener 10 dígitos")
        return numero
        
    def _validar_limite_diario(self, monto: Decimal) -> None:
        """Verifica si la transacción excede el límite diario"""
        if self.transacciones_hoy >= self.max_transacciones_diarias:
            raise LimiteDiarioExcedidoError("Se ha alcanzado el límite diario de transacciones")
            
        if monto > self.limite_diario:
            raise LimiteDiarioExcedidoError(f"Monto excede el límite diario de ${self.limite_diario:.2f}")
            
    def depositar(self, monto: Decimal, descripcion: Optional[str] = None) -> None:
        """Realiza un depósito en la cuenta"""
        if self.estado != 'activa':
            raise CuentaInactivaError("La cuenta está inactiva")
            
        try:
            monto = Decimal(monto)
            if monto <= 0:
                raise ValueError("El monto debe ser positivo")
                
            self._validar_limite_diario(monto)
            
            transaccion = Transaccion('deposito', monto, datetime.now(), descripcion)
            self.transacciones.append(transaccion)
            self.saldo += monto
            self.transacciones_hoy += 1
            
        except InvalidOperation:
            raise ValueError("Monto no válido")
            
    def retirar(self, monto: Decimal, descripcion: Optional[str] = None) -> None:
        """Realiza un retiro de la cuenta"""
        if self.estado != 'activa':
            raise CuentaInactivaError("La cuenta está inactiva")
            
        try:
            monto = Decimal(monto)
            if monto <= 0:
                raise ValueError("El monto debe ser positivo")
                
            if monto > self.saldo:
                raise SaldoInsuficienteError("Saldo insuficiente")
                
            self._validar_limite_diario(monto)
            
            transaccion = Transaccion('retiro', monto, datetime.now(), descripcion)
            self.transacciones.append(transaccion)
            self.saldo -= monto
            self.transacciones_hoy += 1
            
        except InvalidOperation:
            raise ValueError("Monto no válido")
            
    def transferir(self, cuenta_destino: 'CuentaBancaria', monto: Decimal, descripcion: Optional[str] = None) -> None:
        """Realiza una transferencia a otra cuenta"""
        if self.estado != 'activa' or cuenta_destino.estado != 'activa':
            raise CuentaInactivaError("Una de las cuentas está inactiva")
            
        try:
            monto = Decimal(monto)
            if monto <= 0:
                raise ValueError("El monto debe ser positivo")
                
            if monto > self.saldo:
                raise SaldoInsuficienteError("Saldo insuficiente")
                
            self._validar_limite_diario(monto)
            
            # Realizar la transferencia
            self.retirar(monto, f"Transferencia a {cuenta_destino.numero_cuenta}")
            cuenta_destino.depositar(monto, f"Transferencia de {self.numero_cuenta}")
            
        except InvalidOperation:
            raise ValueError("Monto no válido")
            
    def obtener_estado(self) -> Dict:
        """Retorna el estado actual de la cuenta"""
        return {
            'numero_cuenta': self.numero_cuenta,
            'titular': self.titular,
            'saldo': float(self.saldo),
            'estado': self.estado,
            'transacciones_hoy': self.transacciones_hoy,
            'limite_diario': float(self.limite_diario)
        }
        
    def bloquear_cuenta(self) -> None:
        """Bloquea la cuenta"""
        self.estado = 'bloqueada'
        
    def desbloquear_cuenta(self) -> None:
        """Desbloquea la cuenta"""
        self.estado = 'activa'
        
    def reiniciar_transacciones_diarias(self) -> None:
        """Reinicia el contador de transacciones diarias"""
        self.transacciones_hoy = 0
        
    def __str__(self):
        return f"Cuenta {self.numero_cuenta} - Titular: {self.titular} - Saldo: ${self.saldo:.2f}"