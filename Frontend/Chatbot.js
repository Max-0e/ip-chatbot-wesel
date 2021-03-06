var BlockBot = false;
var FirstOpen = true;
var senderID;
const URL = "http://localhost:5005/webhooks/rest/webhook";


function uuid() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );  
}

function send() {
    var Text = document.getElementById("ChatbotSendText").value;
    if (Text == "" || BlockBot) return;
    BlockBot = true;
    document.getElementById("ChatbotSendText").value = "";
    var NewMessage = document.createElement("DIV");
    NewMessage.classList.add("ChatbotMessage", "UserMessage");
    NewMessage.innerHTML = Text;
    document.getElementById("ChatbotContent").appendChild(NewMessage);

    var BotMessage = document.createElement("DIV");
    BotMessage.classList.add("ChatbotMessage", "BotMessage");
    BotMessage.append(getWaitPoints());
    document.getElementById("ChatbotContent").appendChild(BotMessage);
    BotMessage.scrollIntoView();            
    $.ajax({
        url: URL,
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({"sender":senderID,  "message":Text}),
        success: function(result) {
            let tmpNode = document.getElementById("ChatbotContent").lastChild;
            tmpNode.removeChild(BotMessage.lastChild);
            console.log(result);
            let tmpArray = [];
            result.forEach(element => {
                for (let key in element) {
                    if(key == "text")
                        tmpArray.push(element[key]);
                    else if (key == "custom") {
                        if (element[key]["link"] && element[key]["linkname"])
                            tmpArray.push("<a class='BotMessageLink' href='" + element[key]["link"] + "' target='_blank'>" + element[key]["linkname"] + "</a>");
                    }
                    else if (key == "image")
                        tmpArray.push("<img style='width:100%' src='" + element[key] + "'/>");
                }
            });
            tmpNode.innerHTML = tmpArray.join("<br>");
            if (tmpNode.innerHTML == "")
                tmpNode.innerHTML = "Leider konnte ich nichts finden...";
            BlockBot = false;       
            tmpNode.scrollIntoView();    
        },
        error: function() {
            let tmpNode = document.getElementById("ChatbotContent").lastChild;
            tmpNode.removeChild(BotMessage.lastChild);
            tmpNode.innerHTML = "Ich kann Ihnen leider aktuell nicht weiter helfen.";
            tmpNode.scrollIntoView();     
            BlockBot = false;                  
        }
    });
}

function antwortBot(Antwort) { //Funktion für statische Antworten
    FirstOpen = false;
    var BotMessage = document.createElement("DIV");
    BotMessage.classList.add("ChatbotMessage", "BotMessage");
    BotMessage.append(getWaitPoints());
    document.getElementById("ChatbotContent").appendChild(BotMessage);
    BotMessage.scrollIntoView();            
    setTimeout(function() {
        BotMessage.removeChild(BotMessage.lastChild);
        BotMessage.innerHTML = Antwort;
        BotMessage.scrollIntoView();                      
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

function closeChatbot() {
    setTimeout(function() {
        $('.tap-target').tapTarget('close');
    }, 10);
}