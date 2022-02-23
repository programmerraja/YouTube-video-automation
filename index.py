from ppadb.client import Client 
import subprocess
import time,os,math

client=Client()
lenevo=client.device("a8dd6a2c")


no_of_line_css=0
# lenevo.shell("input keyevent KEYCODE_DPAD_DOWN")
# exit(1)
def moveToHtml():
  html_location={"x":193,"y":331}
  lenevo.shell("input tap "+str(html_location["x"])+" "+str(html_location["y"]))
  # time.sleep(0.5)

def moveToCss():
  css_location={"x":393,"y":331}
  lenevo.shell("input tap "+str(css_location["x"])+" "+str(css_location["y"]))
  # time.sleep(0.5)

def moveToJs():
  js_location={"x":648,"y":331}
  lenevo.shell("input tap "+str(js_location["x"])+" "+str(js_location["y"]))
  # time.sleep(0.5) 

def moveToOutput():
  output_location={"x":956,"y":331}
  lenevo.shell("input tap "+str(output_location["x"])+" "+str(output_location["y"]))
  time.sleep(4) 

def writeText(text):
  if("\ba" in text):
    lenevo.shell("input keyevent KEYCODE_DEL")
  text=text.replace("\ba" ,"")
  lenevo.shell("input text \""+text+"\"")
 
def styleParser(style):
  style=style.replace(";","")
  style=style.replace("}","")
  style=style.replace("","")
  style=style.replace("\t","")
  return style

def cleanCss(css):
  temp_css=[]
  for i in css:
    if(len(i)>0):
      temp_css.append(i)
  return temp_css

def writeCss(css,showOutput=True):
  moveToCss()
  count=1
  css=styleParser(css)  
  css=cleanCss(css.split("\n"))
  for i in css:
     writeText(i.replace("\t","  "))
     # this for css prop()
     if("(" in i):
      c=i.count("(")
      lenevo.shell("input keyevent KEYCODE_MOVE_END")
      lenevo.shell("input keyevent KEYCODE_DPAD_LEFT")
      while(c):
       lenevo.shell("input keyevent KEYCODE_DEL")
       c-=1
      # writeText(";")
      # for :: bfore and aftr
     if("::" in i):
       lenevo.shell("input keyevent KEYCODE_MOVE_END")
       lenevo.shell("input keyevent KEYCODE_DEL")
       lenevo.shell("input keyevent KEYCODE_DEL")
       lenevo.shell("input keyevent KEYCODE_DPAD_LEFT")

     if(":hover" in i):
       lenevo.shell("input keyevent KEYCODE_MOVE_END")
       lenevo.shell("input keyevent KEYCODE_DEL")
     if(":nth-child" in i):
       lenevo.shell("input keyevent KEYCODE_MOVE_END")
       lenevo.shell("input keyevent KEYCODE_DEL")
       lenevo.shell("input keyevent KEYCODE_DPAD_LEFT")
       lenevo.shell("input keyevent KEYCODE_ENTER ")
     # for content:""
     if("content:''" in i):
      lenevo.shell("input keyevent KEYCODE_MOVE_END")
      lenevo.shell("input keyevent KEYCODE_DPAD_LEFT")
      lenevo.shell("input keyevent KEYCODE_DEL")
      lenevo.shell("input keyevent KEYCODE_DEL")

     # for props; enter
     if(count!=len(css) and "{" not in i):
      lenevo.shell("input keyevent KEYCODE_MOVE_END")
      writeText("\n")
     
     # for name{ to press enter here}
     if("{" in i and "nth-child" not in i):
      writeText("\n")
     count+=1
  lenevo.shell("input keyevent KEYCODE_DPAD_DOWN")
  lenevo.shell("input keyevent KEYCODE_ENTER")
  if(showOutput):
    moveToOutput()

def writeCssAnimation(css):
  moveToCss()
  count=1
  css=css.replace(";","")
  css=cleanCss(css.split("\n"))
  for i in css:

      writeText(i.replace("\t","  "))
      lenevo.shell("input keyevent KEYCODE_MOVE_END")
      
      if("(" in i):
       c=i.count("(")+1
       while (c):
         lenevo.shell("input keyevent KEYCODE_DEL")
         c-=1
       writeText(";")
       writeText("\n")

      
      if("{" in i):
        lenevo.shell("input keyevent KEYCODE_DEL")

      # if(not is_start and "{" not in i):
        # lenevo.shell("input keyevent KEYCODE_MOVE_END")
        # writeText("\n")
    
       # for props; enter
      if(count==1 and "{" in i):
        lenevo.shell("input keyevent KEYCODE_MOVE_END")
        writeText("\n")
       
       # for name{ to press enter here}
      if("{" in i  and  count>1):
        writeText("\n")
      count+=1
  
  lenevo.shell("input keyevent KEYCODE_ENTER")
   
  moveToOutput()

def writeHTML(html):
  html=html.replace("\"","'")
  for i in html.split("\n"):
    writeText(i.replace("\t","  "))
    if("'" in i):
      c=math.ceil(i.count("'"))
      # print(c,i.count("'"))
      lenevo.shell("input keyevent KEYCODE_MOVE_END")
      while(c):
       lenevo.shell("input keyevent KEYCODE_DEL")
       c-=1
    writeText("\n")  
  moveToOutput()  

def videoStart():
  camera={"x":1034,"y":1030}
  lenevo.shell("input tap "+str(camera["x"])+" "+str(camera["y"]))
  camera_start={"x":981,"y":870}
  lenevo.shell("input tap "+str(camera_start["x"])+" "+str(camera_start["y"]))

def videoStop():
  camera={"x":1034,"y":1030}
  lenevo.shell("input tap "+str(camera["x"])+" "+str(camera["y"]))
  camera_stop={"x":892,"y":951}
  lenevo.shell("input tap "+str(camera_stop["x"])+" "+str(camera_stop["y"]))
  print("Video recoreded sucessfully")

def editVideo():
  cmd=["node /home/saravanan/program/python/andriod_automate/creator/index.js"]
  process=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
  process.wait()
  for line in process.stdout:
    print(line)

def getVideoToSys():
  from_path="/storage/emulated/0/ADVScreenRecorder/";
  to_path="/home/saravanan/program/python/andriod_automate/creator/videos/"
  files=lenevo.shell("ls -t "+from_path)
  file_name=files.split(" ")[0]
  to_path+=file_name
  from_path+=file_name
  print(lenevo.pull(from_path,to_path),"video moved to sys")
  editVideo()

def putVideoToMobile():
  to_path="/storage/emulated/0/Youtube/";
  from_path="/home/saravanan/program/python/andriod_automate/creator/output/"
  files=os.listdir(from_path)
  print(files)
  file_name=files[1]
  from_path+=file_name
  print("enter the file name:")
  tfile_name=input()
  to_path+=tfile_name+".mp4"
  print(lenevo.push(from_path,to_path),"video moved to android")
  os.rename(from_path,"/home/saravanan/program/python/andriod_automate/creator/output/"+file_name)


html="""<div class="container">
\t<div class="head">
\t\t<div class="horn"></div>
<div class="horn1"></div>
<div class="eye">
<div class="eyeball"></div>
</div>
<div class="eye1">
<div class="eyeball1"></div>
\ba</div>
<div class="mouth">
<div class="nose"></div>
<div class="nose1"></div>
<div class="smile"></div>
</div>
</div>"""

# writeCss(""".toggle.active span:nth-child(1) {
# width: 150px;
# transform: translateY(0) rotate(405deg);}""")
# exit(0)

# js="""<script>
# const menu = document.querySelector('.toggle')
# menu.onclick = function () {
#    menu.classList.toggle('active')  
# }
# .</script>"""

videoStart()
writeHTML(html)

# moveToHtml()
# lenevo.shell("input keyevent KEYCODE_DPAD_DOWN")
# lenevo.shell("input keyevent KEYCODE_DPAD_DOWN")
# lenevo.shell("input keyevent KEYCODE_ENTER")
# writeText(js)  
# lenevo.shell("input keyevent KEYCODE_MOVE_END")
# c=3
# while(c):
#   lenevo.shell("input keyevent KEYCODE_DEL")
#   c-=1
# lenevo.shell("input keyevent KEYCODE_DPAD_DOWN")
# c=7
# while(c):
#   lenevo.shell("input keyevent KEYCODE_DEL")
#   c-=1
# time.sleep(2)

css=""".container{
height:581px;
width:360px;
display:flex;
align-items:center;
justify-content:center;
text-align:center ;
position:relative ;
overflow:hidden ;
background-color:none;
}
splitme
.head{
width: 150px;
height: 200px;
background-color:#ffeae0;
position:absolute;
left:110px;
top:80px;
z-index:999;
border-radius:84% 81% 60% 49% / 89% 84% 30% 30% ;
animation:shake 0.5s infinite ;
}
splitme
.head::after{
content:'';
position:absolute;
width:20px;
height:110px;
border-radius:50%;
background-color:#ffeae0;
top:65px;
left:-3px;
transform:rotate(3deg);
}
splitme
.head::before{
content:'';
position:absolute;
width:20px;
height:110px;
border-radius:50%;
background-color:#ffeae0;
top:65px;
right:-3px;
transform:rotate(-3deg);
}
splitme
.mouth{
width: 157px;
height: 60px;
background-color:#fcaeae;
border-bottom-left-radius:45px;
border-bottom-right-radius:48px; 
border-bottom: 0;
position:absolute;
left:-3.5px;
top:140px;
z-index:99;
}
splitme
.mouth::after{
content:'';
position:absolute;
width:157px;
height:40px;
background-color:#fcaeae;
border-radius:50%;
left:0;
bottom:40px;
transform:rotate(-.5deg);
}
splitme
.mouth::before{
content:'';
position:absolute;
width:100px;
height:20px;
background-color:#fcaeae;
border-radius:50%;
left:25px;
top:43.8px;
transform:rotate(1deg);
}
splitme
.eye{
height:23px;
width:18px;
background-color:black;
border-radius:50%;
position:absolute;
left:47px;
top:75px;
}
splitme
.eye1{
height:23px;
width:18px;
background-color:black;
border-radius:50%;
position:absolute;
right:47px;
top:75px;
}
splitme
.eyeball{
height:6.5px;
width:6px;
background-color:white;
border-radius:50%;
position:absolute;
top:5px;
right:2px;
}
splitme
.eyeball1{
height:6.5px;
width:6px;
background-color:white;
border-radius:50%;
position:absolute;
top:5px;
left:2px;
}
splitme
.nose{
height:15px;
width:25px;
background-color:#c26e6e;
border-radius:50%;
position:absolute;
top:2px;
left:25px;
z-index:999;
transform:rotate(10deg);
}
splitme
.nose1{
height:15px;
width:25px;
background-color:#c26e6e;
border-radius:50%;
position:absolute;
top:2px;
right:25px;
z-index:999;
transform:rotate(-10deg);
}
splitme
.smile{
height: 20px;
width: 20px;
border: 5px solid transparent;
border-top: 5px solid #c26e6e;
border-radius: 50%;
position: absolute;
top:20px;
right:40px;
z-index:999;
transform:rotate(130deg);
}
splitme
.smile::before{
content:'';
width: 5px;
height: 5px;
background-color:#c26e6e;
border-top-left-radius:5px;
border-top-right-radius:5px; 
border-bottom: 0;
position:absolute;
top:-1px;
left:-2px;
z-index:9999;
transform:rotate(-130deg);
}
splitme
.smile::after{
content:'';
width: 5px;
height: 5px;
background-color:#c26e6e;
border-top-left-radius:5px;
border-top-right-radius:5px; 
border-bottom: 0;
position:absolute;
top:-.5px;
right:-2px;
z-index:9999;
transform:rotate(-220deg);
}
splitme
.horn{
height:15px;  
width:15px;
background-color:#ffaf03;
border-radius:52% 48% 0% 71% / 100% 100% 0% 0% ;
position:absolute ;
left:30px;
top:-2px;
transform:rotate(-35deg);
}
splitme 
.horn1{
height:15px;  
width:15px;
background-color:#ffaf03;
border-radius:52% 48% 0% 71% / 100% 100% 0% 0%   ;
position:absolute ;
right:30px;
top:-3px;
transform:rotate(34deg);
}"""
for c in css.split("splitme"):
  if("*{" in c or ".circle" in c):
    writeCss(c,False)
  else:
    writeCss(c)

# css="""button {
# height: 4em;
# width: 7em;
# background: #444;
# background: linear-gradient(top, #555, #333);
  # border: none;
# border-top: 3px solid orange;
# border-radius: 0 0 0.2em 0.2em;
# color: #fff;
# font-size: 1em;
# animation: wiggle 2s linear infinite;}"""

# # writeCss(css)

css="""@keyframes shake {
0% { 
  transform: translate(1px, 1px) rotate(0deg);
}10% { 
  transform: translate(-1px, -2px) rotate(-1deg); 
}20% {
  transform: translate(-3px, 0px) rotate(1deg); 
}30% { 
  transform: translate(3px, 2px) rotate(0deg);
}40% { 
  transform: translate(1px, -1px) rotate(1deg); 
}50% { 
  transform: translate(-1px, 2px) rotate(-1deg); 
}60% {   
  transform: translate(-3px, 1px) rotate(0deg); 
}70% {   
  transform: translate(3px, 1px) rotate(-1deg); 
}80% {   
  transform: translate(-1px, -1px) rotate(1deg); 
}90% {   
  transform: translate(1px, 2px) rotate(0deg); 
}100% {  
  transform: translate(1px, -2px) rotate(-1deg); 
}}"""
# moveToJs()
# js=""""""

for c in css.split("splitme"):
  writeCssAnimation(c)

time.sleep(5)
videoStop()

getVideoToSys()
putVideoToMobile()

