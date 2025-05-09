from data.data import CuentaBancaria
import datetime

def test_caso_1_saldo_insuficiente():
    """Intentar retirar más dinero del saldo disponible"""
    cuenta = CuentaBancaria("1234567890", "Cliente Prueba")
    cuenta.depositar(500)
    try:
        cuenta.retirar(1000)
    except Exception as e:
        print(f"Error esperado (Caso 1): {str(e)}")

def test_caso_2_limite_diario():
    """Superar el límite diario de transacciones"""
    cuenta = CuentaBancaria("0987654321", "Cliente Prueba")
    cuenta.depositar(20000)
    
    # Intentar hacer 11 transacciones en un día
    for i in range(11):
        try:
            cuenta.retirar(1000)
        except Exception as e:
            print(f"Error esperado (Caso 2): {str(e)}")
            break

def test_caso_3_monto_negativo():
    """Intentar hacer una transacción con monto negativo"""
    cuenta = CuentaBancaria("1111111111", "Cliente Prueba")
    try:
        cuenta.depositar(-1000)
    except Exception as e:
        print(f"Error esperado (Caso 3): {str(e)}")

def test_caso_4_formato_cuenta_invalido():
    """Crear cuenta con número de cuenta inválido"""
    try:
        cuenta = CuentaBancaria("12345", "Cliente Prueba")  # Solo 5 dígitos
    except Exception as e:
        print(f"Error esperado (Caso 4): {str(e)}")

def test_caso_5_transferencia_invalida():
    """Transferencia entre cuentas con problemas"""
    cuenta1 = CuentaBancaria("1234567890", "Cliente 1")
    cuenta2 = CuentaBancaria("0987654321", "Cliente 2")
    
    # Cuenta 1 tiene saldo insuficiente
    cuenta1.depositar(100)
    try:
        cuenta1.transferir(cuenta2, 200)
    except Exception as e:
        print(f"Error esperado (Caso 5.1): {str(e)}")
    
    # Cuenta 2 está bloqueada
    cuenta2.bloquear_cuenta()
    try:
        cuenta1.transferir(cuenta2, 50)
    except Exception as e:
        print(f"Error esperado (Caso 5.2): {str(e)}")

def test_caso_6_limite_monto():
    """Intentar hacer una transacción que excede el límite diario"""
    cuenta = CuentaBancaria("1111111111", "Cliente Prueba")
    cuenta.depositar(20000)
    try:
        cuenta.retirar(15000)  # Excede el límite diario de 10000
    except Exception as e:
        print(f"Error esperado (Caso 6): {str(e)}")

def test_caso_7_operaciones_con_cuenta_bloqueada():
    """Intentar operar con una cuenta bloqueada"""
    cuenta = CuentaBancaria("2222222222", "Cliente Prueba")
    cuenta.bloquear_cuenta()
    
    try:
        cuenta.depositar(1000)
    except Exception as e:
        print(f"Error esperado (Caso 7.1): {str(e)}")
    
    try:
        cuenta.retirar(1000)
    except Exception as e:
        print(f"Error esperado (Caso 7.2): {str(e)}")

def test_caso_8_tipo_transaccion_invalido():
    """Intentar crear una transacción con tipo inválido"""
    cuenta = CuentaBancaria("3333333333", "Cliente Prueba")
    try:
        cuenta.depositar(1000, "compra")  # Tipo de transacción inválido
    except Exception as e:
        print(f"Error esperado (Caso 8): {str(e)}")

def main():
    print("=== Iniciando pruebas de casos de error ===")
    print("\nCaso 1: Saldo insuficiente")
    test_caso_1_saldo_insuficiente()
    
    print("\nCaso 2: Límite diario de transacciones")
    test_caso_2_limite_diario()
    
    print("\nCaso 3: Monto negativo")
    test_caso_3_monto_negativo()
    
    print("\nCaso 4: Formato de número de cuenta inválido")
    test_caso_4_formato_cuenta_invalido()
    
    print("\nCaso 5: Transferencias inválidas")
    test_caso_5_transferencia_invalida()
    
    print("\nCaso 6: Límite de monto")
    test_caso_6_limite_monto()
    
    print("\nCaso 7: Operaciones con cuenta bloqueada")
    test_caso_7_operaciones_con_cuenta_bloqueada()
    
    print("\nCaso 8: Tipo de transacción inválido")
    test_caso_8_tipo_transaccion_invalido()
    
    print("\n=== Pruebas completadas ===")

if __name__ == "__main__":
    main()