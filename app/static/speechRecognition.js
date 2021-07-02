let generated_text = document.getElementById('generated-text')
let loader = document.getElementById('loader');

let url = "generate_text";


function transcript_iter(num, initial_transcript){
  loader.style = 'display:inline-block';
  let prompt_text = "";
  let transcript_json = {
    "final" : initial_transcript,
    "toremove" : prompt_text
  };
  while(num > 0){
    console.log(transcript_json)
    $.ajax({
      url: url,
      type: "POST",
      data: transcript_json,
      async: false,
      success: function(response) {
        console.log(response['generated_ls']);
        for (var t = 0; t < response['generated_ls'].length; t++) {
            generated_text.innerHTML += " " + response['generated_ls'][t];
//             window.onload=function(){
//               var msg = new SpeechSynthesisUtterance('Hello World');
//               window.speechSynthesis.speak();
//             }
            let prompt_words = response['generated_ls'][t].split(' ');
//             console.log(prompt_words);
            let new_words = prompt_words.splice(prompt_words.length - 3,prompt_words.length - 1);
//             console.log(new_words);
            prompt_text = new_words.join(' ')
            transcript_json["final"] = prompt_text;
            transcript_json["toremove"] = prompt_text;
            console.log(transcript_json["final"])
        }
        
      },
      error: function (jqXHR, textStatus, errorThrown) {
          console.log(jqXHR);
          console.log(textStatus);
          console.log(errorThrown);
      }
    });
    num--;
  }
  loader.style = 'display:none';
};


if ('webkitSpeechRecognition' in window) {
    let speechRecognition = new webkitSpeechRecognition();
    speechRecognition.continuous = true;
    speechRecognition.interimResults = true;
    speechRecognition.lang = 'en';

    // speechRecognition.lang = document.querySelector("#select_dialect").value;

    let final_transcript = '';
    let interim_transcript = '';
    console.log('Starting')
    speechRecognition.onstart = () => {
        document.querySelector("#status").style.display = "inline-block";
    };

    speechRecognition.onend = () => {
        document.querySelector("#status").style.display = "none";
    };

    speechRecognition.onError = () => {
        document.querySelector("#status").style.display = "none";
    };

    speechRecognition.onresult = (event) => {
        // Create the interim transcript string locally because we don't want it to persist like final transcript
        interim_transcript = "";

        for (let i = event.resultIndex; i < event.results.length; ++i) {
            // If the result item is Final, add it to Final Transcript, Else add it to Interim transcript
            if (event.results[i].isFinal) {
              final_transcript += event.results[i][0].transcript;
            } else {
              interim_transcript += event.results[i][0].transcript;
            }
        }

        document.querySelector("#final").innerHTML = final_transcript;
        document.querySelector("#interim").innerHTML = interim_transcript;
    };

    document.querySelector("#start").onclick = () => {
        speechRecognition.start();
    };
    
    document.querySelector("#stop").onclick = () => {
        speechRecognition.stop();
    };

    document.querySelector("#clear").onclick = () => {
        speechRecognition.stop();
        final_transcript = '';
        interim_transcript = '';
        document.getElementById("final").innerHTML = '';
        generated_text.innerHTML = '';
    };

    document.querySelector("#generate").onclick = () => {
        speechRecognition.stop();
        document.querySelector("#status").style.display = "none";
        console.log('generate button is clicked');
        console.log(`final transcript is ${final_transcript}`);


//         fetch(
//             url, {
//                 method: 'POST',
//                 body: JSON.stringify(transcript_json),
//                 headers: {
//                   "Content-Type":"application/json"
//                 }
//             }).then(response => {
//                 console.log(response);      
//                 return response.json();
//             }).then(data => {
//                 console.log(data);
//                 generated_text.innerHTML = "&emsp;" + data['generated_ls'][0];
//             }).catch(error => {
//               console.log(error);
//         });
      
        transcript_iter(3,final_transcript);
    };
    

}
else{
    console.log("Speech Recognition not Available")
}