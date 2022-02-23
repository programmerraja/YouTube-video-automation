const ffmpeg=require("fluent-ffmpeg")
const fs=require("fs")

var VideoEditor=new ffmpeg()

let vpath="/home/saravanan/program/python/andriod_automate/creator/videos/"
let mpath="/home/saravanan/program/python/andriod_automate/creator/music/"
let opath="/home/saravanan/program/python/andriod_automate/creator/output/"

let video=[]
let musics=[]
const SPEED=2

function getFlies(path,arr){
	return new Promise((res,rej)=>{
		fs.readdir(path,(err,files)=>{
			if(err){
				rej()
				console.log(err)
			}else{
				arr.push(...files)
				res()
			}

		})
	})
}	


function addAudio(aud){
  return VideoEditor.addInput(aud)
}

function mixVideoAudio(vid,aud,sec){
  let VideoEditor=new ffmpeg()
  console.log(vid,aud,sec)
  VideoEditor
  .addInput(vid)
  .videoFilter("setpts="+(1/SPEED)+"*PTS")
  .addInput(aud)
  .duration(sec)
	.saveToFile(opath+"myvideos.mp4","./temp")
	.on("end",()=>{
    console.log("end")
    fs.rename(vpath+video[0],vpath+"done/"+video[0],(err)=>{
      if(err){
        console.log("err while moving")
      }else{
        console.log("sucess")
      }
    })
   
  })
	.on("start",()=>{console.log("started")})
	.on("error",(err)=>{console.log("video error",err)})
	.on("progress",()=>{})

}

function getTime(file){

	return new Promise((res,rej)=>{
      ffmpeg.ffprobe(file,(err,meta)=>{
  		if(err){
  			console.log(err,"getTime")
  		}else{
        return res(meta.format.duration)
  		}
  	 })
  }); 
}

getFlies(vpath,video)
getFlies(mpath,musics).then(async ()=>{
        let music=[]
				
        music.push(musics[Math.floor(Math.random()*musics.length)])
				
        let vsec=parseInt(await getTime(vpath+video[0]))/SPEED
        let msec=await getTime(mpath+music[0])
        if(vsec>msec){
            console.log("need extra music")
            while(msec<=vsec){
              let temp=musics[Math.floor(Math.random()*musics.length)]
              msec+=await getTime(mpath+temp)
              music.push(temp)
            }
        }
        console.log(music)
        let temp_videoEditor;
        for(let i=0;i<music.length;i++){
          temp_videoEditor=addAudio(mpath+music[i])
        }

        let new_music=mpath+"merged.mp3"
        temp_videoEditor
        .mergeToFile(new_music,"./temp")
        .on("start",()=>{console.log("started music")})
        .on("error",(err)=>{console.log("music error",err)})
        .on("progress",()=>{})
        .on("end",()=>{
          console.log("music merged end")
          mixVideoAudio(vpath+video[0],new_music,vsec)
        })

	})


