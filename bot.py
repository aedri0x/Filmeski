import os
import random
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# 1. Configuração do Servidor Web (Flask)
app = Flask('')

@app.route('/')
def home():
    return "Servidor Web do Bot Ativo!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Configuração do Bot do Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ALTERAÇÃO NECESSÁRIA: Insira o ID numérico do canal
CANAL_FILMES_ID = 1419867980980027523  

@bot.event
async def on_ready():
    print(f"Bot conectado com sucesso como {bot.user}")

@bot.command(name="filme")
async def sortear_filme(ctx):
    canal = bot.get_channel(CANAL_FILMES_ID)

    if not canal:
        await ctx.send("Erro: Não foi possível encontrar o canal especificado.")
        return

    async with ctx.typing():
        mensagens_validas = []

        async for msg in canal.history(limit=200):
            if msg.content.strip() and not msg.author.bot:
                
                # Verifica se a mensagem já possui a reação 🍿
                ja_assistido = any(str(reaction.emoji) == '🍿' for reaction in msg.reactions)
                
                if not ja_assistido:
                    mensagens_validas.append(msg)

        if not mensagens_validas:
            await ctx.send("Nenhum filme disponível. Todos os itens no histórico recente já possuem a reação 🍿.")
            return

        mensagem_sorteada = random.choice(mensagens_validas)
        
        # Adiciona o emoji de pipoca à mensagem sorteada no histórico
        await mensagem_sorteada.add_reaction('🍿')

        resposta = (
            f"🎬 **Filme sorteado:** {mensagem_sorteada.content}\n"
            f"*(Sugerido por <@{mensagem_sorteada.author.id}> em {mensagem_sorteada.created_at.strftime('%d/%m/%Y')})*"
        )

        await ctx.send(resposta)

# 3. Execução
keep_alive()

try:
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise ValueError("Token não encontrado nas Variáveis de Ambiente.")
    bot.run(token)
except discord.errors.LoginFailure:
    print("MTU0MTY5ODEwMzgwMjA2OTAxMg.GKtD0d.chkzSNJ6X3m8iPSDHWD3G_wceYttJ-wa8N3ssw")
