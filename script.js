let audio = document.getElementById("audio")
let audioBlob = null

function generateAudio(){

let text = document.getElementById("text").value
let voice = document.getElementById("voice").value
let speed = document.getElementById("speed").value

let formData = new FormData()

formData.append("text",text)
formData.append("voice",voice)
formData.append("speed",speed)

fetch("/speak",{
method:"POST",
body:formData
})

.then(response => response.blob())

.then(blob=>{
audioBlob = blob
audio.src = URL.createObjectURL(blob)
audio.play()
})

}

function pauseAudio(){
audio.pause()
}

function resumeAudio(){
audio.play()
}

function stopAudio(){
audio.pause()
audio.currentTime = 0
}

function clearText(){
document.getElementById("text").value=""
}

function downloadAudio(){

if(!audioBlob){
alert("Generate audio first")
return
}

let link=document.createElement("a")
link.href=URL.createObjectURL(audioBlob)
link.download="speech.wav"
link.click()

}