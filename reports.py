import disnake
from disnake.ext import commands

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

class RecruitementModal(disnake.ui.Modal):
    def __init__(self, arg):
        self.arg = arg  # arg - это аргумент, который передается в конструкторе класса RecruitementSelect
        """
        Также можно сделать так:
        components = [
            disnake.ui.TextInput(label="Ваше имя", placeholder="Введите ваше имя", custom_id="name"),
            disnake.ui.TextInput(label="Ваш возраст", placeholder="Введите ваш возраст", custom_id="age")
            disnake.ui.TextInput(
                label="Расскажите о себе и почему именно вы?",
                placeholder="Расскажи о себе здесь",
                custom_id="info",
                style=disnake.TextInputStyle.paragraph,
                min_length=10,
                max_length=500,
            )
        ]
        """
        components = [
            disnake.ui.TextInput(label="Ваш ник", placeholder="Введите ваш ник", custom_id="name"),
            disnake.ui.TextInput(label="Введите нарушение", placeholder="Введите нарушение и ник нарушителя", custom_id="age")
        ]
        if self.arg == "moderator":
            title = "Жалоба на игрока"
        else:
            title = "Расскажите нам о себе"
        super().__init__(title=title, components=components, custom_id="recruitementModal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        name = interaction.text_values["name"]
        age = interaction.text_values["age"]
        embed = disnake.Embed(color=0x2F3136, title="Жалоба отправлена!")
        embed.description = f"{interaction.author.mention}, Благодарим вас за **жалобу**! "
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        channel = interaction.guild.get_channel(1118864908822511767)  # Вставить ID канала куда будут отправляться заявки
        await channel.send(f"Жалоба от {name} {interaction.author.mention} ({age})")


class RecruitementSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Жалоба", value="moderator", description="Жалоба"),
        ]
        super().__init__(
            placeholder="Выберите отчет", options=options, min_values=0, max_values=1, custom_id="recruitement"
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        if not interaction.values:
            await interaction.response.defer()
        else:
            await interaction.response.send_modal(RecruitementModal(interaction.values[0]))


class Recruitement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    @commands.command(name="report")
    async def report(self, ctx):
        if ctx.channel.id != 1117889039840858182:
            return await ctx.send("This command can only be used in the specified channel.")

        view = disnake.ui.View()
        view.add_item(RecruitementSelect())
        # Тут можно добавить эмбед с описанием ролей
        await ctx.send('Выберите отчет', view=view)

    @commands.Cog.listener()
    async def on_connect(self):
        if self.persistents_views_added:
            return

        view = disnake.ui.View(timeout=None)
        view.add_item(RecruitementSelect())
        self.bot.add_view(view, message_id=1119140949336018964)  # Вставить ID сообщения, которое отправится после использования с командой /report

bot.add_cog(Recruitement(bot))

bot.run("MTExODg2MDE3Njk0NzE1MDkyMA.GOYQ20.Kn3XaRSAKl3gBtwGLA_lu63TFAOVSM2A-t_q94")