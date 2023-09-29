#pragma once
#include <stdbool.h>
#include <stddef.h>

typedef long long llint;

llint gerar_chave_publica(llint p, llint q, llint e);
void encriptar(const char *msg, size_t tamanho_msg, llint n, llint e, llint msg_cripto[]);
void desencriptar(const llint msg_cripto[], size_t tamanho_msg, llint p, llint q, llint e, char *msg);

bool e_primo(llint num);
llint algoritmo_euclides(llint a, llint b);
llint exponenciacao_modular(llint base, llint exp, llint mod);
llint calcular_inverso_modular(llint a, llint m);
