#addon/appModules/poedit.py
# Prepared by Him Prasad Gautam <drishtibachak@gmail.com>
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""App module for accessing Poedit.
"""

import addonHandler
import api
import appModuleHandler
import controlTypes
import displayModel
import textInfos
import tones
import ui
from NVDAObjects.IAccessible import sysListView32
import windowUtils
import NVDAObjects.IAccessible
import winUser
import scriptHandler

addonHandler.initTranslation()

doBeep = sharpTone = True


def getPoeditWindow(index, visible=True):
	try:
		obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
			windowUtils.findDescendantWindow(api.getForegroundObject().windowHandle, visible,
			controlID=index), winUser.OBJID_CLIENT, 0)
	except LookupError:
		return None
	objText = obj.value
	return objText if objText else False

class AppModule(appModuleHandler.AppModule):

	def checkError(self, sourceText, transText):
		parameter = {'{': _("brace"), '}': _("brace"), '[': _("bracket"), ']': _("bracket"),
			'%s': "%s ", '%d': "%d ", '%u': "%u ", '%g': "%g ",
			'&': _("ampersand"), '\n': "\n ", chr(13): _("paragraph")}
		for k in parameter.keys():
			if sourceText.count(k) != transText.count(k):
				return parameter[k]
		return True if sourceText == transText else None

	def script_copySourceText(self, gesture):
		gesture.send()
		# Translators: The copying of source text to translation pressing control+b in poedit.
		ui.message(_("copied original text."))
	# Translators: The description of an NVDA command of copying message in Poedit.
	script_copySourceText.__doc__ = _("Reports about the copying act in poedit.")

	def script_deleteTranslation(self, gesture):
		if getPoeditWindow(103) or getPoeditWindow(-31919) or getPoeditWindow(-31918):
			gesture.send()
			# Translators: The deletion of translation pressing control+k in poedit.
			ui.message(_("translation deleted."))
		else:
			# Translators: Report that No translation text available to delete.
			ui.message(_("No text in translation."))
	# Translators: The description of an NVDA command of deletion in Poedit.
	script_deleteTranslation.__doc__ = _("Reports about the deletion act in poedit.")

	def script_savePoFile(self, gesture):
		gesture.send()
		# Translators: The saving  of currently focused  po file by  pressing control+s.
		ui.message(_("saving the po file..."))
	# Translators: The description of an NVDA command of saving po file.
	script_savePoFile.__doc__ = _("Reports while saving the po file.")

	def script_saySourceText(self, gesture):
		# Translators: The announcement of the source text on pressing ctrl+shift+r.
		text = _("No source text.")
		if getPoeditWindow(101) and getPoeditWindow(102):
			if scriptHandler.getLastScriptRepeatCount()==0:
				text = _("singular") + ": " + getPoeditWindow(101)
			else:
				text = _("plural") + ": " + getPoeditWindow(102)
		else:
			if getPoeditWindow(101):
				if scriptHandler.getLastScriptRepeatCount()==0:
					text = getPoeditWindow(101)
				else:
					text = _("Has no plural form.")
		ui.message(text)
	# Translators: The description of an nvda command for reporting source message in Poedit.
	script_saySourceText.__doc__ = _("Reports the source text in poedit. In case of plural form of messages, pressing twice says the plural form of the source text")

	def script_sayTranslation(self, gesture):
		# Translators: The announcement of the translated text on pressing ctrl+shift+t.
		text = _("No text in translation.")
		if getPoeditWindow(103): 
			if scriptHandler.getLastScriptRepeatCount()==0:
				text = getPoeditWindow(103)
			else:
				text = _("Has no plural form.")
		elif getPoeditWindow(-31919):
			if scriptHandler.getLastScriptRepeatCount()==0:
				text = _("singular") + ": " + getPoeditWindow(-31919)
			else:
				text = _("plural") + ": "
				if getPoeditWindow(-31918, False):
					text = text+getPoeditWindow(-31918, False)
				else:
					text = text+_("No text in translation.")
		elif getPoeditWindow(-31918):
			if scriptHandler.getLastScriptRepeatCount()==0:
				text = _("plural") + ": " + getPoeditWindow(-31918)
			else:
				text = _("singular") + ": "
				if getPoeditWindow(-31919, False):
					text = text+getPoeditWindow(-31919, False)
				else:
					text = text+_("No text in translation.")
		ui.message(text)
	# Translators: The description of an nvda command for reporting translation message in Poedit.
	script_sayTranslation.__doc__ = _("Reports the translated string in poedit. In case of plural form of messages, pressing twice says the another form of the translated string")

	def script_reportError(self, gesture):
		if getPoeditWindow(101) and getPoeditWindow(103):
			caseType =""
			unequalItem = self.checkError(getPoeditWindow(101), getPoeditWindow(103))
		elif getPoeditWindow(101) and getPoeditWindow(-31919):
			caseType = _("singular")
			unequalItem = self.checkError(getPoeditWindow(101), getPoeditWindow(-31919))
			if not unequalItem:
				caseType = _("plural")
				unequalItem = self.checkError(getPoeditWindow(102), getPoeditWindow(-31918, False))
		elif getPoeditWindow(102) and getPoeditWindow(-31918):
			caseType = _("plural")
			unequalItem = self.checkError(getPoeditWindow(102), getPoeditWindow(-31918))
			if not unequalItem:
				caseType = _("singular")
				unequalItem = self.checkError(getPoeditWindow(101), getPoeditWindow(-31919, False))
		else:
			ui.message(_("No text in translation."))
			return
		if unequalItem is True:
			text = _("Warning! {caseType} message contains same text in source and translation.").format(caseType = caseType)
		elif unequalItem:
			text = _("{caseType} message has different  number of {unequalItem} in source and translation.").format(caseType = caseType, unequalItem = unequalItem)
		else:
			text = _("no syntax error.")
		ui.message(text)
	script_reportError.__doc__ = _("Describes the cause of error.")

	def script_reportAutoCommentWindow(self,gesture):
		obj = api.getForegroundObject()
		try:
			obj = obj.firstChild.next.next
			i = 1
			while i<6:
				obj = obj.firstChild.firstChild.next
				i += 2
		except AttributeError:
			obj = None
		if obj and obj.windowControlID != 101:
			try:
				obj = obj.next.firstChild
			except AttributeError:
				obj = None
		elif obj:
			obj = obj.firstChild
		if obj:
			try:
				objText = obj.name + " " + obj.value
			except:
				# Translators: Reported when there exists no note for translators.
				objText = _("No notes for translators.")
		else:
			# Translators: Reported when  unable to find the 'Notes for translators' window.
			objText = _("Could not find Notes for translators window.")
		ui.message(objText)
	# Translators: The description of an NVDA command for Poedit.
	script_reportAutoCommentWindow.__doc__ = _("Reports any notes for translators")

	def script_reportCommentWindow(self,gesture):
		objText = getPoeditWindow(104)
		if objText is False:
			# Translators: Reported when the comment window does not contain any texts.
			objText = _("Comment window has no text.")
		elif objText is None:
			# Translators: Reported when the comments window could not be found.
			objText = _("Could not find comment window.")
		ui.message(objText)
	# Translators: The description of an NVDA command for Poedit.
	script_reportCommentWindow.__doc__ = _("Reports any comments in the comments window")

	def script_toggleBeep(self, gesture):
		global doBeep
		if doBeep:
			doBeep = False
			ui.message(_("Beep off"))
		else:
			doBeep = True
			ui.message(_("Beep on"))
	# Translators: An NVDA command for toggling a beep in Poedit.
	script_toggleBeep.__doc__ = _("Toggles the beep mode and informs.")

	def script_setToneLevel(self, gesture):
		global sharpTone
		if sharpTone:
			sharpTone = False
			ui.message(_("set to mild tone"))
		else:
			sharpTone = True
			ui.message(_("set to high tone"))
	# Translators: An NVDA command for adjusting a beep volume.
	script_setToneLevel.__doc__ = _("sets the beep volume in mild and sharp level in poedit.")


	__gestures = {
		"kb:control+b": "copySourceText",
		"kb:control+s": "savePoFile",
		"kb:control+k": "deleteTranslation",
		"kb:control+shift+a": "reportAutoCommentWindow",
		"kb:control+shift+c": "reportCommentWindow",
		"kb:control+shift+e": "reportError",
		"kb:control+shift+r": "saySourceText",
		"kb:control+shift+t": "sayTranslation",
		"kb:control+shift+p": "toggleBeep",
		"kb:control+shift+v": "setToneLevel",
	}

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if "SysListView32" in obj.windowClassName and obj.role==controlTypes.ROLE_LISTITEM:
			clsList.insert(0,PoeditListItem)

	def event_NVDAObject_init(self, obj):
		if obj.role == controlTypes.ROLE_EDITABLETEXT and controlTypes.STATE_MULTILINE in obj.states and obj.isInForeground:
			left, top, long, tall = obj.location
			try:
				obj.name = NVDAObjects.NVDAObject.objectFromPoint(left + 10, top - 10).name
			except AttributeError:
				pass
			return

class PoeditListItem(sysListView32.ListItem):

	def _get_isBold(self):
		info=displayModel.DisplayModelTextInfo(self,position=textInfos.POSITION_FIRST)
		info.expand(textInfos.UNIT_CHARACTER)
		fields=info.getTextWithFields()
		try:
			return fields[0].field['bold']
		except:
			return False

	def category(self):
		# category: 0: untranslated, 1: fuzzy, 2: unsure, 3: normal, 4: Errorneous. 
		if getPoeditWindow(103):
			transID = 103
			sourceID = 101
		elif getPoeditWindow(-31918):
			transID = -31918
			sourceID = 102
		elif getPoeditWindow(-31919):
			transID = -31919
			sourceID = 101
		else:
			return 0	# No text in translation.
		sourceText = getPoeditWindow(sourceID)
		translatedText = getPoeditWindow(transID)
		#Checking  of the equality in quantity of % variables, brackets and paragraph in source and translation. Unequal means error!
		parameter = {'{', '}', '[', ']', '%s', '%d', '%u', '%g', '\n', chr(13)}
		for i in parameter:
			if sourceText.count(i) != translatedText.count(i):
				return 4	#Either bold ornot, Error from perspective of translation rule.
		if self.isBold:
			return 1	# Error from language perspective.
		else:
			if sourceText == translatedText or sourceText.count("&") != translatedText.count("&"):	
				return 2	# It may or may not be an error. 
			else:
				return 3	# normal translation.

	def _get_name(self):
		type = self.category()
		global doBeep
		if getPoeditWindow(102):
			noticeText =_("Has plural form.")
		else:
			noticeText =""
		focusedMessage = super(PoeditListItem,self).name+": "+noticeText
		if doBeep:
			return "* "+focusedMessage if type < 3 else focusedMessage if type ==3 else "** "+focusedMessage
		else:
			return "** "+focusedMessage if type < 2 else "* " + focusedMessage if type ==2 else "** "+focusedMessage if type ==4 else focusedMessage

	def event_gainFocus(self):
		super(sysListView32.ListItem, self).event_gainFocus()
		type = self.category()
		global doBeep, sharpTone
		if type < 3 and doBeep: 
			pitch = 100*(2+(sharpTone+1)*(2-type))
			tones.beep(pitch, 50)
		elif type ==4:
			pitch = 300*(2+sharpTone+doBeep)
			tones.beep(pitch, 75)

	def script_toggleTranslation(self, gesture):
		type = self.category()
		reporting =[_("No text in translation."), _("erased Fuzzy label."), _("labelled as fuzzy."), _("labelled as fuzzy."), _("Error in translation")]
		# Translators: The toggle action performed by pressing control+u in poedit.
		gesture.send()
		ui.message(reporting[type])
	# Translators: The description of an NVDA command in toggling Poedit message status.
	script_toggleTranslation.__doc__ = _("Reports the status of message set by toggling in poedit.")


	__gestures = {
		"kb:control+u": "toggleTranslation",
	}

