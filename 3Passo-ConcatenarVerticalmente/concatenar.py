from PIL import Image
import os
import re

pasta_imagens = "sem-bordas-externas"
pasta_saida = "concatenada"
os.makedirs(pasta_saida, exist_ok=True)

def get_sort_key(nome_arquivo):
    numero = int(re.search(r'pagina_enem_(\d+)', nome_arquivo).group(1))
    return numero

arquivos = [f for f in os.listdir(pasta_imagens) if f.endswith('.png')]
arquivos.sort(key=get_sort_key)

imagens = []
for arquivo in arquivos:
    caminho = os.path.join(pasta_imagens, arquivo)
    imagens.append(Image.open(caminho))
    print(f"Adicionando: {arquivo}")

largura_max = max(img.width for img in imagens)
altura_total = sum(img.height for img in imagens)
imagem_final = Image.new('RGB', (largura_max, altura_total))

y = 0
for img in imagens:
    imagem_final.paste(img, (0, y))
    y += img.height

imagem_final.save(os.path.join(pasta_saida, 'colunas_concatenadas_verticalmente.png'))
print("Imagens concatenadas na ordem correta!")
print(f"Ordem dos arquivos: {arquivos}")