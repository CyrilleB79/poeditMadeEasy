# poeditMadeEasy #
- Author: Him Prasad Gautam <drishtibachak@gmail.com>.
- Download [1.0dev][1]

# Introduction #
This """Add- on makes poedit more accessible and informative in many aspect of the shortcut command of poedit.
It also indicates the different category of messages by either a beep or a preceded asterisk announcement.
Now, you can separately know the text of poedit source and translated messages. This will help you to judge the translation accuracy more easily. It avoids the round trip of TAB and shift+TAB if desired to know these messages individually.

# Features #
- Announcement of the action taken on pressing poedit shortcut commands.
 - Distinct indication of Message type by a different beep.
- Within current nvda session, the Beep can be set to 'on' or 'off' mode.
- In 'beep off' mode, alternate way of indication of message types.
- Reporting of translation texts.
- Reporting of source texts.
- Reporting of error on translation.
- Reporting the current status.

# Indication for Message type #
## In 'beep on' mode ##
- High pitched tone: No translation.
- Median pitched tone: Fuzzy translation.
- Low pitch tone: the source and the translation is same. May or may not be the error!
- No beep: Translation is normal.
## In 'beep off' mode ##
- Message preceded by double asterisk (**): No translation.
- Message preceded by single asterisk (*): Fuzzy translation.
- Message without asterisk preceed: Normal translation.

## In both beep mode ##
- Play of nvda Error sound: Error due to violation of translation Rule.
 
 ## Keyboard commands ##

- control+b: Copies the source text to the translation box and reports.
- control+k: Deletes the translation and reports. Informs if no text available.
- control+s: saves the file by notifying the action being performed.
- control+u: Toggled the message type to fuzzy or normal and reports. Informs if no text available.
- control+shift+a: Announcement about the auto comment window.
- control+shift+c: Announcement about the comment window.
- control+shift+p: Temporarily toggles the beep mode to ON or OFF mode and reports.
- control+shift+r: Announces the source message under focus.
- control+shift+t: Announces the translation messages under focus.
- control+shift+v: Toggles the level of beep tone into sharp or mild.
- control+shift+d: Reports the current status of the messages.
- control+shift+e: Describes the cause of error.

# Changes for 1.0beta version #
- Initial version.

# Changes in 1.1beta version #
- Within current session, an option  to set  the tone to mild or sharp level is available.
- Now, by pressing control+shift+v, you can Toggle the tone level between  sharp and mild.

# Changes in 1.0dev version #
### Addition of new features ###
- one: Error Indication.
- now, poeditMadeEasy automatically detects the following violation of translation rules
- Missing of the percent variables viz. %s,%d,%u,%g.
	- Missing variable/index enclosed by braces or brackets
	- Missing of  some paragraph.
	- a warning of Mismatch of ampersand sign. It may be or may not be an error.

- Two: Error details.
- If the above errors are detected; poeditMadeEasy plays the nvda error sound instead a beep.
- Once the error indication sound is played, you can know exact error by pressing control+shift+e.

- Three: Reporting of status.
- Now, you can know The current status of the translation by pressing control+shift+d.
