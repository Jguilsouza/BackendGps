import struct

def hex_ieee754_to_decimal(hex_string):
    # Converte a representação hexadecimal em bytes
    hex_bytes = bytes.fromhex(hex_string)

    # Verifica se a entrada tem o tamanho correto (4 bytes)
    if len(hex_bytes) != 4:
        raise ValueError("A entrada deve ter 4 bytes")

    # Usa a função struct.unpack() para interpretar os bytes como um número de ponto flutuante de precisão simples
    decimal_value = struct.unpack('>f', hex_bytes)[0]

    return decimal_value

# Exemplo de uso:
hex_value = "c1a196a2"  # Exemplo com 4 bytes
decimal_value = hex_ieee754_to_decimal(hex_value)
print(decimal_value)