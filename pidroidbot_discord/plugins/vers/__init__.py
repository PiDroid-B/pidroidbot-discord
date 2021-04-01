import asyncio
import logging
import random
import string
import time
import traceback

import pidroidbot_discord.plugins.core as core

# import const.ressource_vote as ress
# import discord
from discord.ext import commands
from pidroidbot_discord.module.config import config

# from tools import check, convert
log = logging.getLogger("plugins.version")


class Version(core.CogCore):
    def __init__(self, bot):
        super().__init__(bot)
        log.warning("\t\t" + __name__ + " initialisé" + config["main"]["lang"])

        self.versions = {
            "V1.0.x": "__Nouvelles fonctionnalités :__\n"
            "copy           Copie les messages d'un chan à l'autre\n"
            "delete         Supprime les messages d'un chan\n"
            "ping           Vérifie la latence\n"
            "pop            Déclare que tu viens de faire pop sur un système\n"
            "rappel         Envoie une notification après un temps donné\n"
            "reco           Affiche le chemin à suivre pour une reconnaissance\n",
            "V2.0.0": "__Amélioration anciennes fonctionnalités :__\n"
            """Commandes : ```
copy           Copie les messages d'un chan à l'autre (admin)
delete         Supprime les messages d'un chan (admin)
ping           Vérifie la latence
pop            Déclare que tu viens de faire pop sur un système
rappel         Envoie une notification après un temps donné (privé ou leader)
reco           Affiche le chemin à suivre pour une reconnaissance
```
__Nouvelles fonctionnalités :__
Commandes : ```
poplibre       Déclare que tu viens découvrir des pop non revendiqués
role           Affiche la liste des roles et leur définition
tools          outils pour trouver des informations (admin)
user           Modifie les droits d'un utilisateur (langue, role) (leader)
version        Affiche le numéro de version 
```
Système de traduction : ```
mono-channel      tranforme les messages pour donner 
multi-channels    copie et traduits les messages d'un chan à l'autre 
```             
""",
            "V2.1.0": """__Nouvelles fonctionnalités :__
Commandes : ```
god            Vous êtes omniscient Wow !!! (Leader)
```
- Le bot mentionne son interlocuteur lors des échanges, Cela évite de se télescoper 
lorsque l'on est plusieurs a le soliciter.

- Système d'autoredémarrage en cas de crash.            
""",
            "V2.2.1": """__Nouvelles fonctionnalités :__
        Commandes : ```
        user           Gestion des utilisateurs (droits, dossier, sanction, grace...) (leader)
        ```
        bugfixes
        """,
            "V2.2.2": """__Nouvelles fonctionnalités :__
        Commandes : 
        ```
        user           Gestion des utilisateurs (droits, dossier, sanction, grace...) (leader) + user info
        contact        Notifier un utilisateur quelque soit sa langue (bug)
        ```    
            __Bugfixes :__
        ```
        !user change [utilisateur] - ne crash plus lorsque l'utilisateur est précisé et n'existe pas
        notification et mention - traduit par google, les pseudos et chans sont maintenant notifiés en fin de message
        auto-traduction
        mise à jour des roles
        ```
        """,
            "V2.3.0": """__Nouvelles fonctionnalités :__
        Ajout du chinois
            
        Commandes : 
        ```
        contact        Notifier un utilisateur quelque soit sa langue (internationale)
        ```    
            __Bugfixes :__
        ```
        sanctions : réajustement pour anti-ban discord du plugin (les sanctions n'étaient plus mises à jours)
        notification everyone : est maintenant rajouté même si traduit
        
        ```            
            """,
        }

        self.current_version = "V2.3.0"

    @commands.group(brief="Affiche le numéro de version", pass_context=True, no_pm=True)
    async def version(self, ctx):
        """
        Affiche le numéro de version
        """
        if ctx.invoked_subcommand is None:
            if len(ctx.message.content.split()) > 1:
                await self.send_msg(ctx, msg="Commande ?", send_help=True)
                return

            version = self.current_version

            try:
                await self.send_msg(ctx, msg=version, send_help=True)
            except Exception as e:
                await self.raise_msg(ctx, msg_type="version", except_type="inconnu")
                raise

    @version.command(
        brief="Affiche le détail d'une version", pass_context=True, no_pm=True
    )
    async def change_log(self, ctx, version=""):
        """
        Affiche le détail d'une version

        [version]       : FACULTATIF, au format Vx.x.x
                          - si non précisé :
                            affiche le détail de la dernière version
                            affiche les autres numéros de version
                          - si précisé :
                            affiche le détail de la version précisé

        """

        if version == "":
            changelog = "**{0}**\n{1}".format(
                self.current_version, self.versions[self.current_version]
            )
        else:
            try:
                changelog = "**{0}**\n{1}".format(version, self.versions[version])
            except:
                changelog = "version inconnu"
                await self.send_msg(ctx, msg=changelog, send_help=True)
                return

        try:
            await self.send_msg(ctx, msg=changelog, send_help=False)
        except Exception as e:
            await self.raise_msg(ctx, msg_type="version", except_type="inconnu")
            raise

    @version.command(
        brief="Affiche l'historique des versions", pass_context=True, no_pm=True
    )
    async def history(self, ctx):
        """
        Affiche l'historique des versions

        """

        list_version = self.versions.keys()
        list_version = sorted(list_version)

        msg_histo = "\n".join(list_version)

        history = "__History :__\n```{0}```".format(msg_histo)

        try:
            await self.send_msg(ctx, msg=history, send_help=False)
        except Exception as e:
            await self.raise_msg(ctx, msg_type="version", except_type="inconnu")
            raise


def setup(bot):
    bot.add_cog(Version(bot))
