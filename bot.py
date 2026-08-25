import random
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ALTERAÇÃO 1: Substitua o número abaixo pelo ID do canal copiado no Passo 2A.
# Mantenha o número sem aspas.
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
                mensagens_validas.append(msg)

        if not mensagens_validas:
            await ctx.send("Nenhum filme encontrado no histórico.")
            return

        mensagem_sorteada = random.choice(mensagens_validas)
        resposta = (
            f"🎬 **Filme sorteado:** {mensagem_sorteada.content}\n"
            f"*(Sugerido por <@{mensagem_sorteada.author.id}> em {mensagem_sorteada.created_at.strftime('%d/%m/%Y')})*"
        )

        await ctx.send(resposta)


# ALTERAÇÃO 2: Substitua o texto "SEU_TOKEN_AQUI" pelo Token copiado no Passo 2B.
# Mantenha as aspas ao redor do token.
bot.run("MTU0MTY5ODEwMzgwMjA2OTAxMg.GKtD0d.chkzSNJ6X3m8iPSDHWD3G_wceYttJ-wa8N3ssw")