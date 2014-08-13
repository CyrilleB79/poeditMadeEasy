# poeditMadeEasy #
- Author: Him Prasad Gautam <drishtibachak@gmail.com>
- Download [3.1][1]

## Introduction ##
This Add- on makes poedit more accessible and informative in many aspect of the shortcut command of poedit.
It also indicates the different category of messages by either a beep or a preceded asterisk announcement. The  indicating sound  will help to identify the spots of possible  error and help in correction.
Now, you can know the   source text and the translation texts separately. Further more, the plural formed messages (if any)can now be distinctly recognized. This will help you to judge the translation accuracy more easily. It avoids the round trip of TAB and shift+TAB if desired to know these messages individually.

## Features ##
- Announcement of the instrumented action on pressing poedit shortcut commands.
 - Specific  indication of Message  category  by a distinct  beep and/or asterick.
- Within current nvda session, the Beep can be set to 'on' or 'off' mode.
- In 'beep off' mode, alternate way of indication of message category.
- Standalone reporting of translation texts.
- Standalone reporting of source texts.
- Reporting of  poedit translation syntax error.
- Reporting about  the comment window.
- Reporting about  the 'Note for Translators' window.
- Reporting of the existance of the plural form of the      selected   message if prevailed.

## Indication for Message type ##
### In 'beep on' mode ###
- High pitched tone: No translation.
- Median pitched tone: Fuzzy translation.
- Low pitch tone:
	- the source and the translation is same.
	- The number of ampersand  sign in source and translation differs.
- No beep: Translation is normal.
### In 'beep off' mode ###
- Message preceded by double asterisk (**): No translation.
- Message preceded by single asterisk (*): Fuzzy translation.
- Message preceded by single asterisk (*):
	- the source and the translation text is same.
	- The number of ampersand  sign in source and translation is not equal.
- Message without asterisk preceed: Normal translation.
### In both beep mode ###
- extra sharp beep: Error due to violation of translation Rule.

## Keyboard commands ##
- control+b: Copies the source text to the translation box and reports.
- control+k: Deletes the translation and reports. Informs if no text available.
- control+s: saves the file by notifying the action being performed.
- control+u: Toggled the message type to fuzzy or normal and reports. Informs if no text available.
- control+shift+a: Announcement about the 'Note for Translators' window.
- control+shift+c: Announcement about the comment window.
- control+shift+p: Temporarily toggles the beep mode to ON or OFF mode and reports.
- control+shift+r:
	- Announces the source message text.
	- In case of plural form, pressing twice  reports the plural    source text.
- control+shift+t:
	- Announces the translation message text.
	- In case of plural form, pressing twice  reports the next form of translation.
- control+shift+v: Toggles the level of beep tone into sharp or mild.
- control+shift+e: Describes the cause of error.

## Changes for 1.0beta version ##
- Initial version.

## Changes in 1.1beta version ##
- Within current session, an option  to set  the tone to mild or sharp level is added.
- Now, by pressing control+shift+v, you can Toggle the tone level between  sharp and mild.

## Changes in 1.0dev version ##
- Addition of new features:
- Error Indication.
- now, poeditMadeEasy automatically detects the following violation of translation rules
	- Missing of the percent variables viz. %s,%d,%u,%g.
	- Missing variable/index enclosed by braces or brackets
	- Missing of  some paragraph.
	- a warning of Mismatch of ampersand sign. It may be or may not be an error.
- Error indication:
 - If the above errors are detected; poeditMadeEasy plays the nvda error sound instead a beep.
 - Once the error indication sound is played, you can know exact error by pressing control+shift+e.
- Reporting of status:
 - Now, you can know The current status of the translation by pressing control+shift+d.

## changes in 3.0dev ##
- Addition of new Features:
- Now poeditMadeEasy is accessible in plural formed messages.
- Now,  In plural form messages:
	- the singular and plural form message of source can be known separately.
	- press  control+shift+r  to know the singular  message. Press  twice for plural form.
	- the singular and plural form message of translation  can be known separately.
	- press  control+shift+t  to know the focussed   form of message. Press  twice for next form.
- Now, While reporting the error of plural formed messages,  press of control+shift+e will  report the  exact message  singular or plural containing the error.
- Note: There are no plural formed message in main nvda or in its official add-ons! You can find them in wxwidgit, orca, linus or poedit itself.
  - Corrections:
-  since nvda global command (nvda+shift+end) serve the same, Removed the status gesture added in 1.0dev.
- Fixed the bug that  was indicating  unusual error in some messages.

## Changes in 3.0dev ##
- Bug fixing.
-	 More clarity in error checking.

## Changes in 3.1 ##
- Fixed  the issue of  inaccessibility  of the 'note for Translators' window.
- Added more parameters  of  error checking.
- Fixed the issue of self truncation of long listview  messages.
- Now, on    twice pressing, it will inform  if no  plural form  exist.
- To remove the confusion, Redesigned the error indication beep tone instead a play of  nvda error sound.
- Added the plural form notifying  feature if it prevailed.