#addon/appModules/poedit.py
# Prepared by Him Prasad Gautam <drishtibachak@gmail.com>
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""App module for accessing  Poedit.
"""

from nvdaBuiltin.appModules import poedit
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
import nvwave

addonHandler.initTranslation()

doBeep = sharpTone = True
 
class AppModule(poedit.AppModule):

	def getPoeditObject(self, index):
		try:
			obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
				windowUtils.findDescendantWindow(api.getForegroundObject().windowHandle, visible=True,
				controlID=index), winUser.OBJID_CLIENT, 0)
		except LookupError:
			return None
		try:
			return obj.value
		except:
			return False

	def script_copyOriginalText(self, gesture):
		gesture.send()
		# Translators: The copying  of  source text to translation pressing control+b in poedit.
		ui.message(_("copied original text."))
	# Translators: The description of an NVDA command of copying message in Poedit.
	script_copyOriginalText.__doc__ = _("Reports about the copying act in poedit.")

	def script_deleteTranslation(self, gesture):
		if self.getPoeditObject(103):
			gesture.send()
			# Translators: The deletion  of  translation pressing control+k in poedit.
			ui.message(_("translation deleted."))
		else:
			# Translators: Report that No translation  text available to delete.
			ui.message(_("No text."))
	# Translators: The description of an NVDA command of deletion in Poedit.
	script_deleteTranslation.__doc__ = _("Reports about the deletion act in poedit.")

	def script_savePoFile(self, gesture):
		gesture.send()
		# Translators: The saving   of  currently focused    po file by   pressing control+s.
		ui.message(_("saving the po file..."))
	# Translators: The description of an NVDA command of saving  po  file.
	script_savePoFile.__doc__ = _("Reports while  saving the po  file.")

	def script_sayOriginalText(self, gesture):
		# Translators: The announcement  of  the source text on  pressing ctrl+shift+r.
		text = self.getPoeditObject(101)
		if text:
			ui.message(text)
		else:
			# Translator: Announcement  if the source text could not be read.
			ui.message(_("Could not read the source text"))
	# Translators: The description of an NVDA command for reporting source message in Poedit.
	script_sayOriginalText.__doc__ = _("Reports the source  message in poedit.")

	def script_sayTranslation(self, gesture):
		# Translators: The announcement  of  the translated text on  pressing ctrl+shift+t.
		text = self.getPoeditObject(103)
		if text:
			ui.message(text)
		else:
			# Translators: Report if  No translation   available to read.
			ui.message(_("No text."))
	# Translators: The description of an NVDA command for reporting translation message in Poedit.
	script_sayTranslation.__doc__ = _("Reports the translation  message in poedit.")

	def script_toggleBeep(self, gesture):
		global doBeep
		if doBeep:
			doBeep = False
			ui.message(_("Beep off"))
		else:
			doBeep = True
			ui.message(_("Beep on"))
	# Translators: An NVDA command for toggling a beep  in Poedit.
	script_toggleBeep.__doc__ = _("Toggles the beep mode and informs.")

	def script_setToneLevel(self, gesture):
		global sharpTone
		if sharpTone:
			sharpTone = False
			ui.message(_("set to  mild tone"))
		else:
			sharpTone = True
			ui.message(_("set to high  tone"))
	# Translators: An NVDA command for adjusting  a beep  volume.
	script_setToneLevel.__doc__ = _("sets the beep volume in mild  and sharp level in poedit.")

	def script_reportStatus(self,gesture):
		ui.message(api.getStatusBarText(api.getStatusBar()))
		# Translators: An NVDA command for getting  status of translation.
	script_reportStatus.__doc__ = _("Reports the current status of translation.")

	def script_guessError(self, gesture):
		if self.getPoeditObject(101) and self.getPoeditObject(103):
			sourceText = self.getPoeditObject(101)
			TransText = self.getPoeditObject(103)
		elif self.getPoeditObject(101) and self.getPoeditObject(-31919):
			sourceText = self.getPoeditObject(101)
			TransText = self.getPoeditObject(-31919)
		elif self.getPoeditObject(102) and self.getPoeditObject(-31918):
			sourceText = self.getPoeditObject(102)
			TransText = self.getPoeditObject(-31918)
		else:
			ui.message(_("No text."))
			return
		parameter = {'{': _("brace"), '}': _("brace"), '[': _("bracket"), ']': _("bracket"), '%s': '%s ', '%d': '%d ', '%u': '%u ', '%g': '%g ', '&': _("ampersand"), chr(13): _("paragraph")}
		for k in parameter.keys():
			if sourceText.count(k) != TransText.count(k):
				ui.message(parameter[k]+": "+_("Unequal  number in source and translation."))
				return
		ui.message(_("No error"))
		return
	script_guessError.__doc__ = _("Describes the cause of error.")


	__gestures = {
		"kb:control+b": "copyOriginalText",
		"kb:control+d": "reportStatus",
		"kb:control+s": "savePoFile",
		"kb:control+k": "deleteTranslation",
		"kb:control+shift+d": "reportStatus",
		"kb:control+shift+e": "guessError",
		"kb:control+shift+r": "sayOriginalText",
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
		# category 0: not translated, 1: fuzzy translation, 2: unsure translation, 3: normal translation, 4: Errorful translation. 
		translatedText = super(PoeditListItem,self)._getColumnContent(2)
		if translatedText: 
			# Finding out    the category of   the   translation.
			originalText = super(PoeditListItem,self)._getColumnContent(1)
			#Checking   of the equality in  quantity  of % variables, brackets and paragraph  in source and translation. Unequal means error!
			parameter = ['{', '}', '[', ']', '%s', '%d', '%u', '%g', '\n']
			for i in parameter:
				if originalText.count(i) != translatedText.count(i):
					return 4	#Either bold ornot, Error from perspective of translation rule.
			if self.isBold:
				return 1	# Error from language  perspective.
			else:
				if originalText == translatedText or originalText.count("&") != translatedText.count("&"):	
					return 2	# It may or may not be an error. 
				else:
					return 3	# normal translation.
		else:
			return 0	# No translation.

	def _get_name(self):
		type = self.category()
		focusedMessage = super(PoeditListItem,self).name
		global doBeep
		if doBeep:
			return "* "+focusedMessage if type < 2 else focusedMessage if type ==3 else "** "+focusedMessage
		else:
			return "** "+focusedMessage if type == 0 else "* " + focusedMessage if type ==1 else "** "+focusedMessage if type ==4 else focusedMessage

	def event_gainFocus(self):
		super(sysListView32.ListItem, self).event_gainFocus()
		type = self.category()
		global doBeep, sharpTone
		if type < 3 and doBeep: 
			pitch = 100*(2+(sharpTone+1)*(2-type))
			tones.beep(pitch, 50)
		elif type ==4:
			try:
				nvwave.playWaveFile("waves\\error.wav")
			except:
				tones.beep(1000,50)

	def script_toggleTranslation(self, gesture):
		type = self.category()
		reporting =[_("No text."), _("erased Fuzzy label."), _("labelled as fuzzy."), _("labelled as fuzzy."), _("Error in translation")]
		# Translators: The toggle action performed by pressing control+u in poedit.
		gesture.send()
		ui.message(reporting[type])
	# Translators: The description of an NVDA command in toggling Poedit message status.
	script_toggleTranslation.__doc__ = _("Reports the status  of message set by toggling in poedit.")


	__gestures = {
		"kb:control+u": "toggleTranslation",
	}

