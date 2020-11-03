Antworten = ["Hallo mein Name ist Chatbot, wie kann ich Ihnen weiterhelfen?", "Weitere Informationen finden Sie in unserem FAQ.", "Bitte wiederholen Sie die Frage.", 
             "Der Kreis Wesel ist immer für Sie da."]

function openChatbot() {
    document.getElementById("Chatbot").style.transform = "scale(1)";
}

function closeChatbot() {
    document.getElementById("Chatbot").style.transform = "scale(0)";
}

function send() {
    var Text = document.getElementById("ChatbotSendText").value;
    if (Text == "") return;
    document.getElementById("ChatbotSendText").value = "";
    var NewMessage = document.createElement("DIV");
    NewMessage.classList.add("ChatbotMessage", "UserMessage");
    NewMessage.innerHTML = Text;
    document.getElementById("ChatbotContent").appendChild(NewMessage);
    NewMessage.scrollIntoView();
    setTimeout(function() { antwortBot() }, 1000);
}

function antwortBot() {
    var Antwort = Antworten[Math.floor(Math.random() * Antworten.length)];
    var NewMessage = document.createElement("DIV");
    NewMessage.classList.add("ChatbotMessage", "BotMessage");
    NewMessage.innerHTML = Antwort;
    document.getElementById("ChatbotContent").appendChild(NewMessage);
    NewMessage.scrollIntoView();
}