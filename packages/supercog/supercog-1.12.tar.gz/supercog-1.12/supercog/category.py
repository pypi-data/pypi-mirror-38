import shlex

class Category:
    """Creates a new Category object.\n

    Parameters:
        discordClient (discord.Client): The Discord Client object that the Category uses.
        categoryName (str): The name of the Category.
    """

    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Default Class Fields
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    DESCRIPTION = "There is not description for this category yet."
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

    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Constructor
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def __init__(self, discordClient, categoryName, description = DESCRIPTION, restriction_info = RESTRICTION_INFO):
        """Creates a new Category object.\n

        Parameters:
            discordClient (discord.Client): The Discord Client object that the Category uses.
            categoryName (str): The name of the Category.
        """

        self.client = discordClient
        self._categoryName = categoryName
        self._description = description
        self._restriction_info = restriction_info
        self._commands = []
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Getters
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def getCategoryName(self):
        """Returns the name of the Category.

        Returns:
            categoryName (str)
        """

        return self._categoryName
    
    def getDescription(self):
        """Returns the description of the Category.

        Returns:
            description (str)
        """

        return self._description
    
    def getRestrictionInfo(self):
        """Returns the restriction info of the Category.

        Returns:
            restrictionInfo (str)
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

    def setCommands(self, commands):
        """Sets the `Command`s that are in this `Category`

        Parameters:
            commands (list): The Commands in this Category
        """
        
        self._commands = commands