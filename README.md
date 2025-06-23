# 🎮 Campo Minado - Jogo com Bombas Falsas

Um jogo de Campo Minado implementado em Flask com funcionalidades especiais de bombas falsas e sistema de pontuação.

## ✨ Funcionalidades Implementadas

### 🎯 Sistema de Cache
- **Persistência de Estado**: O jogo mantém o estado mesmo após recarregar a página
- **Sessões Únicas**: Cada jogador tem sua própria sessão de jogo
- **Cache com Flask-Caching**: Estado do jogo armazenado em cache por 1 hora

### 💣 Sistema de Bombas Falsas
- **Bombas Falsas (⭐)**: 5 bombas especiais que não terminam o jogo
- **Células Vizinhas Vermelhas**: Números em vermelho ao redor das bombas falsas
- **Som Especial**: Áudio reproduzido ao encontrar bombas falsas

### 🏆 Sistema de Pontuação
- **Contagem de Bombas Falsas**: Registro no banco de dados
- **Estatísticas**: Página dedicada para visualizar pontuações
- **Histórico**: Últimos 10 jogos salvos

### 🎨 Interface Melhorada
- **Contadores Visuais**: Bombas, bandeiras, bombas falsas, tempo e pontuação
- **Cores Especiais**: Números vermelhos para células vizinhas de bombas falsas
- **Design Responsivo**: Interface moderna e intuitiva

## 🚀 Como Executar

### Pré-requisitos
```bash
pip install flask flask-sqlalchemy flask-caching
```

### Executar o Jogo
```bash
python app.py
```

Acesse `http://localhost:5000` no seu navegador.

## 🎮 Como Jogar

1. **Clique Esquerdo**: Revela uma célula
2. **Clique Direito**: Coloca/remove uma bandeira
3. **Bombas Falsas (⭐)**: Dão pontos e não terminam o jogo
4. **Bombas Reais (💣)**: Terminam o jogo
5. **Números Vermelhos**: Indicam proximidade com bombas falsas

## 📊 Estrutura do Projeto

```
Trabalho A4/
├── app.py                 # Aplicação Flask principal
├── controller/
│   └── FieldController.py # Controlador do campo
├── model/
│   ├── Cell.py           # Modelo de célula
│   └── MineField.py      # Modelo do campo minado
├── service/
│   └── GameService.py    # Lógica de negócio
├── static/
│   └── css/
│       └── main.css      # Estilos CSS
├── templates/
    ├── index.html        # Template principal
    └── score.html        # Template de pontuações

```

## 🗄️ Banco de Dados

### Modelo Game
- `id`: ID único do jogo
- `fakeBombsFound`: Bombas falsas encontradas
- `timeInSeconds`: Tempo do jogo em segundos

### Ordenação dos Registros
Os registros são ordenados por:
1. **Tempo de jogo (crescente)** - Jogos mais rápidos primeiro
2. **Bombas falsas encontradas (decrescente)** - Mais bombas falsas primeiro

## 🔧 Configurações

### Cache
- **Tipo**: Simple Cache (memória)
- **Timeout**: 1 hora
- **Chave**: `game_state_{session_id}`

### Campo de Jogo
- **Tamanho**: 10x10 células
- **Bombas Reais**: 15
- **Bombas Falsas**: 5
- **Total**: 20 bombas

## 🎯 Funcionalidades Técnicas

### Serialização de Estado
- Conversão de objetos MineField para dicionários
- Cache de estado serializado
- Restauração de estado ao recarregar

### Sistema de Sessões
- IDs únicos por sessão
- Persistência de dados por usuário
- Isolamento de jogos

### API REST
- `/`: Página principal
- `/score`: Estatísticas
- `/reveal`: Revelar célula
- `/flag`: Colocar bandeira
- `/restart`: Reiniciar jogo
- `/end_game`: Salvar resultado

## 🎨 Estilos CSS

### Classes Especiais
- `.fake-bomb-neighbor`: Células vizinhas de bombas falsas
- `.revealed`: Células reveladas
- `.flagged`: Células com bandeira

## 🔄 Fluxo do Jogo

1. **Início**: Criação de novo campo ou restauração do cache
2. **Jogada**: Clique para revelar célula
3. **Bomba Falsa**: Adiciona pontos e marca vizinhas
4. **Bomba Real**: Termina jogo e salva estatísticas
5. **Reinício**: Limpa cache e cria novo campo