# TODO : plugins
#   a réorganiser en plugins/<nom plugins>/main.py et default_conf
#   revoir fonctionnement core.py

import asyncio
import logging
import os.path
import traceback

import discord
from discord.ext import commands


class ECogsManagedException(Exception):
    pass


class CogCore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.log = bot.log

    async def ask_for_user(self, ctx, title="", not_me=True, contains=""):
        """
        Questionne l'utilisateur et vérifie qu'il s'agisse d'un joueur
        :param ctx: context
        :param title: titre du message
        :param contains: string must be included in the nickname (optional)
        :param not_me: interdit que l'utilisateur soit le demandeur
        :return:
        """

        msg_to_remove = []

        mention = ctx.message.author.mention

        users = ctx.message.server.members

        if title != "":
            title = "**{0}**\n".format(title)

        msg_begin = (
            title + "{0}\nOk ! Commençons par trouver l'utilisateur :thinking: "
            "\nPeux-tu me donner au moins une partie de son pseudo (3 caractères minimum) ?"
            "\nQ pour quitter sinon..."
        )

        msg_list = (
            title
            + "{0}\nYo man ! Tu veux voir si tu reconnais quelqu'un dans ma liste de potes ?"
            "\nIl n'y a qu'eux qui ont un nom se rapprochant de ce que tu me donnes :"
            "\nQ pour qu'on arrête là si tu veux..."
        )

        msg_found = (
            title
            + "{0}\n Ah ? c'est lui ou elle dont tu me parles ??? {1}, je connais cette meuf ou ce mec..."
            "\non passe à la suite ?"
        )

        self.log.debug("core.ask_for_user > loop start")

        filtered_users = []
        o_utilisateur = None

        msg = msg_begin.format(mention)

        while True:

            if contains == "":

                curr_msg_id = await self.send_msg(ctx, msg)
                msg_to_remove.append(curr_msg_id)

                response = await self.bot.wait_for_message(
                    author=ctx.message.author, timeout=30
                )

                if response is None:
                    self.log.debug("core.ask_for_user > answer timeout")
                    await self.send_msg(
                        ctx,
                        msg="Tu me fais signe quand tu reviens, on reprendra depuis le début...",
                    )
                    return None

                msg_to_remove.append(response)

                if response.clean_content.lower() == "q":
                    self.log.debug("core.ask_for_user > q for quit")
                    for msgdel in msg_to_remove:
                        await self.bot.delete_message(msgdel)
                    await self.send_msg(ctx, msg="Ok ok on annule tout...")
                    return None

                response = response.clean_content.lower()
            else:
                response = contains.lower()

            contains = ""

            if len(response) > 2:
                self.log.debug("core.ask_for_user > we have an answer (> 3char)")

                filtered_users = []

                for user in users:
                    if response == user.display_name.lower():
                        o_utilisateur = user
                        msg = msg_found.format(mention, user.display_name)
                        self.log.debug(
                            "core.ask_for_user > user found : {0}".format(
                                user.display_name
                            )
                        )
                        break
                    elif response in user.display_name.lower():
                        filtered_users.append(user)
                        self.log.debug(
                            "core.ask_for_user > response in {0}".format(
                                user.display_name
                            )
                        )

                if o_utilisateur is not None:
                    self.log.debug("core.ask_for_user > user found by name > break")
                    if not_me and o_utilisateur.id == ctx.message.author.id:
                        await self.send_msg(ctx, msg="Laisse tomber je t'es reconnu...")
                        msg = msg_begin.format(mention)
                        continue
                    else:
                        break

                self.log.debug("core.ask_for_user > rebuild list filtered user")
                msg = msg_list.format(mention) + "```"
                for index, user in enumerate(filtered_users):
                    msg += "\n\t{0} - {1}".format(str(index), user.display_name)
                msg += "```"

            elif response.isdigit() and len(filtered_users) > 0:
                self.log.debug("core.ask_for_user > we have an answer (digit)")
                try:
                    o_utilisateur = filtered_users[int(response)]
                    self.log.debug("core.ask_for_user > user found by digit > break")
                    break
                except:
                    msg = msg_begin.format(mention)
            else:
                msg = msg_begin.format(mention)

        self.log.debug("core.ask_for_user > end loop")
        resultat = {}
        resultat["user"] = o_utilisateur
        resultat["msg_to_remove"] = msg_to_remove

        return resultat

    async def ask(
        self,
        ctx,
        title,
        content,
        question,
        array_choice,
        choice_by_val_accepted=False,
        in_pm=False,
    ):
        """
        Questionne l'utilisateur et vérifie la réponse
        :param ctx: context
        :param title: titre du message
        :param content: contenu (détail)
        :param question: la question a poser
        :param array_choice: les réponses possibles
        :param choice_by_val_accepted:
        :return: {choice_index: index, msg_to_remove: array} ou None si pas de réponse
        """

        # title = "Sanction par {0}".format(ctx.message.author.display_name)
        # descr = "**- Utilisateur :** {0} \n" \
        #         "**- Sanction :** {1} \n" \
        #         "**- Delai :** {2} \n" \
        #         "**- Motif :** {3} \n" \
        #         "-------------------------\n" \
        #         "(Q pour quitter) \n" \
        #         "{4}"
        #
        # question = "Quel est le type de sanction ?\n" + "\t\n".join(self.langs.keys())

        msg_to_remove = []

        descr = (
            "{0} \n"
            "-------------------- \n"
            "{1} \n"
            "Valeurs possibles : ".format(content, question)
        )

        for key, value in enumerate(array_choice):
            descr += "\n`\t{0} - {1}`".format(key, value)

        descr += "\n`\tQ - Quitter`"

        # envoi initial
        embed = discord.Embed(title=title, description=descr, color=0xFF7E00)

        choice_index = -1
        self.log.debug("core.ask > loop start")

        while True:
            if in_pm:
                await self.send_pm(ctx, embed=embed)
            else:
                msg_to_remove.append(await self.send_msg(ctx, embed=embed))
            response = await self.bot.wait_for_message(
                author=ctx.message.author, timeout=30
            )

            if response is None:
                self.log.debug("core.ask > answer timeout")
                if in_pm:
                    await self.send_pm(
                        ctx,
                        msg="Tu me fais signe quand tu reviens, on reprendra depuis le début..."
                        " too late | слишком поздно | 太晚了",
                    )
                else:
                    await self.send_msg(
                        ctx,
                        msg="Tu me fais signe quand tu reviens, on reprendra depuis le début..."
                        " too late | слишком поздно | 太晚了",
                    )
                return None

            if not in_pm:
                msg_to_remove.append(response)

            if response.clean_content.lower() == "q":
                self.log.debug("core.ask > q for quit")
                for msgdel in msg_to_remove:
                    await self.bot.delete_message(msgdel)
                if in_pm:
                    await self.send_pm(
                        ctx, msg="Ok ok on annule tout...\n" "canceled / отменен / 取消"
                    )
                else:
                    await self.send_msg(
                        ctx, msg="Ok ok on annule tout...\n" "canceled / отменен / 取消"
                    )
                return None

            response = response.clean_content.lower()
            if response != "":
                self.log.debug("core.ask > we have an answer")
                for key, value in enumerate(array_choice):
                    if response == str(key) or (
                        choice_by_val_accepted and response == str(value).lower()
                    ):
                        self.log.debug("core.ask > key matched")
                        choice_index = key

            if choice_index != -1:
                break

            msg_to_remove.append(
                await self.send_msg(
                    ctx, msg="Ca ne fait pas parti des choix possibles..."
                )
            )
            self.log.debug("core.ask > new iteration response : {}".format(response))

        self.log.debug("core.ask > end loop")
        resultat = {}
        resultat["choice_index"] = choice_index
        resultat["msg_to_remove"] = msg_to_remove

        return resultat

    async def send_pm(self, ctx, msg=None, embed=None):
        try:
            # Si option manquant alors Exception
            if msg is None and embed is None:
                raise Exception("manque message ou embed")
            elif embed is not None:
                msg_id = await self.bot.send_message(ctx.message.author, embed=embed)
            else:
                msg_id = await self.bot.send_message(ctx.message.author, msg)

        except discord.Forbidden as f:
            await self.raise_msg(ctx, msg_type="send_pm", is_embed=(embed is None))
            raise
        except Exception as e:
            await self.raise_msg(
                ctx, msg_type="send_pm", is_embed=(embed is None), except_type="inconnu"
            )
            raise
        return msg_id

    async def send_msg(self, ctx, msg=None, embed=None, send_help=False):
        try:
            # Si option manquant alors Exception
            if msg is None and embed is None:
                raise Exception("manque message ou embed")
            elif embed is not None:
                msg_id = await self.bot.send_message(ctx.message.channel, embed=embed)
            else:
                msg_id = await self.bot.send_message(ctx.message.channel, msg)

            # si ajouter l'aide correspondante à la suite
            if send_help:
                await ctx.invoke(
                    self.bot.get_command("help"), *ctx.command.qualified_name.split()
                )
        except discord.Forbidden as f:
            await self.raise_msg(ctx, msg_type="send", is_embed=(embed is None))
            raise
        except Exception as e:
            await self.raise_msg(
                ctx, msg_type="send", is_embed=(embed is None), except_type="inconnu"
            )
            raise
        return msg_id

    async def edit_msg(self, ctx, msg_id, msg=None, embed=None):
        try:
            # Si option manquant alors Exception
            if msg is None and embed is None:
                raise Exception("manque message ou embed")
            elif embed is not None:
                msg_id = await self.bot.edit_message(msg_id, embed=embed)
            else:
                msg_id = await self.bot.edit_message(msg_id, msg)
        except discord.Forbidden as f:
            await self.raise_msg(ctx, msg_type="edit", is_embed=(embed is None))
            raise
        except Exception as e:
            await self.raise_msg(
                ctx, msg_type="edit", is_embed=(embed is None), except_type="inconnu"
            )
            raise
        return msg_id

    async def raise_msg(
        self, ctx, msg_type="send", is_embed=False, except_type="permission"
    ):
        if is_embed:
            is_embed = "embed"
        else:
            is_embed = "msg"

        titre = "{0} '{1}' > {2} `{3}`  = {4} {5} {6}".format(
            ctx.message.server.name,
            ctx.message.channel.name,
            ctx.message.author.display_name,
            ctx.message.clean_content,
            msg_type,
            is_embed,
            except_type,
        )
        trace = traceback.format_exc()

        self.log.error(titre)
        self.log.error(trace)

        try:
            trace = "```" + trace + "```"
            embed = discord.Embed(title=titre, description=trace, color=0xFF0000)

            owners_id = []
            for owner_id in self.bot.cfg["check"]["owners_id"].values():
                owner = ctx.message.server.get_member(owner_id)
                await self.bot.send_message(owner, embed=embed)
                owners_id.append(owner.mention)

            try:
                await self.bot.send_message(
                    ctx.message.channel,
                    "Ya un truc qui cloche... \n"
                    + ", ".join(owners_id)
                    + ": quelqu'un peut m'aider ?",
                )
            except Exception as e:
                self.log.error(traceback.format_exc())
        except Exception as e:
            self.log.error(traceback.format_exc())
        raise ECogsManagedException

    async def raise_pm(self, msg_type="send", is_embed=False, except_type="permission"):
        if is_embed:
            is_embed = "embed"
        else:
            is_embed = "msg"

        titre = "{0} '{1}' {2} ".format(msg_type, is_embed, except_type)
        trace = traceback.format_exc()

        self.log.error(titre)
        self.log.error(trace)

        try:
            trace = "```" + trace + "```"
            embed = discord.Embed(title=titre, description=trace, color=0xFF0000)

            owners_id = []
            for owner_id in self.bot.cfg["check"]["owners_id"].values():
                for member in self.bot.get_all_members:
                    if owners_id == member.id:
                        owner = member
                        await self.bot.send_message(owner, embed=embed)
                        owners_id.append(owner.mention)
        except Exception as e:
            self.log.error(traceback.format_exc())
        raise ECogsManagedException
