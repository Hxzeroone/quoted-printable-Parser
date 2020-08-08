from burp import IBurpExtender
from burp import IBurpExtenderCallbacks
from burp import ITab
from javax import swing
from java import awt
#partial script copied & tweaked from https://github.com/Meatballs1/burp_saml
import quopri
class BurpExtender(IBurpExtender, ITab):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context    = None
        callbacks.setExtensionName("quoted-printable Parser")
        self._jPanel = swing.JPanel()
        self._jPanel.setLayout(swing.BoxLayout(self._jPanel, swing.BoxLayout.Y_AXIS))
        self._jTextIn = swing.JTextArea("Input", 20,10)
        self._jTextIn.setLineWrap(True)
        self._jScrollPaneIn = swing.JScrollPane(self._jTextIn)
        self._jScrollPaneIn.setVerticalScrollBarPolicy(swing.JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
        self._jScrollPaneIn.setPreferredSize(awt.Dimension(20,10))
        self._jTextOut = swing.JTextArea("Output", 20,10)
        self._jTextOut.setLineWrap(True)
        self._jScrollPaneOut = swing.JScrollPane(self._jTextOut)
        self._jScrollPaneOut.setVerticalScrollBarPolicy(swing.JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
        self._jScrollPaneOut.setPreferredSize(awt.Dimension(20,10))
        self._jButtonPanel = swing.JPanel()
        self._jButtonDecode = swing.JButton('Decode', actionPerformed=self.decode)
        self._jButtonPanel.add(self._jButtonDecode)
        self._jPanel.add(self._jScrollPaneIn)
        self._jPanel.add(self._jButtonPanel)
        self._jPanel.add(self._jScrollPaneOut)
        callbacks.customizeUiComponent(self._jPanel)
        callbacks.addSuiteTab(self)
        return
    def getTabCaption(self):
        return "quoted-printable Parser"
    def getUiComponent(self):
        return self._jPanel
    def decode(self, button):
        mystring = self._jTextIn.getText()
        decoded_string = quopri.decodestring(mystring)
        decoded_string0 = decoded_string.decode('utf-8')
        Output = decoded_string0.replace("= ","")
        self._jTextOut.setText(str(Output))
