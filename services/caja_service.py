import json
import os
from datetime import datetime

from dao.caja_dao import CajaDAO
from modelo.movimiento_caja_vo import MovimientoCajaVO


class CajaService:
    ESTADO_PATH = os.path.join("data", "estado_caja.json")

    def __init__(self):
        self.dao = CajaDAO()
        os.makedirs("data", exist_ok=True)

    def _default_state(self):
        return {
            "abierta": False,
            "saldo": 0.0,
            "monto_apertura": 0.0,
            "monto_cierre": 0.0,
            "id_caja": None,
            "id_empleado": None,
            "movimientos": [],
        }

    def obtener_estado(self):
        if not os.path.exists(self.ESTADO_PATH):
            return self._default_state()
        with open(self.ESTADO_PATH, "r", encoding="utf-8") as file_obj:
            estado = json.load(file_obj)
        estado_base = self._default_state()
        estado_base.update(estado)
        return estado_base

    def _guardar_estado(self, estado):
        with open(self.ESTADO_PATH, "w", encoding="utf-8") as file_obj:
            json.dump(estado, file_obj, indent=2, ensure_ascii=False)

    def abrir_caja(self, monto, id_empleado=None):
        monto = float(monto)
        if monto < 0:
            raise ValueError("El monto de apertura no puede ser negativo")

        estado = self.obtener_estado()
        if estado["abierta"]:
            raise ValueError("La caja ya esta abierta")

        caja_id = None
        try:
            caja_id = self.dao.crear_apertura(monto, id_empleado)
        except Exception:
            caja_id = None

        estado = self._default_state()
        estado.update(
            {
                "abierta": True,
                "saldo": monto,
                "monto_apertura": monto,
                "monto_cierre": 0.0,
                "id_caja": caja_id,
                "id_empleado": id_empleado,
            }
        )
        self._guardar_estado(estado)
        return estado

    def _registrar_movimiento(self, tipo, monto, descripcion):
        estado = self.obtener_estado()
        if not estado["abierta"]:
            raise ValueError("La caja debe estar abierta")

        monto = float(monto)
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        if tipo in ("retiro", "gasto") and monto > estado["saldo"]:
            raise ValueError("El monto no puede ser mayor al saldo disponible de la caja")

        movimiento = MovimientoCajaVO(tipo, monto, descripcion, datetime.now())
        signo = 1 if tipo in ("apertura", "ingreso", "venta") else -1
        estado["saldo"] += signo * movimiento.monto
        estado["movimientos"].append(
            {
                "tipo": movimiento.tipo,
                "monto": movimiento.monto,
                "descripcion": movimiento.descripcion,
                "fecha": movimiento.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        self._guardar_estado(estado)
        return movimiento

    def registrar_ingreso(self, monto, motivo):
        return self._registrar_movimiento("ingreso", monto, motivo)

    def registrar_retiro(self, monto, motivo):
        return self._registrar_movimiento("retiro", monto, motivo)

    def registrar_gasto(self, monto, motivo):
        estado = self.obtener_estado()
        movimiento = self._registrar_movimiento("gasto", monto, motivo)
        try:
            self.dao.registrar_gasto(
                descripcion=motivo,
                monto=float(monto),
                id_empleado=estado.get("id_empleado"),
                id_caja=estado.get("id_caja"),
            )
        except Exception:
            pass
        return movimiento

    def registrar_venta(self, total, descripcion):
        return self._registrar_movimiento("venta", total, descripcion)

    def cerrar_caja(self, monto_real):
        estado = self.obtener_estado()
        if not estado["abierta"]:
            raise ValueError("No hay una caja abierta")

        monto_real = float(monto_real)
        if monto_real < 0:
            raise ValueError("El monto de cierre no puede ser negativo")

        extraccion = sum(
            mov["monto"] for mov in estado["movimientos"] if mov["tipo"] in ("retiro", "gasto")
        )
        if estado.get("id_caja"):
            try:
                self.dao.actualizar_cierre(estado["id_caja"], monto_real, extraccion)
            except Exception:
                pass

        resumen = {
            "saldo_sistema": estado["saldo"],
            "monto_real": monto_real,
            "diferencia": monto_real - estado["saldo"],
            "movimientos": estado["movimientos"],
        }
        estado_cerrado = {
            "abierta": False,
            "saldo": monto_real,
            "monto_apertura": estado["monto_apertura"],
            "monto_cierre": monto_real,
            "id_caja": estado.get("id_caja"),
            "id_empleado": estado.get("id_empleado"),
            "movimientos": estado["movimientos"],
        }
        self._guardar_estado(estado_cerrado)
        return resumen
