const ffmpeg=require("fluent-ffmpeg")
const fs=require("fs")

var VideoEditor=new ffmpeg()


let video=[]
let musics=[]

function getFlies(path,arr){
	return new Promise((res,rej)=>{
		fs.readdir(path,(err,files)=>{
			if(err){
				rej()
				console.log(err)
			}else{
				// console.log(files)
				arr.push(...files)
				res()
			}

		})
	})
}	

function addAudio(vid,aud,sec){
	VideoEditor
	.addInput(vid)
	.videoFilter("setpts=0.5*PTS")
	.addInput(aud)
	.duration(String(sec/2))
	.saveToFile("./output/ou.mp4","./temp")
	.on("end",()=>{console.log("end")})
	.on("start",()=>{console.log("started")})
	.on("error",(err)=>{console.log("error",err)})
	.on("progress",()=>{})
}

function getTime(vid,music){
	ffmpeg.ffprobe(vid,(err,meta)=>{
		if(err){
			console.log(err,"getTime")
		}else{
		addAudio(vid,music,meta.format.duration)
		}
	})
}

getFlies("./videos",video)
getFlies("./music",musics).then(()=>{
				let music=musics[Math.floor(Math.random()*musics.length)]
				getTime("./videos/"+video[0],"./music/"+music)
			})





