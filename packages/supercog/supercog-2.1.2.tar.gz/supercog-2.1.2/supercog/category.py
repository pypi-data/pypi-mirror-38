import inspect, shlex

class Category:
    """Creates a new `Category` object.

    The `nsfw_channel_error` is a function that gives an error message when a command is NSFW being run in a SFW channel.
        Note: The default function will return a simple error message.
    
    The `private_message_error` is a function that gives an error message when a command is trying to be run in a Private Message but can't.
        Note: The default function will return a simple error message.
    
    The `server_mod_error` is a function that gives an error message when a Discord Member is trying to run a Server Moderator command
    without having the proper permissions.
        Note: The default function will return a simple error message.
    
    The `bot_mod_error` is a function that gives an error message when a Discord Member is trying to run a Bot Moderator command
    without having the proper permissions.
        Note: The default function will return a simple error message.

    The `locally_inactive_error` is a function that gives an error message when a command is inactive in a Server.
        Note: The default function will return a simple error message.
    
    The `globally_inactive_error` is a function that gives an error message when a command is inactive throughout the Bot.
        Note: The default function will return a simple error message.

    The `locally_active_check` is a function that checks if a `Command` is active in a Server.
        If providing a custom function, you must give the Discord Server and Command to check
        Note: The default function will return True.
    
    The `globally_active_check` is a function the checks if a `Command` is active throughout the Bot.
        If providing a custom function, you must give the Command to check.
        Note: The default function will return True.
            If a Bot Moderator runs the command, it will run normally as to easily test it.

    The `server_mod_check` is merely a function that checks if a Discord Member is a Server Moderator.
        Note: The default function will check if they have Manage Server permissions.
            A server_mod_check function should only accept one parameter: The Discord Member.

    The `bot_mod_check` is also a function that checks if a Discord Member is a Bot Moderator.
        Note: The default function will check if a Discord Member is the Bot's Owner.
            A bot_mod_check function should only accept one parameter: The Discord Member

    Parameters:
        discordClient (discord.Client): The Discord Client object that the Category uses.
        categoryName (str): The name of the Category.

        description (str): The description of the Category.
        restriction_info (str): The restrictions of the Category.

        nsfw_channel_error (func): The function that gives an error message when an NSFW Command 
                                is trying to be run in a SFW Channel.
        private_message_error (func): The function that gives an error message when a Command is 
                                    trying to be run in a Private Message but can't be.
        server_mod_error (func): The function that gives an error message when a Discord Member who is not a 
                                Server Moderator tries to run a Command that only Server Moderator's can run.
        bot_mod_error (func): The function that gives an error message when a Discord Member who is not a
                            Bot Moderator tries to run a Command that only Bot Moderator's can run.
        locally_inactive_error (func): The function that gives an error message when a Command is trying to
                                    be run when the Command is inactive in the Server.
        globally_inactive_error (func): The function that gives an error message when a Command is trying to
                                        be run when the Command is inactive in the Bot.

        locally_active_check (func): The function that checks whether or not a Command is active in a Server.
        globally_active_check (func): The function that checks whether or not a Command is active in the Bot.

        server_mod_check (func): The function that checks whether or not a Discord Member is a Server Moderator.
        bot_mod_check (func): The function that checks whether or not a Discord Member is a Bot Moderator.
    """

    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Default Class Fields
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    DESCRIPTION = "A {} Category."
    RESTRICTION_INFO = None

    EMBED_COLOR = 0xC8C8C8 # Default is a bright white rgb(200, 200, 200)

    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Error Messages
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    NOT_ENOUGH_PARAMETERS = "NOT_ENOUGH_PARAMETERS"
    """str: An error identifier for when there are not enough parameters in a command.
    """

    TOO_MANY_PARAMETERS = "TOO_MANY_PARAMETERS"
    """str: An error identifier for when there are too many parameters in a command.
    """

    INVALID_PARAMETER = "INVALID_PARAMETER"
    """str: An error identifier for when a parameter is not valid.
    """

    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Class Methods
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    @staticmethod
    def parseText(prefixes, text):
        """Uses the `shlex` module to split the text in a smarter way.

        Parameters:
            prefixes (list): A list of prefixes that can be used for a Command.
            text (str): The text to split up.
        
        Returns:
            command, parameters (tuple)
        """

        # Remove the prefix
        for prefix in prefixes:
            if text.startswith(prefix):
                text = text[len(prefix):]
                break

        # Try using shlex to split the text
        try:
            
            split = shlex.split(text)
        
        # Shlex splitting failed; Use the regular split method using a space as the split character
        except:

            split = text.split(" ")
        
        # One of the 2 worked; Get the command and parameters from it
        finally:
            
            # Command is first index; Parameters are everything after
            command = split[0]
            parameters = split[1:]

            return command, parameters
    
    @staticmethod
    def defaultNSFWChannelError():
        """The default function that gives an error when a Command is NSFW being run in a SFW Channel.
        """

        return "This command is NSFW. You must run it in an NSFW Channel."
    
    @staticmethod
    def defaultPrivateMessageError():
        """The default function that gives an error when a Command is trying to be run in a Private Message but can't.
        """

        return "You cannot run this command in a Private Message."
    
    @staticmethod
    def defaultServerModError():
        """The default function that gives an error when a Discord Member is trying to run a Server Moderator command 
        without having the proper permissions.
        """

        return "You do not have the proper permissions to run this command."
    
    @staticmethod
    def defaultBotModError():
        """The default function that gives an error when a Discord Member is trying to run a Bot Moderator command
        without having the proper permissions.
        """

        return "You do not have the proper permissions to run this command."
    
    @staticmethod
    def defaultLocallyInactiveError():
        """The default function that gives an error when a Command is inactive in a Server.
        """
        
        return "This command is locally inactive right now."
    
    @staticmethod
    def defaultGloballyInactiveError():
        """The default function that gives an error when a Command is inactive in the Bot.
        """

        return "This command is globally inactive right now."
    
    @staticmethod
    def defaultLocalActiveCheck(discordServer, commandObject):
        """The default function that checks if the Command is active in the Server.

        Parameters:
            discordServer (discord.Guild): The Discord Server to check for the active status of the Command
            commandObject (supercog.Command): The Command to check.
        """

        return True
    
    @staticmethod
    def defaultGlobalActiveCheck(commandObject):
        """The default function that checks if the Command is active in the Bot.

        Parameters:
            commandObject (supercog.Command): The Command to check.
        """

        return True

    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Constructor
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def __init__(self, discordClient, categoryName, *, description = None, restriction_info = None, nsfw_channel_error = None, private_message_error = None, server_mod_error = None, bot_mod_error = None, locally_inactive_error = None, globally_inactive_error = None, locally_active_check = None, globally_active_check = None, server_mod_check = None, bot_mod_check = None):
        """Creates a new `Category` object.

        The `nsfw_channel_error` is a function that gives an error message when a command is NSFW being run in a SFW channel.
            Note: The default function will return a simple error message saying \"This command is NSFW. You must run it in an NSFW Channel.\"
        
        The `private_message_error` is a function that gives an error message when a command is trying to be run in a Private Message but can't.
            Note: The default function will return a simple error message saying \"You cannot run this command in a Private Message.\"
    
        The `server_mod_error` is a function that gives an error message when a Discord Member is trying to run a Server Moderator command
        without having the proper permissions.
            Note: The default function will return a simple error message saying \"You do not have the proper permissions to run this command.\"

        The `bot_mod_error` is a function that gives an error message when a Discord Member is trying to run a Bot Moderator command
        without having the proper permissions.
            Note: The default function will return a simple error message saying \"You do not have the proper permissions to run this command.\"

        The `locally_inactive_error` is a function that gives an error message when a command is inactive in a Server.
            Note: The default function will return a simple error message saying \"This command is locally inactive right now.\"

        The `globally_inactive_error` is a function that gives an error message when a command is inactive throughout the Bot.
            Note: The default function will return a simple error message saying \"This command is globally inactive right now.\"

        The `locally_active_check` is a function that checks if a `Command` is active in a Server.
            If providing a custom function, you must give the Discord Server and Command to check
            Note: The default function will return True.

        The `globally_active_check` is a function the checks if a `Command` is active throughout the Bot.
            If providing a custom function, you must give the Command to check.
            Note: The default function will return True.
                  If a Bot Moderator runs the command, it will run normally as to easily test it.

        The `server_mod_check` is merely a function that checks if a Discord Member is a Server Moderator.
            Note: The default function will check if they have Manage Server permissions.
                  A server_mod_check function should only accept one parameter: The Discord Member.

        The `bot_mod_check` is also a function that checks if a Discord Member is a Bot Moderator.
            Note: The default function will check if a Discord Member is the Bot's Owner.
                  A bot_mod_check function should only accept one parameter: The Discord Member

        Parameters:
            discordClient (discord.Client): The Discord Client object that the Category uses.
            categoryName (str): The name of the Category.

            description (str): The description of the Category.
            restriction_info (str): The restrictions of the Category.

            nsfw_channel_error (func): The function that gives an error message when an NSFW Command 
                                       is trying to be run in a SFW Channel.
            private_message_error (func): The function that gives an error message when a Command is 
                                          trying to be run in a Private Message but can't be.
            server_mod_error (func): The function that gives an error message when a Discord Member who is not a 
                                     Server Moderator tries to run a Command that only Server Moderator's can run.
            bot_mod_error (func): The function that gives an error message when a Discord Member who is not a
                                  Bot Moderator tries to run a Command that only Bot Moderator's can run.
            locally_inactive_error (func): The function that gives an error message when a Command is trying to
                                           be run when the Command is inactive in the Server.
            globally_inactive_error (func): The function that gives an error message when a Command is trying to
                                            be run when the Command is inactive in the Bot.

            locally_active_check (func): The function that checks whether or not a Command is active in a Server.
            globally_active_check (func): The function that checks whether or not a Command is active in the Bot.

            server_mod_check (func): The function that checks whether or not a Discord Member is a Server Moderator.
            bot_mod_check (func): The function that checks whether or not a Discord Member is a Bot Moderator.
        """

        self.client = discordClient
        self.setCategoryName(categoryName)

        self.setDescription(description)
        self.setRestrictionInfo(restriction_info)

        self.setNSFWChannelError(nsfw_channel_error)
        self.setPrivateMessageError(private_message_error)
        self.setServerModError(server_mod_error)
        self.setBotModError(bot_mod_error)
        self.setLocallyInactiveError(locally_inactive_error)
        self.setGloballyInactiveError(globally_inactive_error)

        self.setLocallyActiveCheck(locally_active_check)
        self.setGloballyActiveCheck(globally_active_check)

        self.setServerModCheck(server_mod_check)
        self.setBotModCheck(bot_mod_check)

        self._commands = []
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Getters
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def getCategoryName(self):
        """Returns the name of the Category.

        Returns:
            categoryName (str)
        """

        return self._category_name
    
    def getDescription(self):
        """Returns the description of the Category.

        Returns:
            description (str)
        """

        return self._description
    
    def getRestrictionInfo(self):
        """Returns the restriction info of the Category.

        Returns:
            restriction_info (str)
        """

        return self._restriction_info

    def getCommands(self):
        """Returns the Commands in the Category.

        Returns:
            commands (list)
        """
        
        return self._commands
    
    def getCommand(self, commandString):
        """Returns the specific Command given by a command string.

        Parameters:
            commandString (str): The command, or an alternative, of a Command
        
        Returns:
            command (Command)
        """

        # Iterate through Category's Commands
        for command in self.getCommands():
            if commandString in command.getAlternatives():
                return command
        
        return None
    
    def isCommand(self, commandString):
        """Returns whether or not a Command is in this Category given by a command string.

        Parameters:
            commandString (str): The command, or an alternative, of a Command
        
        Returns:
            isCommand (bool)
        """

        return self.getCommand(commandString) != None
    
    def getCategoryHelp(self, category, *, isNSFW = False, maxFieldLength = 1000):
        """Returns a dictionary for the help menu of a Category

        A help dictionary will include the following:
            1.) The Category's name.
            2.) The Commands in the Category.
            3.) Info on what each Command does.
        
        The help dictionary will have the following tags:
            \"title\": The Category's name.
            \"fields\": The list of Commands in the Category.

        Parameters:
            category (Category): The Category object to get the help menu for.
            isNSFW (bool): Whether or not the help menu should censor NSFW text.
            maxFieldLength (int): The maximum text size of each field. (Defaults to 1000)
        
        Returns:
            categoryHelp (dict)
        """

        # Add the commands
        fields = []
        fieldText = ""
        for command in category.getCommands():

            commandText = command.getHelp(isNSFW = isNSFW)["title"] + "\n"

            if len(fieldText) + len(commandText) >= maxFieldLength:
                fields.append(fieldText)
                fieldText = ""
            
            fieldText += commandText

        if len(fieldText) > 0:
            fields.append(fieldText)
        
        # Return the Category help as a dictionary
        return {
            "title": category.getCategoryName(),
            "fields": fields
        }
    
    def getHelp(self, command = None, *, inServer = False, isNSFW = False, maxFieldLength = 1000):
        """Returns help for a Command, or all Commands.

        Parameters:
            command (Command): The Command to get help for. (Defaults to None)
            inServer (bool): Whether or not the help menu is being sent in a Discord Server or a DMChannel/GroupChannel.
            isNSFW (bool): Whether or not to show the NSFW results. (Defaults to False)
            maxFieldLength (int): The maximum text size for a field. (Defaults to 1000)
        
        Returns:
            fields (list): If getting help for all Commands in this Category.
            command (dict): If getting help for a single Command in this Category.
        """

        # Check if command is None; Get help for all Commands
        if command == None:

            # Setup fields
            fields = []
            fieldText = ""
            for cmd in self.getCommands():

                # Only add Command if Command can't be run in private
                if (not inServer and cmd.canBeRunInPrivate() or inServer):

                    # Get help text and censor it
                    cmd = cmd.getHelp(isNSFW = isNSFW, maxFieldLength = maxFieldLength)["title"] # Only get the title from the dictionary that results; The other tags are empty

                    # Make sure field text does not exceed maxFieldLength
                    if len(fieldText) + len(cmd) >= maxFieldLength:
                        fields.append(fieldText)
                        fieldText = ""
                    
                    fieldText += cmd
            
            if len(fieldText) > 0:
                fields.append(fieldText)
            
            return fields
        
        # Help for specific command
        for cmd in self.getCommands():
            if command in cmd.getAlternatives():
                return cmd.getHelp(inDepth = True, isNSFW = isNSFW, maxFieldLength = maxFieldLength)
    
    def getHTML(self):
        """Returns the HTML rendering text for the `Category`

        Returns:
            htmlText (str)
        """

        # Setup HTML Text
        html = (
            "<h2>{}</h2>\n" +
            "  <p><em>{}</em></p>\n" +
            "  <p style=\"color:#FF5555\"><strong>{}</strong></p>\n"
        ).format(
            self.getCategoryName(),
            self.getDescription(),
            self.getRestrictionInfo() if self.getRestrictionInfo() != None else ""
        )

        # Iterate through Commands
        html += "<ul>\n"
        for command in self.getCommands():
            html += command.getHTML() + "\n"
        html += "</ul>\n"
        
        return html
    
    def getMarkdown(self):
        """Returns the Markdown render text for this `Category`.\n

        Returns:
            markdownText (str)
        """

        # Setup Markdown Text
        markdown = "## {}\n  *{}*\n\n".format(
            self.getCategoryName(),
            self.getDescription()
        )

        if self.getRestrictionInfo() != None:
            markdown += "  **{}**\n".format(
                self.getRestrictionInfo()
            )

        # Iterate through Commands
        for command in self.getCommands():
            markdown += command.getMarkdown() + "\n"
        
        return markdown
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Setters
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def setCategoryName(self, category_name):
        """Sets the name of the `Category`

        Parameters:
            category_name (str): The name of the Category
        """

        self._category_name = category_name

    def setDescription(self, description):
        """Sets the description of the `Category`

        Parameters:
            description (str): The description of the Category.
        """

        self._description = description
        if description == None:
            self._description = Category.DESCRIPTION.format(self.getCategoryName())
        
    def setRestrictionInfo(self, restriction_info):
        """Sets the restriction info of the `Category`

        Parameters:
            restriction_info (str): The restriction info of the Category.
        """

        self._restriction_info = restriction_info
        if restriction_info == None:
            self._restriction_info = Category.RESTRICTION_INFO
    
    def setNSFWChannelError(self, nsfw_channel_error):
        """Sets the NSFW Channel error function for the `Category`

        Parameters:
            nsfw_channel_error (func): The function that gives an error when an NSFW Command is trying to be run in a SFW Channel.
        """

        if nsfw_channel_error == None:
            nsfw_channel_error = Category.defaultNSFWChannelError

        if callable(nsfw_channel_error):
            self._nsfw_channel_error = nsfw_channel_error
        else:
            raise TypeError("The function provided is not callable.")
    
    def setPrivateMessageError(self, private_message_error):
        """Sets the Private Message error function for the `Category`

        Parameters:
            private_message_error (func): The function that gives an error when a Command is trying to be run in a Private Message.
        """

        if private_message_error == None:
            private_message_error = Category.defaultPrivateMessageError

        if callable(private_message_error):
            self._private_message_error = private_message_error
        else:
            raise TypeError("The function provided is not callable.")
    
    def setServerModError(self, server_mod_error):
        """Sets the Server Mod error function for the `Category`

        Parameters:
            server_mod_error (func): The function that gives an error when a Server Moderator Command 
                                     is trying to be run by someone who isn't a Server Moderator.
        """

        if server_mod_error == None:
            server_mod_error = Category.defaultServerModError

        if callable(server_mod_error):
            self._server_mod_error = server_mod_error
        else:
            raise TypeError("The function provided is not callable.")
    
    def setBotModError(self, bot_mod_error):
        """Sets the Bot Mod error function for the `Category`.

        Parameters:
            bot_mod_error (func): The function that gives an error when a Bot Moderator command
                                  is trying to be run by someone who isn't a Bot Moderator.
        """

        if bot_mod_error == None:
            bot_mod_error = Category.defaultBotModError

        if callable(bot_mod_error):
            self._bot_mod_error = bot_mod_error
        else:
            raise TypeError("The function provided is not callable.")
    
    def setLocallyInactiveError(self, locally_inactive_error):
        """Sets the Locally Inactive error function for the `Category`.

        Parameters:
            locally_inactive_error (func): The function that gives an error when a Command is Locally Inactive.
        """

        if locally_inactive_error == None:
            locally_inactive_error = Category.defaultLocallyInactiveError

        if callable(locally_inactive_error):
            self._locally_inactive_error = locally_inactive_error
        else:
            raise TypeError("The function provided is not callable.")
    
    def setGloballyInactiveError(self, globally_inactive_error):
        """Sets the Globally Inactive error function for the `Category`.

        Parameters:
            globally_inactive_error (func): The function that gives an error when a Command is Globally Inactive.
        """

        if globally_inactive_error == None:
            globally_inactive_error = Category.defaultGloballyInactiveError

        if callable(globally_inactive_error):
            self._globally_inactive_error = globally_inactive_error
        else:
            raise TypeError("The function provided is not callable.")
        
    def setLocallyActiveCheck(self, locally_active_check):
        """Sets the function that checks if a `Command` is active in a Server.

        The function provided must accept two parameters:
            discordServer (discord.Guild): The Discord Server to check if a Command is active.
            commandObject (supercog.Command): The Command to check.

        Parameters:
            locally_active_check (func): The function that checks if a Command is active in a Server.
        """

        if locally_active_check == None:
            locally_active_check = Category.defaultLocalActiveCheck
        
        if callable(locally_active_check):
            self._locally_active_check = locally_active_check
        else:
            raise TypeError("The function provided is not callable.")
    
    def setGloballyActiveCheck(self, globally_active_check):
        """Sets the function that checks if a `Command` is active in a Bot.

        The function provided must accept one parameter:
            commandObject (supercog.Command): The Command to check.

        Parameters:
            globally_active_check (func): The function that checks if a Command is active in the Bot.
        """

        if globally_active_check == None:
            globally_active_check = Category.defaultGlobalActiveCheck
        
        if callable(globally_active_check):
            self._globally_active_check = globally_active_check
        else:
            raise TypeError("The function provided is not callable.")

    def setServerModCheck(self, server_mod_check):
        """Sets the function that checks if a Discord Member is a Server Moderator.

        The function provided must accept one parameter:
            discordMember (discord.Member): The Discord Member to check if they are a Server Moderator.

        Parameters:
            server_mod_check (func): The function that checks if a Discord Member is a Server Moderator
        """

        if server_mod_check == None:
            server_mod_check = self.isAuthorServerModerator

        if callable(server_mod_check):
            self._server_mod_check = server_mod_check
        else:
            raise TypeError("The function provided is not callable.")
        
    def setBotModCheck(self, bot_mod_check):
        """Sets the function that checks if a Discord Member is a Bot Moderator.

        The function provided must accept one parameter:
            discordMember (discord.Member): The Discord Member to check if they are a Bot Moderator.

        Parameters:
            bot_mod_check (func): The function that checks if a Discord Member is a Bot Moderator.
        """

        if bot_mod_check == None:
            bot_mod_check = self.isAuthorBotModerator

        if callable(bot_mod_check):
            self._bot_mod_check = bot_mod_check
        else:
            raise TypeError("The function provided is not callable.")

    def setCommands(self, commands):
        """Sets the `Command`s that are in this `Category`

        Parameters:
            commands (list): The Commands in this Category
        """
        
        self._commands = commands
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Default Methods
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def getNSFWChannelError(self):
        """Rusn the NSFW Channel Error function and returns the result.
        """

        return self._nsfw_channel_error()

    def getPrivateMessageError(self):
        """Runs the Private Message Error function and returns the result.
        """

        return self._private_message_error()

    def getLocallyInactiveError(self):
        """Runs the Locally Inactive Error function and returns the result.
        """

        return self._locally_inactive_error()
    
    def getGloballyInactiveError(self):
        """Runs the Globally Inactive Error function and returns the result.
        """

        return self._globally_inactive_error()
    
    def getServerModError(self):
        """Runs the Server Mod Error function and returns the result.
        """

        return self._server_mod_error()
    
    def getBotModError(self):
        """Runs the Bot Mod Error function and returns the result.
        """

        return self._bot_mod_error()

    def isCommandLocallyActive(self, discordServer, commandObject):
        """Runs the Locally Active Check function and returns the result.

        Parameters:
            discordServer (discord.Guild): The Discord Server to check in.
            commandObject (supercog.Command): The Command to check
        """

        return self._locally_active_check(discordServer, commandObject)

    def isCommandGloballyActive(self, commandObject):
        """Runs the Globally Active Check function and returns the result.

        Parameters:
            commandObject (supercog.Command): The Command to check.
        """

        return self._globally_active_check(commandObject)
    
    def getServerModCheck(self, discordMember):
        """Runs the Server Mod Check function and returns the result.

        Parameters:
            discordMember (discord.Member): The Discord Member to check if they are a Server Moderator.
        """

        return self._server_mod_check(discordMember)
    
    def getBotModCheck(self, discordMember):
        """Runs the Bot Mod Check function and returns the result.

        Parameters:
            discordMember (discord.Member): The Discord Member to check if they are a Bot Moderator.
        """

        return self._bot_mod_check(discordMember)
    
    def isAuthorServerModerator(self, discordMember):
        """The default function to check if a Discord Member has Manage Server permissions.

        Parameters:
            discordMember (discord.Member): The Discord Member to check the permissions for.
        """

        return discordMember.guild_permissions.manage_guild
    
    def isAuthorBotModerator(self, discordMember):
        """The default function to check if a Discord Member is the Bot Owner

        Parameters:
            discordMember (discord.Member): The Discord Member to check if they are the Bot Owner.
        """

        return self.client.is_owner(discordMember)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Run Method
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    async def run(self, discordMessage, commandObject, function, *args, **kwargs):
        """Runs a command given the command object.

        Parameters:
            discordMessage (discord.Message): The Discord Message to use. Used for the destination, guild, and author.
            commandObject (supercog.Command): The Command object to use.
            function (func): The function to run.
                *args (list): The arguments to pass to the function.
                **kwargs (dict): The keyword arguments to pass to the function.
        """

        # Emulate Typing
        async with discordMessage.channel.typing():

            # Command is Globally Active
            if self.isCommandGloballyActive(commandObject) or self.getBotModCheck(discordMessage.author):

                # Command is a Bot Moderator command
                if commandObject.isBotModeratorCommand():

                    # Author is a Bot Moderator
                    if self.getBotModCheck(discordMessage.author):

                        # Function is async
                        if inspect.iscoroutinefunction(function):
                            return await function(*args, **kwargs)
                        
                        # Function is sync
                        else:
                            return function(*args, **kwargs)
                    
                    # Author is not a Bot Moderator
                    else:
                        return self.getBotModError()
                
                # Command is being run in a Server
                elif discordMessage.guild != None:

                    # Command is Locally Active
                    if self.isCommandLocallyActive(discordMessage.guild, commandObject):

                        # Command is a Server Moderator Command
                        if commandObject.isServerModeratorCommand():

                            # Author is a Server Moderator
                            if self.getServerModCheck(discordMessage.author):

                                # See if Command is SFW or NSFW in NSFW Channel
                                if not commandObject.isNSFW() or (commandObject.isNSFW() and discordMessage.channel.is_nsfw()):

                                    # Function is async
                                    if inspect.iscoroutinefunction(function):
                                        return await function(*args, **kwargs)
                                    
                                    # Function is sync
                                    else:
                                        return function(*args, **kwargs)
                                
                                # Command is NSFW being run in SFW Channel
                                else:
                                    return self.getNSFWChannelError()
                            
                            # Author is not a Server Moderator
                            else:
                                return self.getServerModError()
                
                        # Command is not a Server Moderator Command
                        else:

                            # See if Command is SFW or NSFW in NSFW Channel
                            if not commandObject.isNSFW() or (commandObject.isNSFW() and discordMessage.channel.is_nsfw()):

                                # Function is async
                                if inspect.iscoroutinefunction(function):
                                    return await function(*args, **kwargs)
                                
                                # Function is sync
                                else:
                                    return function(*args, **kwargs)
                            
                            # Command is NSFW being run in SFW Channel
                            else:
                                return self.getNSFWChannelError()
                    
                    # Command is Locally Inactive
                    else:
                        return self.getLocallyInactiveError()
                
                # Command is being run in a Private Message
                else:

                    # Command can be run in Private Message
                    if commandObject.canBeRunInPrivate():

                        # Function is async
                        if inspect.iscoroutinefunction(function):
                            return await function(*args, **kwargs)
                        
                        # Function is sync
                        else:
                            return function(*args, **kwargs)
                    
                    # Command cannot be run in Private Message
                    else:
                        return self.getPrivateMessageError()
            
            # Command is not Globally Inactive
            else:
                return self.getGloballyInactiveError()