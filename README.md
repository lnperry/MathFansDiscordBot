# MathFansDiscordBot

MathFansDiscordBot is a Python based Discord Bot to help with streaming/lecturing during COVID-19

## Installation
##### Create a server
Create a free server at https://discordapp.com if you do not have one yet. Simply log in, and then click the plus sign on the left side of the main window to create a new server.

##### Create an application
Go to https://discordapp.com/developers and create a new application.

##### Create a Bot
Navigate to the Bot tab in your Discord application details, and click Add Bot.
![Image of Adding Bot](https://i.imgur.com/1ZhnfNp.png)

##### Generating server authentication hyperlink a Bot user
Navigate to the OAuth2 tab in your Discord application details, under the scope table toggle the bot checkbox. Scroll down to the permissions and toggle administrator permissions. Copy the hyperlink
MathFansDiscordBot uses administrator permissions for the Queue feature, but does not need admin permissions to take attendance.
![Image of Adding Bot](https://i.imgur.com/iJJY7md.png)

##### Authorizing a bot user
Visit the hyperlink in your web browser and follow the instructions to authorize your Bot user.
![Image of Adding Bot](https://i.imgur.com/0bvAitV.png)

##### Save the Bot user token
Navigate back to the Bot tab after creating your application and create a bot user. **Save the token**, you will need it later to run the bot. ***Do NOT share the token with any unathorized users or post online***
![Image of Adding Bot](https://i.imgur.com/m9IKkVO.png)

##### Install the python package discord.py
Open python from your system terminal/shell/command prompt and use the example below to install discord.py.

```bash
python -m pip install discord.py
```

## Using MathFansDiscordBot

##### Installation
Download the compressed ZIP file [here](https://github.com/PerryProjects/MathFansDiscordBot/archive/master.zip) and unzip into another folder.

##### Usage
To start your instance of the bot some changes are needed to the main python file.
Open [MathFansDiscordBot.py](https://github.com/PerryProjects/MathFansDiscordBot/blob/master/mathfansdiscordbot.py) with a text editor such as notepad, notepad++, etc. or an IDE of choice.

On download, lines 12-14 will include the text:
```python
# Change Per Server Deployment
token = 'bot_token'
instructor = 'instructor_ID'
current_voice_channel = 0
```

You must change these values to:
1. Your personal **token** found when you created the bot account on discord (see Installation).
2. Your personal **instructor_id** which can be found by using the Discord desktop app in developer mode and right clicking your username in then selecting 'copy id' at the bottom of the pop up menu.
3. The name of the server where you would like to use this bot.
4. Set current voice channel with the bot command !changeinstructor.

The resulting code block should look something like this:
```python
# Change Per Server Deployment
token = 'D43f5y0ahjqew82jZ4NViEr2YafMKhue'
instructor = 307362705684299777
server_name = 'My Test Server'
```

Once you have verified that the submitted information is correct, save and exit. Then run the attached 'run.bat'

## Commands

For the Student:
Command | Function
------------ | -------------
**!attendance {student name}** | logs the student to the attendance log
**!talk** | adds the user to the voice queue
**!done** | removes the user from the voice queue
**!queue** | shows current queue to ask questions
**!poll** | creates a reaction poll with format [!poll <question>? <option1>:<option2>]

For the Instructor:
Command | Function
------------ | -------------
**!start** | start class, will mute users in voice chat
**!end** | ends class, will unmutes all users in voice chat
**!qauto** | changes questions to cycle automatically
**!qsingle** | changes questions to cycle one at a time
**!next** | cycles to the next student in line
**!changeinstructor {instructor_id}** | changes the current instructor to a new instructor

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
