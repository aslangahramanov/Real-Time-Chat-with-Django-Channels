// STATE 

const messageScreen = document.getElementById('message-screen')
const submitButton = document.getElementById('submit-button')
const interestInput = document.getElementById("interest-input")
const userId = localStorage.getItem('user_id');
const onlineInfo = document.querySelector("#info .online") 
const writingInfo = document.querySelector("#info .writing") 
const personId = document.getElementById("person-id")
const onlineIcon = document.querySelector("#info i")
const findNewPerson = document.getElementById("find_new_person")
const messageInputDom = document.querySelector('#chat-message-input');
const messageSendButton = document.querySelector('#chat-message-submit')

const newChat = document.getElementById('new-chat')
const exitChat = document.getElementById('exit-chat')


const imageSelectInput = document.getElementById("image-select")
const imageSelectButton = document.getElementById("chat-image-select")
const selectedImageDiv = document.getElementById('selected-image');



function changeInputValue(){
    if (messageInputDom.value !== ""){
        writingMessageHandler()
    }
    else{
        endingMessageHandler()
    }
}



function endingMessageHandler() {

    chatSocket.send(JSON.stringify({
        'action_type': 'writing_end',
        'user_id': userId
    }));

}



function writingMessageHandler() {
    chatSocket.send(JSON.stringify({
        'action_type': 'writing_start',
        'user_id': userId
    }));

}




setTimeout(() => {
    endingMessageHandler();
}, 1000);


const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
);




window.addEventListener('DOMContentLoaded', (event) => {
if (!userId) {
    const newUserId = generateUserId();
    localStorage.setItem('user_id', newUserId);
}

personId.value = localStorage.getItem("user_id")


chatSocket.onopen = function(event) {
    chatSocket.send(JSON.stringify({
        'action_type': 'insert_app',
        'user_id': userId
    }));
};



submitButton.addEventListener('click', () => {
    localStorage.setItem('interest', interestInput.value)
    chatSocket.send(JSON.stringify({
        'action_type': 'match_persons',
        'person_interest': interestInput.value,
        'user_id': userId
    })
    )
    openModel()
});


if (newChat) {
    newChat.addEventListener('click', () => {
        interest = localStorage.getItem("interest")
        console.log(interest);
        console.log(userId);
        chatSocket.send(JSON.stringify({
            'action_type': 'rematch_persons',
            'person_interest': interest,
            'user_id': userId
        })
        )
        findNewPerson.style.display = 'none'
        messageSendButton.disabled = false
        imageSelectButton.disabled = false
        messageScreen.innerHTML = ""
    })
}




document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        messageSendButton.click();
    }
}


chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const type = data.type;

    if (type === 'writing_status') {
        updateOnlineStatus(true)
        const writing = data.writing;
        const user_id = data.user_id;

        if (writing && user_id !== userId) {
            onlineInfo.style.display = "none";
            writingInfo.style.display = "block";
        } else {
            writingInfo.style.display = "none";
            onlineInfo.style.display = "block";
        }
    } else if (type === 'send_message') {
        updateOnlineStatus(true)
        const message = data.message;
        const sender = data.sender;
        if (message) {
            const messageBox = document.createElement('div');
            messageBox.className = sender === userId ? 'my-side message-box' : 'opponent message-box';
            messageBox.innerHTML = `<p class="text">${message}</p>`;

            messageScreen.appendChild(messageBox);
            messageScreen.scrollTop = messageScreen.scrollHeight;
            messageInputDom.value = "";
            endingMessageHandler();
        }
    } else if (type === 'send_image') {
        updateOnlineStatus(true)
        const imageUrl = data.image_url;
        const sender = data.sender;
        if (imageUrl) {
            const imageBox = document.createElement('div');
            imageBox.className = sender === userId ? 'my-side message-box' : 'opponent message-box';
            imageBox.innerHTML = `<img style="width:100%; height:100%;" src="${imageUrl}" alt="">`;

            messageScreen.appendChild(imageBox);
            messageScreen.scrollTop = messageScreen.scrollHeight;
            messageInputDom.value = "";
            endingMessageHandler();
        }
    } else if (type === 'offline') {
        const user_id = data.user_id;
        const offline = data.offline;
        if (offline && user_id !== userId) {
            updateOnlineStatus(false)
            chatSocket.send(JSON.stringify({
                'action_type': 'discard_room',
                'user_id': userId
            }));
        }
    } else if (type === 'online') {
        const user_id = data.user_id;
        const online = data.online;
        if (online) {
            updateOnlineStatus(true)
        }
    }
};



function updateOnlineStatus(isOnline) {
    if (isOnline) {
        onlineInfo.textContent = 'Online';
            onlineIcon.style.color = 'green';
            messageScreen.style.overflow = 'auto';
            findNewPerson.style.display = 'none';
            messageSendButton.disabled = false;
            imageSelectButton.disabled = false;
    } else {
        onlineInfo.textContent = 'Offline';
        onlineIcon.style.color = 'grey';
        messageScreen.style.overflow = 'hidden';
        findNewPerson.style.display = 'flex';
        messageSendButton.disabled = true;
        imageSelectButton.disabled = true;
    }
}


messageSendButton.onclick = function(e) {
    const message = messageInputDom.value;
    if (message) {
        chatSocket.send(JSON.stringify({
            'action_type': 'on_chat',
            'message': message,
            'user_id': userId
        }));
    }
};



const chat = document.getElementById("chat")

function openModel(){
    if (chat) {
        chat.style.visibility = 'visible'
        chat.style.opacity = '1'
    }
}

function generateUserId() {
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}




})









imageSelectButton.addEventListener("click", () => {
    imageSelectInput.click()
})




imageSelectInput.addEventListener('change', function(event) {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
        const reader = new FileReader();

        reader.onload = function(event) {
            const imageUrl = event.target.result;
            chatSocket.send(JSON.stringify({
                'action_type': 'send_image',
                'image_url': imageUrl,
                'user_id': userId
            }));
        };

        reader.readAsDataURL(selectedFile)
    }
});