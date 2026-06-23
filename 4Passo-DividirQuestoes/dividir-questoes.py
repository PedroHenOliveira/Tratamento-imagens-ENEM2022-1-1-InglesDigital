"""
Propósito: Dividir as questões por padrão de faixa cinza RGB (220, 220, 220)
Corte: EXATAMENTE no início da faixa divisória (sem margens adicionais)
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026
"""

from PIL import Image
import os

# ===== SOLUÇÃO PARA O ERRO DE LIMITE DE PIXELS =====
Image.MAX_IMAGE_PIXELS = None  # Remove o limite máximo de pixels

def encontrar_faixa_separadora(imagem, cor_alvo=(220, 220, 220), tolerancia=20, altura_faixa=156):
    """
    Encontra posições onde há uma faixa horizontal da cor especificada
    A faixa padrão é RGB (220, 220, 220) com 156 pixels de altura
    
    Args:
        imagem: Objeto PIL Image
        cor_alvo: Tupla RGB da cor da faixa (padrão: 220, 220, 220)
        tolerancia: Tolerância para variação de cor (padrão: 20)
        altura_faixa: Altura da faixa em pixels (padrão: 156)
    
    Returns:
        Lista de posições y onde as faixas começam
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_faixas = []  # Posição onde a faixa COMEÇA (y inicial)
    
    # Percorre a imagem de cima para baixo
    y = 0
    while y < altura - altura_faixa:
        # Verifica se há uma faixa de 'altura_faixa' pixels da cor alvo
        faixa_encontrada = True
        
        # Verifica em múltiplos pontos na horizontal para maior precisão
        pontos_verificacao = [
            largura // 4,   # 25% da largura
            largura // 2,   # 50% da largura (meio)
            3 * largura // 4 # 75% da largura
        ]
        
        for dy in range(altura_faixa):
            linha_valida = False
            
            # Verifica em vários pontos da linha
            for x in pontos_verificacao:
                if x >= largura:
                    continue
                    
                pixel = pixels[x, y + dy]
                
                if len(pixel) == 4:  # RGBA
                    r, g, b, a = pixel
                else:  # RGB
                    r, g, b = pixel[:3]
                
                # Verifica se a cor está dentro da tolerância
                if (abs(r - cor_alvo[0]) <= tolerancia and 
                    abs(g - cor_alvo[1]) <= tolerancia and 
                    abs(b - cor_alvo[2]) <= tolerancia):
                    linha_valida = True
                    break
            
            if not linha_valida:
                faixa_encontrada = False
                break
        
        if faixa_encontrada:
            # Guarda a posição onde a faixa COMEÇA (y inicial)
            posicoes_faixas.append(y)
            print(f"Faixa separadora encontrada começando em y={y}")
            
            # Pula a faixa inteira para evitar detecções múltiplas
            y += altura_faixa
        else:
            y += 1
    
    return posicoes_faixas

def dividir_questoes(caminho_imagem, pasta_saida, cor_alvo=(220, 220, 220)):
    """
    Divide a imagem em questões individuais cortando EXATAMENTE no início das faixas cinzas
    A faixa pertence à questão anterior
    
    Args:
        caminho_imagem: Caminho da imagem de entrada
        pasta_saida: Pasta onde salvar as questões
        cor_alvo: Cor da faixa em RGB (padrão: 220, 220, 220)
    """
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_imagem):
        print(f"ERRO: Arquivo não encontrado: {caminho_imagem}")
        return
    
    # Abre a imagem
    try:
        imagem = Image.open(caminho_imagem)
        largura, altura = imagem.size
        print(f"Imagem carregada: {largura}x{altura} pixels")
    except Exception as e:
        print(f"ERRO ao carregar imagem: {e}")
        return
    
    # Encontra as posições onde as faixas começam
    posicoes_faixas = encontrar_faixa_separadora(imagem, cor_alvo)
    
    if not posicoes_faixas:
        print("Nenhuma faixa separadora encontrada na imagem!")
        print("Verifique se a imagem contém faixas RGB (220, 220, 220)")
        return
    
    print(f"\nEncontradas {len(posicoes_faixas)} faixas separadoras")
    print("Posições das faixas (y inicial):", posicoes_faixas)
    
    # Cria a pasta de saída se não existir
    os.makedirs(pasta_saida, exist_ok=True)
    
    # ===== CORTE EXATO NO INÍCIO DA FAIXA =====
    # A faixa pertence à questão anterior (corte em cima da faixa)
    
    posicao_anterior = 0
    
    for i, posicao_faixa in enumerate(posicoes_faixas):
        # Corta a questão: do início anterior até o COMEÇO da faixa
        # SEM margens adicionais - corte exato
        area_corte = (0, posicao_anterior, largura, posicao_faixa)
        questao = imagem.crop(area_corte)
        
        # Salva a questão
        nome_arquivo = f"questao_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        questao.save(caminho_completo)
        print(f"✅ Salvo: {nome_arquivo} ({questao.width}x{questao.height}px)")
        print(f"   Corte: y={posicao_anterior} até y={posicao_faixa} (exato)")
        
        # A próxima questão começa EXATAMENTE no início da faixa
        posicao_anterior = posicao_faixa
    
    # Corta a questão final (após a última faixa até o final)
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        questao = imagem.crop(area_corte)
        
        nome_arquivo = f"questao_{len(posicoes_faixas)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        questao.save(caminho_completo)
        print(f"✅ Salvo: {nome_arquivo} ({questao.width}x{questao.height}px)")
        print(f"   Corte: y={posicao_anterior} até y={altura} (final)")
    
    print(f"\n{'='*60}")
    print(f"✅ DIVISÃO CONCLUÍDA!")
    print(f"📁 Total: {len(posicoes_faixas)+1} questões salvas em '{pasta_saida}'")
    print(f"{'='*60}")

def main():
    """
    Função principal - Configure aqui os parâmetros
    """
    
    # ===== CONFIGURAÇÕES =====
    
    # COR DA FAIXA SEPARADORA (RGB)
    # Padrão: (220, 220, 220) - Cinza claro
    cor_faixa = (220, 220, 220)
    
    # ALTURA DA FAIXA em pixels
    altura_faixa = 156
    
    # TOLERÂNCIA para detecção da cor
    tolerancia = 20
    
    # ===== PROCESSAR COLUNAS CONCATENADAS =====
    caminho_imagem = "colunas_concatenadas_58-104.png"
    pasta_saida = "questoes_colunas2"
    
    # ===== PROCESSAR PÁGINAS INDIVIDUAIS =====
    # Para processar a página que você enviou:
    #caminho_imagem = "pagina_enem_7.png"
    #pasta_saida = "questoes_pagina_7"
    
    # ===== EXECUTAR =====
    print("="*60)
    print("DIVISOR DE QUESTÕES DO ENEM")
    print("="*60)
    print(f"📐 Cor da faixa: RGB{cor_faixa}")
    print(f"📏 Altura da faixa: {altura_faixa} pixels")
    print(f"🎯 Tolerância: {tolerancia}")
    print(f"📂 Imagem: {caminho_imagem}")
    print(f"📁 Pasta de saída: {pasta_saida}")
    print("="*60)
    print()
    
    dividir_questoes(caminho_imagem, pasta_saida, cor_faixa)

if __name__ == "__main__":
    main()