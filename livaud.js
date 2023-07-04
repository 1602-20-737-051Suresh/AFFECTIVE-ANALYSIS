// get references to the HTML elements
const recordBtn = document.getElementById('record-btn');
const stopBtn = document.getElementById('stop-btn');
const playBtn = document.getElementById('play-btn');
const audioElem = document.getElementById('audio');

// create an instance of the AudioContext
const audioCtx = new AudioContext();

// create a MediaStreamSource node to capture audio from the microphone
let mediaStreamSource = null;
navigator.mediaDevices.getUserMedia({ audio: true })
  .then((stream) => {
    mediaStreamSource = audioCtx.createMediaStreamSource(stream);
  })
  .catch((err) => {
    console.error('getUserMedia error:', err);
  });

// create a ScriptProcessorNode to process the audio data
const bufferSize = 4096;
let audioData = [];
const scriptProcessor = audioCtx.createScriptProcessor(bufferSize, 1, 1);
scriptProcessor.onaudioprocess = (event) => {
  // get the input buffer
  const inputBuffer = event.inputBuffer.getChannelData(0);
  // push the input buffer to the audio data array
  audioData.push(new Float32Array(inputBuffer));
};

// connect the nodes to the audio context
mediaStreamSource.connect(scriptProcessor);
scriptProcessor.connect(audioCtx.destination);

// add event listeners to start and stop the audio recording
recordBtn.addEventListener('click', () => {
  audioData = [];
  scriptProcessor.connect(audioCtx.destination);
});
stopBtn.addEventListener('click', () => {
  scriptProcessor.disconnect(audioCtx.destination);
});

// add event listener to play the recorded audio
playBtn.addEventListener('click', () => {
  // create a new AudioBuffer from the recorded audio data
  const audioBuffer = audioCtx.createBuffer(1, audioData.length * bufferSize, audioCtx.sampleRate);
  for (let i = 0; i < audioData.length; i++) {
    audioBuffer.getChannelData(0).set(audioData[i], i * bufferSize);
  }
  // set the AudioBuffer as the source of the audio element and play it
  audioElem.src = URL.createObjectURL(new Blob([audioBuffer.getChannelData(0)], { type: 'audio/wav' }));
  audioElem.play();
});
