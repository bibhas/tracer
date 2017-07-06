#renderlog.py
# 2016 Bibhas Acharya <mail@bibhas.com>

import os, sys, string, re, random
from collections import OrderedDict

SAMPLE_INPUT = "sample.log"

BASE_TEMPLATE = string.Template("""<!-- Rendered with DriverAPI-LogViewer -->
<html>
<head>
    <title>$title</title>
    <style>
      $styles
    </style>
    
    <script   src="https://code.jquery.com/jquery-1.12.4.min.js"   integrity="sha256-ZosEbRLbNQzLpnKIkEdrPv7lOy9C27hHQ+Xp8a4MxAQ="   crossorigin="anonymous"></script>
    
    <script>
      $script
    </script>
</head>
<body>
    $body
</body>
</html>""")

SCRIPT = """
    $(document).ready(function(){
        
        $('.detail').click(function(event) {
            
            $('.active').removeClass('active');
            
            $(this).addClass('active');
        });
    });
    
    $(window).keydown(function(e) {
        
        // Prevent default arrow key behavior
        
        e.preventDefault(); 
        
        var targetElement;
        
        // Handle down key
        
        if (e.keyCode == 40) {
            
            $targetElement = $('.active').next().next().next();
        }
        
        // Handle up key
        
        else if (e.keyCode == 38) {
            
            $targetElement = $('.active').prev().prev().prev();
        }
        
        if (!$targetElement.offset()) {
            
            return;
        }
        
        $('.active').removeClass('active');
        
        $targetElement.addClass('active');
        
        // Scroll element into view in 100ms
        
        $('html, body').animate({ scrollTop: $targetElement.offset().top - 10 }, 100);
    });"""

inCommentBlock = False

class LogEntry(object):
  
  class Source(object):
    
    def __init__(self, f, l):
      
      self.filename = f
      
      self.lineNumber = l
    
  class Argument:
    
    def __init__(self, i, v):
      
      self.identifier = i
      
      self.value = v
  
  class ReturnValue:
    
    def __init__(self, i, v):
      
      self.identifier = i
      
      self.value = v
      
  def __init__(self, repr):
    
    self.threadId = 0
    
    self.level = ""
    
    self.time = None
    
    self.source = None
    
    self.signature = ""
    
    self.arguments = []
    
    self.returnValues = []
    
    self.parse(repr)
  
  def parse(self, line):
    
    # Scan
    
    tokens = []
    
    for i in re.split("\[(THR)\]|\[(LVL)\]|\[(TIM)\]|\[(SRC)\]|\[(SIG)\]|\[(ARG)\]|\[(RET)\]", line):
      
      if i not in ["", None]:
      
        tokens.append(i)
        
    # Parse
    
    acc = OrderedDict()
    
    tokens.reverse() # prepping to pop
    
    while len(tokens) != 0:
      
      _key = tokens.pop()
      
      _value = tokens.pop()
      
      if _key == "THR":
        
        self.threadId = int(_value)
      
      elif _key == "LVL":
        
        self.level = _value
      
      elif _key == "TIM":
        
        self.time = _value
      
      elif _key == "SRC":
        
        v = _value.split("/")
        
        self.source = LogEntry.Source("/".join(v[:-1]), v[-1])
        
      elif _key == "SIG":
        
        self.signature = _value
      
      elif _key == "ARG":
        
        v = _value.split("=")
        
        try:
            self.arguments.append(LogEntry.Argument(v[0], v[1]))
        except:
            print v
      
      elif _key == "RET":
        
        v = _value.split("=")
        
        self.returnValues.append(LogEntry.ReturnValue(v[0], v[1]))

def HTML(startingTab=0):
    
    return {
        
        "STARTINDENT" : "&nbsp;" * startingTab,
        
        "TAB" : "&nbsp;&nbsp;&nbsp;&nbsp;",
        
        "NEWLINE" : "<br>",
        
        "ITALIC_START" : "<i><span style='color:#8c8c8c;word-wrap:break-word;display:inline-block;width:900px;'>",
        
        "ITALIC_END" : "</span></i>"
    }

def CONSOLE(startingTab=0):
    
    return {
        
        "STARTINDENT" : " " * startingTab,
        
        "TAB" : "    ",
        
        "NEWLINE" : "\n",
        
        "ITALIC_START" : "",
        
        "ITALIC_END" : "",
    }

def format_value(value, mode):
    
    buf = []
    
    indent = 0
    
    def new_line(_buf = buf):
        
        buf.append(mode["NEWLINE"])
        
        buf.append(mode["STARTINDENT"])
        
        for i in range(0, indent):
            
            buf.append(mode["TAB"])
    
    while True:
        
        _newValue = value.replace(", ", ",")
        
        if (value == _newValue):
            
            break
        
        value = _newValue
    
    i = 0
    
    global inCommentBlock;
    
    while i < len(value):
        
        c = value[i]
        
        if c == "{":
            
            buf.append(c)
            
            indent += 1
            
            new_line()
            
            new_line()
            
        elif c == "}":
            
            indent -= 1
            
            new_line()
            
            buf.append(c)
            
        elif c == "," and inCommentBlock == False:
            
            buf.append(c)
            
            new_line()
            
            new_line()
        
        elif c == "/" and (i + 1) < len(value) and value[i+1] == "*":
            
            i += 1
            
            buf.append(mode["ITALIC_START"])
            
            inCommentBlock = True
        
        elif c == "*" and (i + 1) < len(value) and value[i+1] == "/":
            
            i += 1
            
            buf.append(mode["ITALIC_END"])
            
            new_line()
            
            new_line()
            
            inCommentBlock = False
            
        else:
            
            buf.append(c)
        
        i += 1
            
    return "".join(buf)
    
def renderlog(inputFilename, destination=""):
  
  # Read sample log
  
  f = file(inputFilename, "r")
  
  c = f.read();
  
  f.close()
  
  # Prepare content
  
  logEntries = []
  
  for line in c.split("\n"):
    
    if line not in ["", None]:
      
      logEntries.append(LogEntry(line))
      
  # Render
  
  def render(filename, collapse=False):
    
    styles = ""
    
    body = ""
    
    index = 0
    
    for entry in logEntries:
        
      params = ""
      
      for arg in entry.arguments:
        
        params += "[arg]  %s = %s\n\n" % (arg.identifier, format_value(arg.value, CONSOLE(4)))
        
      for ret in entry.returnValues:
        
        params += "[ret] %s = %s\n\n" % (ret.identifier, format_value(ret.value, CONSOLE(4)))
        
      value = ""
      
      if collapse:
        
        value = string.Template("$index $content\n").substitute(
        
          index = "%i) " % index,
        
          content = entry.signature, 
        
          params = params
        )
      
      else:
        
        value = string.Template("$index $content\n$params\n").substitute(
        
          index = "%i) " % index,
        
          content = entry.signature, 
        
          params = params
        )
      
      body += value
      
      index += 1
      
    # Prepare html header
    
    f = open(filename, "w")
    
    f.writelines(body)
    
    f.close()
  
  render(os.path.join(destination, "render.txt"), False)