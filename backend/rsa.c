#include <math.h>

#include "rsa.h"

/* Funções auxiliares */

// Questão 1 da lista de exercícios
bool e_primo(llint num) {
  llint limite, i;

  if (num <= 1) {
    return false;
  }

  if (num != 2 && num % 2 == 0) {
    return false;
  }

  limite = (llint)ceil(sqrt((double)num));
  for (i = 3; i <= limite; i += 2) {
    if (num % i == 0) {
      return false;
    }
  }

  return true;
}

// Questão 5 da lista de exercícios
llint algoritmo_euclides(llint a, llint b) {
  llint aux;

  while (b != 0) {
    aux = b;
    b = a % b;
    a = aux;
  }

  return a;
}

// https://en.wikipedia.org/wiki/Modular_exponentiation#Pseudocode
llint exponenciacao_modular(llint base, llint exp, llint mod) {
  llint resultado;

  if (mod == 1) {
    return 0;
  }

  resultado = 1;
  base = base % mod;

  while (exp > 0) {
    if (exp % 2 != 0) {
      resultado = (resultado * base) % mod;
    }

    exp >>= 1;
    base = (base * base) % mod;
  }

  return resultado;
}

// https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Example
llint calcular_inverso_modular(llint a, llint m) {
  llint s, s2, m0, aux;

  m0 = m;
  s = 1;
  s2 = 0;

  while (m != 0) {
    aux = s2;
    s2 = s - (a / m) * aux;
    s = aux;

    aux = m;
    m = a % m;
    a = aux;
  }

  if (s < 0) {
    s += m0;
  }

  return s;
}

/*
 * Funções do RSA
 * p e q são primos que formam a chave privada
 * e é expoente relativamente primo a (p - 1) * (q - 1)
 * n é chave pública
 * d é inverso modular de e mod (p - 1) * (q - 1)
 */

// Zero não é primo e indica entrada inválida
llint gerar_chave_publica(llint p, llint q, llint e) {
  if (!e_primo(p) || !e_primo(q)) {
    return 0;
  }

  if (algoritmo_euclides(e, (p - 1) * (q - 1)) != 1) {
    return 0;
  }

  return p * q;
}

void encriptar(const char *msg, size_t tamanho_msg, llint n, llint e, llint msg_cripto[]) {
  size_t i;

  for (i = 0; i < tamanho_msg; i++) {
    msg_cripto[i] = exponenciacao_modular(msg[i], e, n);
  }
}

void desencriptar(const llint msg_cripto[], size_t tamanho_msg, llint p, llint q, llint e, char *msg) {
  llint d, n;
  size_t i;

  d = calcular_inverso_modular(e, (p - 1) * (q - 1));
  n = p * q;

  for (i = 0; i < tamanho_msg; i++) {
    msg[i] = (char)exponenciacao_modular(msg_cripto[i], d, n);
  }
}
