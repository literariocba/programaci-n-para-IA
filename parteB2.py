import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import datetime

class Producto:
    """Representa un producto individual en el inventario."""
    def __init__(self, id_prod, nombre, precio, stock_actual):
        self.id = id_prod
        self.nombre = nombre
        self.precio = precio
        self.stock = stock_actual

    def __str__(self):
        return f"ID: {self.id} | {self.nombre} | Precio: ${self.precio:.2f} | Stock: {self.stock}"

class PredictorVentas:
    """Maneja la lógica de Machine Learning para predecir ventas futuras."""
    def __init__(self):
        self.modelo = LinearRegression()
        self.entrenado = False
        self.metricas = {}

    def entrenar(self, df_ventas):
        """Entrena un modelo basado en el día histórico para predecir cantidad."""
        if len(df_ventas) < 3:
            return False, "Se necesitan al menos 3 registros históricos para entrenar."
        
        # Preprocesamiento simple: usar el índice como variable de tiempo
        X = np.array(range(len(df_ventas))).reshape(-1, 1)
        y = df_ventas['cantidad'].values
        
        self.modelo.fit(X, y)
        predicciones = self.modelo.predict(X)
        
        self.metricas['mse'] = mean_squared_error(y, predicciones)
        self.metricas['r2'] = r2_score(y, predicciones)
        self.entrenado = True
        return True, "Modelo entrenado con éxito."

    def predecir_siguiente(self, n_historicos):
        """Predice la cantidad de ventas para el siguiente periodo."""
        if not self.entrenado:
            return 0
        siguiente_paso = np.array([[n_historicos]])
        prediccion = self.modelo.predict(siguiente_paso)
        return max(0, int(round(prediccion)))

class GestionInventario:
    """Clase principal que integra la lógica de negocio, Pandas y predicciones."""
    def __init__(self):
        self.productos = {}
        self.historial_ventas = [] # Lista de diccionarios para Pandas
        self.predictor = PredictorVentas()

    def registrar_producto(self, id_prod, nombre, precio, stock):
        if id_prod in self.productos:
            print(f"Error: El ID {id_prod} ya existe.")
            return
        self.productos[id_prod] = Producto(id_prod, nombre, precio, stock)
        print(f"Producto '{nombre}' registrado.")

    def registrar_venta(self, id_prod, cantidad):
        if id_prod not in self.productos:
            print("Error: Producto no encontrado.")
            return
        
        prod = self.productos[id_prod]
        if prod.stock >= cantidad:
            prod.stock -= cantidad
            # Guardamos datos para análisis posterior [1]
            venta = {
                'fecha': datetime.date.today(),
                'id_prod': id_prod,
                'nombre': prod.nombre,
                'cantidad': cantidad,
                'monto_total': cantidad * prod.precio
            }
            self.historial_ventas.append(venta)
            print(f"Venta registrada: {prod.nombre} x{cantidad}.")
        else:
            print(f"Error: Stock insuficiente. Disponible: {prod.stock}")

    def analizar_datos(self):
        """Usa Pandas para mostrar estadísticas de ventas [2, 3]."""
        if not self.historial_ventas:
            print("No hay datos históricos suficientes.")
            return
        
        df = pd.DataFrame(self.historial_ventas)
        print("\n--- RESUMEN DE VENTAS HISTÓRICAS ---")
        print(df.describe())
        print("\n--- TOTALES POR PRODUCTO ---")
        print(df.groupby('nombre')['monto_total'].sum())

    def ejecutar_prediccion(self, id_prod):
        """Integra Pandas y Scikit-learn para predecir stock y ganancias [4, 5]."""
        if id_prod not in self.productos:
            print("Error: Producto no existe.")
            return

        df_completo = pd.DataFrame(self.historial_ventas)
        df_prod = df_completo[df_completo['id_prod'] == id_prod]
        
        exito, msj = self.predictor.entrenar(df_prod)
        print(msj)
        
        if exito:
            pred_cant = self.predictor.predecir_siguiente(len(df_prod))
            prod = self.productos[id_prod]
            ganancia_est = pred_cant * prod.precio
            
            print(f"\n--- RECOMENDACIÓN PARA {prod.nombre} ---")
            print(f"Ventas estimadas próximo periodo: {pred_cant} unidades")
            print(f"Ganancia esperada: ${ganancia_est:.2f}")
            print(f"Stock recomendado (incluyendo margen 20%): {int(pred_cant * 1.2)}")
            print(f"Diferencia a reponer: {max(0, int(pred_cant * 1.2) - prod.stock)}")

    def ver_metricas(self):
        if self.predictor.entrenado:
            print(f"\nMétricas del Modelo (ML):")
            print(f"R² Score: {self.predictor.metricas['r2']:.4f}")
            print(f"Error Cuadrático Medio: {self.predictor.metricas['mse']:.4f}")
        else:
            print("El modelo aún no ha sido entrenado.")

# --- INTERFAZ DE MENÚ ---
def menu():
    sistema = GestionInventario()
    
    while True:
        print("\n--- SISTEMA DE GESTIÓN INTELIGENTE (POO + IA) ---")
        print("1. Registrar nuevo producto")
        print("2. Registrar venta")
        print("3. Analizar histórico (Pandas)")
        print("4. Predecir ventas futuras y stock")
        print("5. Ver métricas del modelo")
        print("6. Ver todos los productos")
        print("7. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            try:
                id_p = int(input("ID único: "))
                nom = input("Nombre: ")
                pre = float(input("Precio: "))
                stk = int(input("Stock inicial: "))
                sistema.registrar_producto(id_p, nom, pre, stk)
            except ValueError: print("Error: Ingrese valores numéricos válidos.")
            
        elif opcion == "2":
            try:
                id_p = int(input("ID del producto: "))
                cant = int(input("Cantidad vendida: "))
                sistema.registrar_venta(id_p, cant)
            except ValueError: print("Error: Entrada inválida.")
            
        elif opcion == "3":
            sistema.analizar_datos()
            
        elif opcion == "4":
            try:
                id_p = int(input("ID del producto para predecir: "))
                sistema.ejecutar_prediccion(id_p)
            except ValueError: print("Error: Ingrese un ID válido.")
            
        elif opcion == "5":
            sistema.ver_metricas()
            
        elif opcion == "6":
            for p in sistema.productos.values(): print(p)
            
        elif opcion == "7":
            print("Cerrando sistema...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()