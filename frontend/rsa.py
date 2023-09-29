import os
import typing
from ctypes import CDLL, POINTER, c_char_p
from ctypes import c_longlong as llint
from ctypes import c_size_t, create_string_buffer


def _encontrar_biblioteca() -> str:
    extensao = "dll" if os.name == "nt" else "so"
    return os.path.join(os.path.dirname(__file__), "../bin/rsa." + extensao)


def gerar_chave_publica(p: int, q: int, e: int) -> int:
    return typing.cast(int, _gerar_chave_publica(p, q, e))


def encriptar(msg: bytes, n: int, e: int) -> tuple[int, ...]:
    msg_cripto = (llint * len(msg))()
    _encriptar(msg, len(msg), n, e, msg_cripto)
    return tuple(msg_cripto)


def desencriptar(msg_cripto: list[int], p: int, q: int, e: int) -> bytes:
    tipo_array = llint * len(msg_cripto)
    msg = create_string_buffer(len(msg_cripto))
    _desencriptar(tipo_array(*msg_cripto), len(msg), p, q, e, msg)
    return msg.value


_biblioteca = CDLL(_encontrar_biblioteca())
_ponteiro_llint = POINTER(llint)

_gerar_chave_publica = _biblioteca.gerar_chave_publica
_gerar_chave_publica.argtypes = llint, llint, llint
_gerar_chave_publica.restype = llint

_encriptar = _biblioteca.encriptar
_encriptar.argtypes = c_char_p, c_size_t, llint, llint, _ponteiro_llint
_encriptar.restype = None

_desencriptar = _biblioteca.desencriptar
_desencriptar.argtypes = _ponteiro_llint, c_size_t, llint, llint, llint, c_char_p
_desencriptar.restype = None
