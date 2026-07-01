"""
Propósito: recortar excessos inferiores baseado na cor RGB (242, 242, 242)
Autor: Alexandre Nassar de Peder
Criação: 03/06/2026
"""
from PIL import Image
import os
import shutil

def cortar_imagem(imagem, cor_alvo=(242, 242, 242), tolerancia=10):
    """
    Procura a cor alvo de baixo para cima e corta 10 pixels abaixo
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    # Pega a coluna do meio para verificação
    x_meio = largura // 2
    
    # Percorre de baixo para cima
    for y in range(altura - 1, -1, -1):
        pixel = pixels[x_meio, y]
        
        # Pega apenas RGB (ignora alpha)
        if len(pixel) == 4:  # RGBA
            r, g, b, a = pixel
        else:  # RGB
            r, g, b = pixel[:3]
        
        # Verifica se a cor é igual à cor alvo (com tolerância)
        if (abs(r - cor_alvo[0]) <= tolerancia and 
            abs(g - cor_alvo[1]) <= tolerancia and 
            abs(b - cor_alvo[2]) <= tolerancia):
            
            # Encontrou a cor alvo, corta 10 pixels abaixo
            posicao_corte = y + 10
            
            # Garante que não ultrapassa a altura
            if posicao_corte > altura:
                posicao_corte = altura
            
            # Recorta a imagem
            area_corte = (0, 0, largura, posicao_corte)
            imagem_cortada = imagem.crop(area_corte)
            
            print(f"  ✓ Cor encontrada em y={y}, cortando em y={posicao_corte}")
            return imagem_cortada
    
    # Se não encontrou a cor, retorna a imagem original
    print(f"  ⚠️ Cor não encontrada, mantendo original")
    return imagem

def processar_pasta(pasta_origem, pasta_destino):
    """
    Processa todas as imagens da pasta
    """
    # Cria pasta de destino
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Lista arquivos de imagem
    arquivos = [f for f in os.listdir(pasta_origem) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    
    print(f"Encontrados {len(arquivos)} arquivos")
    print("-" * 50)
    
    for arquivo in arquivos:
        caminho_origem = os.path.join(pasta_origem, arquivo)
        caminho_destino = os.path.join(pasta_destino, arquivo)
        
        try:
            print(f"\n📄 {arquivo}")
            
            # Abre a imagem
            with Image.open(caminho_origem) as imagem:
                # Aplica o corte
                imagem_final = cortar_imagem(imagem)
                
                # Salva
                imagem_final.save(caminho_destino)
                print(f"  ✅ Salvo: {imagem_final.width}x{imagem_final.height}")
                
        except Exception as e:
            print(f"  ❌ Erro: {e}")
            # Copia o arquivo original em caso de erro
            shutil.copy2(caminho_origem, caminho_destino)
            print(f"  ⚠️ Copiado original (com erro)")

# Execução principal
if __name__ == "__main__":
    pasta_origem = "./1-90"
    pasta_destino = "finalizadas"
    
    print("="*50)
    print("RECORTADOR DE EXCESSOS")
    print("="*50)
    print(f"Cor alvo: RGB (242, 242, 242)")
    print(f"Pasta origem: {pasta_origem}")
    print(f"Pasta destino: {pasta_destino}")
    print("="*50)
    
    # Verifica se a pasta existe
    if not os.path.exists(pasta_origem):
        print(f"ERRO: Pasta '{pasta_origem}' não encontrada!")
        exit(1)
    
    # Processa
    processar_pasta(pasta_origem, pasta_destino)
    
    print("\n" + "="*50)
    print("✅ PROCESSAMENTO CONCLUÍDO!")
    print(f"📁 Imagens salvas em: {pasta_destino}")