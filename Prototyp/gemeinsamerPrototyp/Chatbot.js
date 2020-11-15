Antworten = ["Hallo mein Name ist Chatbot, wie kann ich Ihnen weiterhelfen?", "Weitere Informationen finden Sie in unserem FAQ.", "Bitte wiederholen Sie die Frage.", 
             "Der Kreis Wesel ist immer für Sie da."]

function send() {
    var Text = document.getElementById("ChatbotSendText").value;
    if (Text == "") return;
    document.getElementById("ChatbotSendText").value = "";
    var NewMessage = document.createElement("DIV");
    NewMessage.classList.add("ChatbotMessage", "UserMessage");
    NewMessage.innerHTML = Text;
    document.getElementById("ChatbotContent").appendChild(NewMessage);
    NewMessage.scrollIntoView();
    antwortBot();
}

function antwortBot(Antwort) {
    if (!Antwort) Antwort = Antworten[Math.floor(Math.random() * Antworten.length)]; 

    var NewMessage = document.createElement("DIV");
    NewMessage.classList.add("ChatbotMessage", "BotMessage");
    NewMessage.append(getWaitPoints());
    document.getElementById("ChatbotContent").appendChild(NewMessage);
    NewMessage.scrollIntoView();            
    setTimeout(function() {
        NewMessage.removeChild(NewMessage.lastChild);
        NewMessage.innerHTML = Antwort;
        NewMessage.scrollIntoView();            
    }, 1500);

}

function getWaitPoints() {
    var WaitPoints = document.createElement("DIV");
    WaitPoints.classList.add("ChatbotWaitPointWrapper");
    for (let i = 0; i < 3; i++) {
        let Point = document.createElement("DIV");
        Point.classList.add("ChatbotWaitPoint")
        WaitPoints.append(Point);     
   }
   return WaitPoints;
}