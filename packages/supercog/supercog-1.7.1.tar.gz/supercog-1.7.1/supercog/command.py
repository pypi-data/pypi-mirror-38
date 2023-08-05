from .exception import EmptyAcceptedParameterException, EmptyCommandException, EmptyErrorException, EmptyParameterException
from .exception import NoSuchAcceptedParameterException, NoSuchErrorException, NoSuchParameterException

from .censor import censor

from random import choice

class Error:
    """An Error class for an error in a `Command`.
    """
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Constructor
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def __init__(self, *, messages = None, errorDict = None):
        """Creates a new Error object.
        There are two (2) different ways to make an `Error` object:
            1.) Clarify the messages parameter in the constructor.
            2.) Clarify a dictionary that holds the messages for the error.
        
        You must do one or the other. 
        If they are both missing, an `EmptyErrorException` will occur.
        If both are included, the `messages` parameter will be used.

        If the `errorDict` parameter is used, the following tags must be included:
            \"messages\"

        Parameters:
            messages (list): The messages this Error object holds. (Defaults to None)
            errorDict (dict): The dict that holds the messages for this Error. (Defaults to None)
        """

        # Check if messages and errorDict are both None
        if messages == None and errorDict == None:
            raise EmptyErrorException("You must include the messages parameter or errorDict parameter.")
        
        # messages parameter exists
        if messages != None:
            self._messages = messages
        
        # errorDict parameter exists
        elif errorDict != None:
            self._messages = errorDict["messages"]
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Getters
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def getMessages(self):
        """Returns the messages that this `Error` object holds.
        """

        return self._messages
    
    def getMessage(self):
        """Returns a random error message for this `Error`
        """

        return choice(self._messages)

class AcceptedParameter:
    """An AcceptedParameter class for an accepted parameter in a `Parameter`.
    """

    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Constructor
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def __init__(self, *, alternatives = None, info = None, acceptedParameterDict = None):
        """Creates a new AcceptedParameter object.
        There are two (2) different ways to make an `AcceptedParameter` object:
            1.) Clarify the alternatives and info parameters in the constructor.
            2.) Clarify a dictionary that holds the alternative names and info for the parameter.
        
        You must do one or the other.
        If they are both missing, an `EmptyAcceptedParameterException` will occur.
        If both are included, the `alternatives` and `info` parameters will be used.

        If the `acceptedParameterDict` parameter is used, the following tags must be included:
            \"alternatives\"
            \"info\"
        
        Parameters:
            alternatives (list): The alternative names that can be used for this accepted parameter.
            info (str): The description of this accepted parameter.
        """

        # Check if all parameters are None
        if (alternatives == None or info == None) and acceptedParameterDict == None:
            raise EmptyAcceptedParameterException("You must include either the alternatives and info parameters or the acceptedParameterDict parameter.")
        
        # alternatives and info parameters exist
        if alternatives != None and info != None:
            self._alternatives = alternatives
            self._info = info
        
        # acceptedParameterDict parameter exists
        elif acceptedParameterDict != None:
            self._alternatives = acceptedParameterDict["alternatives"]
            self._info = acceptedParameterDict["info"]
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Getters
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def getAlternatives(self):
        """Returns the alternative names for this `AcceptedParameter` object.
        """

        return self._alternatives
    
    def getInfo(self):
        """Returns the description of this `AcceptedParameter` object.
        """

        return self._info

class Parameter:
    """A Parameter class for a parameter in a `Command`.
    """

    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Constructor
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def __init__(self, *, info = None, optional = None, accepted_parameters = None, parameterDict = None):
        """Creates a new Parameter object
        There are two (2) different ways to make a `Parameter` object:
            1.) Clarify the info and optional parameters in the constructor.
            2.) Clarify a dictionary that holds the info and optional tag for the parameter.
        
        You must do one or the other.
        If they are both missing, an `EmptyParameterException` will occur.
        If both are included, the `info` and `optional` parameters will be used.

        If the `parameterDict` parameter is used, the following tags must be included:
            \"info\"
            \"optional\"
        The following tags are optional:
            \"accepted_parameters\" (Defaults to an empty dictionary)
        
        Parameters:
            info (str): The description of this parameter.
            optional (bool): Whether or not the parameter is optional.
            accepted_parameters (dict): A dictionary of `AcceptedParameter` objects.
        """

        # Setup optional fields (defaults)
        self._accepted_parameters = {}

        # Check if all parameters are None
        if (info == None or optional == None) and parameterDict == None:
            raise EmptyParameterException("You must include either the info and optional parameters or the parameterDict parameter.")
        
        # info and optional parameters exist
        if info != None and optional != None:
            self._info = info
            self._optional = optional

            # the acceptedParameters list exists
            if accepted_parameters != None:
                self._accepted_parameters = accepted_parameters
        
        # parameterDict parameter exists
        elif parameterDict != None:
            self._info = parameterDict["info"]
            self._optional = parameterDict["optional"]

            # the acceptedParameters tag exists
            if "accepted_parameters" in parameterDict:
                for parameter in parameterDict["accepted_parameters"]:
                    self._accepted_parameters[parameter] = AcceptedParameter(acceptedParameterDict = parameterDict["accepted_parameters"][parameter])
        
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Getters
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def getInfo(self):
        """Returns the description of this `Parameter` object.

        Returns:
            info (str)
        """

        return self._info
    
    def isOptional(self):
        """Returns whether or not this `Parameter` object is optional.

        Returns:
            optional (bool)
        """

        return self._optional
    
    def getAcceptedParameters(self):
        """Returns the accepted parameters for this `Parameter` object.

        Returns:
            acceptedParameters (dict)
        """

        return self._accepted_parameters
    
    def getAcceptedParameter(self, acceptedParameter):
        """Returns an `AcceptedParameter` from this `Parameter` object.

        Returns:
            accepted_parameter (AcceptedParameter)
        
        Raises:
            NoSuchAcceptedParameterException - when the `accepted_parameter` parameter does not exist in this `Parameter` object.
        """

        if acceptedParameter in self._accepted_parameters:
            return self._accepted_parameters[acceptedParameter]
        
        raise NoSuchAcceptedParameterException("{} is not an accepted parameter.")

class Command:
    """A Command class used in a Discord Bot.
    """
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Constructor
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def __init__(self, *, alternatives = None, info = None, restriction_info = None, run_in_private = None, server_moderator_only = None, bot_moderator_only = None, parameters = None, errors = None, commandDict = None):
        """Creates a new Command object
        There are two (2) different ways to make a `Command` object:
            1.) Clarify the alternatives and info parameters in the constructor.
            2.) Clarify a dictionary that holds the alternatives and the info for the command.

        You must do one or the other.
        If they are both missing, an `EmptyCommandException` will occur.
        If both are included, the `alternatives` and `info` parameters will be used.

        If the `commandDict` parameter is used, the following tags must be included:
            \"alternatives\"
            \"info\"
        The following tags are optional:
            \"restriction_info\" (Defaults to an empty string)
            \"run_in_private\" (Defaults to True)
            \"server_moderator_only\" (Defaults to False)
            \"bot_moderator_only\" (Defaults to False)
            \"parameters\" (Defaults to an empty dictionary)
            \"errors\" (Defaults to an empty dictionary)
        """

        # Setup optional fields (defaults)
        self._restriction_info = ""
        self._run_in_private = True
        self._server_moderator_only = False
        self._bot_moderator_only = False
        self._parameters = {}
        self._errors = {}

        # Check if all parameters are None
        if (alternatives == None or info == None) and commandDict == None:
            raise EmptyCommandException("You must include either the alternatives and info parameters or the commandDict parameter.")
        
        # alternatives and info parameters exist
        if alternatives != None and info != None:
            self._alternatives = alternatives
            self._info = info

            # the optional tags exist
            if restriction_info != None:
                self._restriction_info = restriction_info
            if run_in_private != None:
                self._run_in_private = run_in_private
            if server_moderator_only != None:
                self._server_moderator_only = server_moderator_only
            if bot_moderator_only != None:
                self._bot_moderator_only = bot_moderator_only
            if parameters != None:
                self._parameters = parameters
            if errors != None:
                self._errors = errors
        
        # commandDict parameter exists
        elif commandDict != None:
            self._alternatives = commandDict["alternatives"]
            self._info = commandDict["info"]

            # the optional tags exist
            if "restriction_info" in commandDict:
                self._restriction_info = commandDict["restriction_info"]
            if "run_in_private" in commandDict:
                self._run_in_private = commandDict["run_in_private"]
            if "server_moderator_only" in commandDict:
                self._server_moderator_only = commandDict["server_moderator_only"]
            if "bot_moderator_only" in commandDict:
                self._bot_moderator_only = commandDict["bot_moderator_only"]
            if "parameters" in commandDict:
                for parameter in commandDict["parameters"]:
                    self._parameters[parameter] = Parameter(parameterDict = commandDict["parameters"][parameter])
            if "errors" in commandDict:
                for error in commandDict["errors"]:
                    self._errors[error] = Error(errorDict = commandDict["errors"][error])
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Getters
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def getAlternatives(self):
        """Returns the alternatives for this `Command`.

        Returns:
            alternatives (list)
        """

        return self._alternatives
    
    def getInfo(self):
        """Returns the description of this `Command` object.

        Returns:
            info (str)
        """

        return self._info
    
    def getRestrictionInfo(self):
        """Returns any restriction info for this `Command` object.

        Returns:
            restrictionInfo (str)
        """

        return self._restriction_info
    
    def canBeRunInPrivate(self):
        """Returns whether or not this `Command` object can be run in a DMChannel or a GroupChannel.

        Returns:
            runInPrivate (bool)
        """

        return self._run_in_private
    
    def isServerModeratorCommand(self):
        """Returns whether or not this `Command` object can only be run by a server moderator.

        Returns:
            serverModeratorCommand (bool)
        """

        return self._server_moderator_only
    
    def isBotModeratorCommand(self):
        """Returns whether or not this `Command` object can only be run by a bot moderator.

        Returns:
            botModeratorCommand (bool)
        """

        return self._bot_moderator_only
    
    def getParameters(self):
        """Returns the parameters for this `Command` object.

        Returns:
            parameters (dict)
        """

        return self._parameters
    
    def getParameter(self, parameter):
        """Returns a `Parameter` from this `Command` object.

        Parameters:
            parameter (str): The identifier of the `Parameter`

        Returns:
            parameters (dict)

        Raises:
            NoSuchParameterException: when the `parameter` does not exist
        """

        if parameter in self._parameters:
            return self._parameters[parameter]
        
        raise NoSuchParameterException("{} is not a parameter.")
    
    def getAcceptedParameters(self, parameter):
        """Returns the accepted parameters for a `Parameter` object.

        Parameters:
            parameter (str): The identifier of the `Parameter`

        Returns:
            acceptedParameters (dict)
        
        Raises:
            NoSuchParameterException: when the `parameter` does not exist
        """

        if parameter in self._parameters:
            return self._parameters[parameter].getAcceptedParameters()
        
        raise NoSuchParameterException("{} is not a parameter.")
    
    def getAcceptedParameter(self, parameter, acceptedParameter):
        """Returns an `AcceptedParameter` from this `Parameter` object.

        Parameters:
            parameter (str): The identifier of the `Parameter`
            acceptedParameter (str): The identifier of the `AcceptedParameter`

        Returns:
            acceptedParameter (AcceptedParameter)
        
        Raises:
            NoSuchParameterException: when the `parameter` does not exist
            NoSuchAcceptedParameterException: when the `acceptedParameter` does not exist
        """

        if parameter in self._parameters:
            return self._parameters[parameter].getAcceptedParameter(acceptedParameter)
        
        raise NoSuchParameterException("{} is not a parameter.")
    
    def getErrors(self):
        """Returns the `Error`s in this `Command` object.

        Returns:
            errors (list)
        """
        
        return self._errors
    
    def getError(self, errorType):
        """Returns an `Error` from this `Command` object.

        Parameters:
            errorType (str): The identifier of the `Error`
        
        Returns:
            error (Error)
        
        Raises:
            NoSuchErrorException: when the `errorType` does not exist
        """
        
        if errorType in self._errors:
            return self._errors[errorType]
        
        raise NoSuchErrorException("{} is not an error.")
    
    def getErrorMessage(self, errorType):
        """Returns a random error message from this `Command` object.

        Parameters:
            errorType (str): The identifier of the `Error`
        
        Returns:
            errorMessage (str)
        
        Raises:
            NoSuchErrorException: when the `errorType` does not exist
        """
        
        if errorType in self._errors:
            return self._errors[errorType].getMessage()
        
        raise NoSuchErrorException("{} is not an error.")
    
    def getHelp(self, *, inDepth = False, isNSFW = False, maxFieldLength = 1000):
        """Returns a dictionary giving help on this `Command` object.

        A short help dictionary (not inDepth) will include the following:
            1.) The primary command name.
            2.) Optional and required parameters surrounded by [] and <> respectively.
            3.) Info on what the command does
        
        A long help dictionary (inDepth) will include the following:
            1.) Alternative names for the command.
            2.) Optional and required parameters surrounded by [] and <> respectively.
            3.) Info on what the command does
            4.) Info on what each parameter is for
            5.) Info on any accepted parameters and what they represent
        
        The help dictionary will have the following tags:
            \"title\": The primary help information. 
            \"restriction\": The restriction info. (An empty string if it is not inDepth)
            \"accepted\": The accepted parameter information. (An empty dictionary if it is not inDepth)
        
        Parameters:
            inDepth (bool): Whether or not to get in-depth help for a command. (Defaults to False)
            isNSFW (bool): Whether or not to censor any NSFW material. (Defaults to False)
            maxFieldLength (int): The maximum length of a single field if inDepth. (Defaults to 1000)
        
        Returns:
            help (dict)
        """

        # Set default values
        dictRestriction = ""
        dictAccepted = {}

        # Setup Placeholder Parameters Text (Shows on both inDepth and not inDepth)
        placeholderParameters = []
        for parameter in self.getParameters():
            placeholderParameters.append("{}{}{}".format(
                "[" if self.getParameters()[parameter].isOptional() else "<",
                parameter,
                "]" if self.getParameters()[parameter].isOptional() else ">"
            ))
        placeholders = " ".join(placeholderParameters)

        # See if inDepth
        if inDepth:

            # Setup Accepted Parameter Fields
            acceptedParameters = {}
            for parameter in self.getParameters():
                parameterName = parameter
                parameterObject = self.getParameters()[parameter]

                # Only add if there are accepted parameters
                if len(parameterObject.getAcceptedParameters()) > 0:
                    acceptedParameters[parameterName] = ""

                    # Iterate through all accepted parameters and add them to a single string
                    for acceptedParameter in parameterObject.getAcceptedParameters():
                        acceptedObject = parameterObject.getAcceptedParameters()[acceptedParameter]

                        # Add parameter info to string
                        acceptedParameters[parameterName] += "`{}` - {}\n".format(
                            " | ".join(acceptedObject.getAlternatives()),
                            acceptedObject.getInfo()
                        )
            
            # Add Accepted Parameter Fields
            for parameter in acceptedParameters:

                # Setup fields
                fields = []
                fieldText = ""
                acceptedParams = acceptedParameters[parameter].split("\n")

                # Keep each parameter underneath the maxFieldLength
                for param in acceptedParams:

                    accepted = censor(param) if not isNSFW else param
                    accepted += "\n"

                    if len(fieldText) + len(accepted) >= maxFieldLength:
                        fields.append(fieldText)
                        fieldText = ""
                    
                    fieldText += accepted
                
                if len(fieldText) > 0:
                    fields.append(fieldText)
                
                # Add fields to accepted dict
                dictAccepted[parameter] = fields
            
            # Set title and fields
            dictTitle = "`{} {}` - {}\n".format(
                censor(" | ".join(self.getAlternatives()), True) if not isNSFW else " | ".join(self.getAlternatives()),
                censor(placeholders) if not isNSFW else placeholders,
                censor(self.getInfo()) if not isNSFW else self.getInfo()
            )
            dictRestriction = self.getRestrictionInfo()
            dictFields = dictAccepted
        
        # Not inDepth
        else:

            dictTitle = "`{} {}` - {}\n".format(
                censor(self.getAlternatives()[0], True) if not isNSFW else self.getAlternatives()[0],
                censor(placeholders) if not isNSFW else placeholders,
                censor(self.getInfo()) if not isNSFW else self.getInfo()
            )
        
        # Return the help dictionary
        return {
            "title": dictTitle,
            "restriction": dictRestriction,
            "accepted": dictFields
        }
    
    def getHTML(self, *, commandStyle = None, parameterStyle = None):
        """Returns the HTML rendering text for the `Command`.

        The `commandStyle` and `parameterStyle` parameters are CSS attributes inside an HTML
        file that you must declare in a `<style>` block before your HTML body.

            Example:
                ```
                styleName {
                    border-width: 2px;
                    background-color: #FF80000;
                }
                ```

        Parameters:
            commandStyle (str): A specific cell border style to use for the command cells. (Defaults to None)
            parameterStyle (str): A specific cell border style to use to the parameter cells. (Defaults to None)

        Returns:
            htmlText (str)
        """

        # Setup HTML text
        html = ""

        # Add Commands and Placeholder Parameters
        placeholderParameters = []
        for parameter in self.getParameters():
            placeholderParameters.append("{}{}{}".format(
                "[" if self.getParameters()[parameter].isOptional() else "&lt;",
                parameter,
                "]" if self.getParameters()[parameter].isOptional() else "&gt;"
            ))
        
        # Get who can access it
        access = "Anyone"
        if self.isServerModeratorCommand() and self.isBotModeratorCommand():
            access = "Only Server and Bot Moderators"
        elif self.isServerModeratorCommand():
            access = "Only Server Moderators"
        elif self.isBotModeratorCommand():
            access = "Only Bot Moderators"
        
        # Add the row for the command
        html += (
            "\t\t\t<tr>\n" +
            "\t\t\t\t<td {} style=\"width: 185px; text-align: left;\">{}</td>\n" +
            "\t\t\t\t<td {} style=\"width: 185px; text-align: left;\">{}</td>\n" +
            "\t\t\t\t<td {} style=\"width: 185px; text-align: left;\">{}</td>\n" +
            "\t\t\t\t<td {} style=\"width: 185px; text-align: left;\">{}</td>\n" +
            "\t\t\t\t<td {} style=\"width: 185px; text-align: left;\">{}</td>\n" +
            "\t\t\t</tr>\n"
        ).format(
            "" if commandStyle == None else "id=\"" + commandStyle + "\"", ", ".join(self.getAlternatives()),
            "" if commandStyle == None else "id=\"" + commandStyle + "\"", " ".join(placeholderParameters) if len(placeholderParameters) > 0 else "None",
            "" if commandStyle == None else "id=\"" + commandStyle + "\"", self.getInfo(),
            "" if commandStyle == None else "id=\"" + commandStyle + "\"", access,
            "" if commandStyle == None else "id=\"" + commandStyle + "\"", "Yes" if self.canBeRunInPrivate() else "No"
        )

        # Setup Accepted Parameter Fields
        for parameter in self.getParameters():
            parameterName = parameter
            parameterObject = self.getParameters()[parameter]

            # Only add if there are accepted parameters
            if len(parameterObject.getAcceptedParameters()) > 0:
                html += (
                    "\t\t\t\t<tr>\n" +
                    "\t\t\t\t\t<td {} style=\"width: 185px; text-align: left;\"></td>\n" +
                    "\t\t\t\t\t<td {} style=\"width: 185px; text-align: left;\"><em>{}</em></td>\n" +
                    "\t\t\t\t\t<td {} style=\"width: 185px; text-align: left;\"><em>{}</em></td>\n" +
                    "\t\t\t\t</tr>\n"
                ).format(
                    "" if parameterStyle == None else "id=\"{}\"".format(parameterStyle),
                    "" if parameterStyle == None else "id=\"{}\"".format(parameterStyle), "Accepted Parameters for `{}`".format(parameterName),
                    "" if parameterStyle == None else "id=\"{}\"".format(parameterStyle), parameterObject.getInfo()
                )
            
                # Iterate through all accepted parameters and add them to the HTML row
                for acceptedParameter in parameterObject.getAcceptedParameters():
                    acceptedObject = parameterObject.getAcceptedParameters()[acceptedParameter]

                    html += (
                        "\t\t\t\t<tr>\n" +
                        "\t\t\t\t\t<td {} style=\"width: 185px; text-align: left;\"></td>\n" +
                        "\t\t\t\t\t<td {} style=\"width: 185px; text-align: left;\"><em>{}</em></td>\n" +
                        "\t\t\t\t\t<td {} style=\"width: 185px; text-align: left;\"><em>{}</em></td>\n" +
                        "\t\t\t\t</tr>\n"
                    ).format(
                        "" if parameterStyle == None else "id=\"{}\"".format(parameterStyle),
                        "" if parameterStyle == None else "id=\"{}\"".format(parameterStyle), " | ".join(acceptedObject.getAlternatives()),
                        "" if parameterStyle == None else "id=\"{}\"".format(parameterStyle), acceptedObject.getInfo()
                    )
        
        return html
    
    def getMarkdown(self):
        """Returns the Markdown render text for the `Command`.\n

        Returns:
            markdownText (str)
        """

        # Setup Markdown Text
        markdown = ""

        # Add Commands and Placeholder Parameters
        placeholderParameters = []
        for parameter in self.getParameters():
            placeholderParameters.append("{}{}{}".format(
                "[" if self.getParameters()[parameter].isOptional() else "<",
                parameter,
                "]" if self.getParameters()[parameter].isOptional() else ">"
            ))
        
        markdown += ("  * `{} {}` - {}\n".format(
            " | ".join(self.getAlternatives()),
            " ".join(placeholderParameters) if len(placeholderParameters) > 0 else "",
            self.getInfo()
        ))

        # Setup Accepted Parameters
        for parameter in self.getParameters():
            parameterName = parameter
            parameterObject = self.getParameters()[parameter]

            # Only add if there are accepted parameters
            if len(parameterObject.getAcceptedParameters()) > 0:
                markdown += ("    * {}\n".format(
                    "Accepted Parameters for `{}`".format(
                        parameterName
                    )
                ))

                # Iterate through all accepted parameters and add them
                for acceptedParameter in parameterObject.getAcceptedParameters():
                    acceptedObject = parameterObject.getAcceptedParameters()[acceptedParameter]

                    markdown += ("      * `{}` - {}\n".format(
                        " | ".join(acceptedObject.getAlternatives()),
                        acceptedObject.getInfo()
                    ))
        
        return markdown