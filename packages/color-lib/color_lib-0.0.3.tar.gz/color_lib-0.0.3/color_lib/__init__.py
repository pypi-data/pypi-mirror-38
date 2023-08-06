from colorama import init

class colors:
    reset = '\033[0m'
    
    @classmethod
    def init(self):
    	init()
    
    @classmethod
    def formatText(self, code, text):
        return '{0}{1}{2}'.format(code, text, self.reset)
    
    @classmethod
    def bold(self, text):
        return self.formatText('\033[01m', text)
    
    @classmethod
    def disable(self, text):
        return self.formatText('\033[02m', text)
    
    @classmethod
    def underline(self, text):
        return self.formatText('\033[04m', text)
    
    @classmethod
    def reverse(self, text):
        return self.formatText('\033[07m', text)
    
    @classmethod
    def strikethrough(self, text):
        return self.formatText('\033[09m', text)
    
    @classmethod
    def invisible(self, text):
        return self.formatText('\033[08m', text)
    
    class fg:
        reset = '\033[0m'
        
        @classmethod
        def formatText(self, code, text):
            return '{0}{1}{2}'.format(code, text, self.reset)
        
        @classmethod
        def black(self, text):
            return self.formatText('\033[30m', text)
        
        @classmethod
        def red(self, text):
            return self.formatText('\033[31m', text)
        
        @classmethod
        def green(self, text):
            return self.formatText('\033[32m', text)
        
        @classmethod
        def orange(self, text):
            return self.formatText('\033[33m', text)
        
        @classmethod
        def blue(self, text):
            return self.formatText('\033[34m', text)
        
        @classmethod
        def purple(self, text):
            return self.formatText('\033[35m', text)
        
        @classmethod
        def cyan(self, text):
            return self.formatText('\033[36m', text)
        
        @classmethod
        def lightgrey(self, text):
            return self.formatText('\033[37m', text)
        
        @classmethod
        def darkgrey(self, text):
            return self.formatText('\033[90m', text)
        
        @classmethod
        def lightred(self, text):
            return self.formatText('\033[91m', text)
        
        @classmethod
        def lightgreen(self, text):
            return self.formatText('\033[92m', text)
        
        @classmethod
        def yellow(self, text):
            return self.formatText('\033[93m', text)
        
        @classmethod
        def lightblue(self, text):
            return self.formatText('\033[94m', text)
        
        @classmethod
        def pink(self, text):
            return self.formatText('\033[95m', text)
        
        @classmethod
        def lightcyan(self, text):
            return self.formatText('\033[96m', text)
        
    class bg:
        reset = '\033[0m'
        
        @classmethod
        def formatText(self, code, text):
            return '{0}{1}{2}'.format(code, text, self.reset)
        
        @classmethod
        def black(self, text):
            return self.formatText('\033[40m', text)
        
        @classmethod
        def red(self, text):
            return self.formatText('\033[41m', text)
        
        @classmethod
        def green(self, text):
            return self.formatText('\033[42m', text)
        
        @classmethod
        def orange(self, text):
            return self.formatText('\033[43m', text)
        
        @classmethod
        def blue(self, text):
            return self.formatText('\033[44m', text)
        
        @classmethod
        def purple(self, text):
            return self.formatText('\033[45m', text)
        
        @classmethod
        def cyan(self, text):
            return self.formatText('\033[46m', text)
        
        @classmethod
        def lightgrey(self, text):
            return self.formatText('\033[47m', text)
