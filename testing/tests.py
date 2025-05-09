class Banco:
    """Clase que maneja las validaciones y operaciones bancarias"""
    
    def __init__(self):
        self.cuentas = {}
        self.limite_diario = 10000  # Límite diario de transacciones
        self.max_transacciones = 10  # Máximo número de transacciones diarias
        
    def validar_numero_cuenta(self, numero_cuenta: str) -> bool:
        """
        Valida que el número de cuenta tenga el formato correcto
        """
        if not numero_cuenta.isdigit():
            print("Error: El número de cuenta debe contener solo dígitos")
            return False
            
        if len(numero_cuenta) != 10:
            print("Error: El número de cuenta debe tener 10 dígitos")
            return False
            
        return True
        
    def validar_monto(self, monto: float) -> bool:
        """
        Valida que el monto sea válido
        """
        if monto <= 0:
            print("Error: El monto debe ser mayor a cero")
            return False
            
        if monto > self.limite_diario:
            print(f"Error: El monto excede el límite diario de ${self.limite_diario}")
            return False
            
        return True
        
    def validar_saldo(self, cuenta: dict, monto: float) -> bool:
        """
        Valida que haya saldo suficiente
        """
        if cuenta['saldo'] < monto:
            print("Error: Saldo insuficiente")
            return False
            
        return True
        
    def validar_estado_cuenta(self, cuenta: dict) -> bool:
        """
        Valida que la cuenta esté activa
        """
        if cuenta['estado'] != 'activa':
            print("Error: La cuenta está bloqueada")
            return False
            
        return True
        
    def validar_transacciones_diarias(self, cuenta: dict) -> bool:
        """
        Valida el límite diario de transacciones
        """
        if cuenta['transacciones_hoy'] >= self.max_transacciones:
            print(f"Error: Se ha alcanzado el límite diario de {self.max_transacciones} transacciones")
            return False
            
        return True
        
    def crear_cuenta(self, numero_cuenta: str, nombre: str) -> dict:
        """
        Crea una nueva cuenta si el número es válido
        """
        if not self.validar_numero_cuenta(numero_cuenta):
            return None
            
        if numero_cuenta in self.cuentas:
            print("Error: El número de cuenta ya existe")
            return None
            
        nueva_cuenta = {
            'numero': numero_cuenta,
            'nombre': nombre,
            'saldo': 0,
            'estado': 'activa',
            'transacciones_hoy': 0
        }
        self.cuentas[numero_cuenta] = nueva_cuenta
        return nueva_cuenta
        
    def depositar(self, numero_cuenta: str, monto: float) -> bool:
        """
        Realiza un depósito en la cuenta
        """
        if numero_cuenta not in self.cuentas:
            print("Error: Cuenta no encontrada")
            return False
            
        cuenta = self.cuentas[numero_cuenta]
        
        if not self.validar_estado_cuenta(cuenta):
            return False
            
        if not self.validar_monto(monto):
            return False
            
        if not self.validar_transacciones_diarias(cuenta):
            return False
            
        cuenta['saldo'] += monto
        cuenta['transacciones_hoy'] += 1
        print(f"Depósito exitoso. Nuevo saldo: ${cuenta['saldo']}")
        return True
        
    def retirar(self, numero_cuenta: str, monto: float) -> bool:
        """
        Realiza un retiro de la cuenta
        """
        if numero_cuenta not in self.cuentas:
            print("Error: Cuenta no encontrada")
            return False
            
        cuenta = self.cuentas[numero_cuenta]
        
        if not self.validar_estado_cuenta(cuenta):
            return False
            
        if not self.validar_monto(monto):
            return False
            
        if not self.validar_saldo(cuenta, monto):
            return False
            
        if not self.validar_transacciones_diarias(cuenta):
            return False
            
        cuenta['saldo'] -= monto
        cuenta['transacciones_hoy'] += 1
        print(f"Retiro exitoso. Nuevo saldo: ${cuenta['saldo']}")
        return True
        
    def transferir(self, cuenta_origen: str, cuenta_destino: str, monto: float) -> bool:
        """
        Realiza una transferencia entre cuentas
        """
        if cuenta_origen not in self.cuentas or cuenta_destino not in self.cuentas:
            print("Error: Una de las cuentas no existe")
            return False
            
        origen = self.cuentas[cuenta_origen]
        destino = self.cuentas[cuenta_destino]
        
        if not self.validar_estado_cuenta(origen) or not self.validar_estado_cuenta(destino):
            return False
            
        if not self.validar_monto(monto):
            return False
            
        if not self.validar_saldo(origen, monto):
            return False
            
        if not self.validar_transacciones_diarias(origen) or not self.validar_transacciones_diarias(destino):
            return False
            
        # Realizar la transferencia
        origen['saldo'] -= monto
        destino['saldo'] += monto
        origen['transacciones_hoy'] += 1
        destino['transacciones_hoy'] += 1
        
        print(f"Transferencia exitosa. Nuevo saldo origen: ${origen['saldo']}")
        print(f"Nuevo saldo destino: ${destino['saldo']}")
        return True
        
    def bloquear_cuenta(self, numero_cuenta: str) -> bool:
        """
        Bloquea una cuenta
        """
        if numero_cuenta not in self.cuentas:
            print("Error: Cuenta no encontrada")
            return False
            
        self.cuentas[numero_cuenta]['estado'] = 'bloqueada'
        print("Cuenta bloqueada exitosamente")
        return True
        
    def desbloquear_cuenta(self, numero_cuenta: str) -> bool:
        """
        Desbloquea una cuenta
        """
        if numero_cuenta not in self.cuentas:
            print("Error: Cuenta no encontrada")
            return False
            
        self.cuentas[numero_cuenta]['estado'] = 'activa'
        print("Cuenta desbloqueada exitosamente")
        return True

# Ejemplo de uso
if __name__ == "__main__":
    banco = Banco()
    
    # Crear cuentas
    cuenta1 = banco.crear_cuenta("1234567890", "Juan Pérez")
    cuenta2 = banco.crear_cuenta("0987654321", "María García")
    
    # Intentar crear cuenta con número inválido
    banco.crear_cuenta("12345", "Cliente Inválido")  # Debería fallar
    
    # Hacer operaciones
    banco.depositar("1234567890", 1000)
    banco.retirar("1234567890", 500)
    
    # Intentar retirar más de lo disponible
    banco.retirar("1234567890", 1000)  # Debería fallar
    
    # Hacer transferencia
    banco.transferir("1234567890", "0987654321", 200)
    
    # Bloquear cuenta
    banco.bloquear_cuenta("1234567890")
    
    # Intentar operar con cuenta bloqueada
    banco.depositar("1234567890", 1000)  # Debería fallar
    
    # Desbloquear cuenta
    banco.desbloquear_cuenta("1234567890")
    
    # Intentar hacer una transacción que excede el límite diario
    banco.depositar("1234567890", 15000)  # Debería fallar
    
    print("\nEstado final de las cuentas:")
    for numero, cuenta in banco.cuentas.items():
        print(f"Cuenta {numero}: Saldo = ${cuenta['saldo']}, Estado = {cuenta['estado']}, Transacciones hoy = {cuenta['transacciones_hoy']}")