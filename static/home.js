// STATE 

const messageScreen = document.getElementById('message-screen')
const submitButton = document.getElementById('submit-button')
const interestInput = document.getElementById("interest-input")




const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
);


chatSocket.onmessage = function(event) {
// Gelen mesajı işle
};


chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

window.addEventListener('DOMContentLoaded', (event) => {
const userId = localStorage.getItem('user_id');
if (!userId) {
    // Kullanıcı kimliği local storage'a kaydet
    const newUserId = generateUserId(); // Örneğin rastgele bir fonksiyonla kimlik oluşturabilirsiniz
    localStorage.setItem('user_id', newUserId);
    uniqueId.value = newUserId
}


chatSocket.onopen = function(event) {
    chatSocket.send(JSON.stringify({
        'action_type': 'insert_app',
        'user_id': userId
    }));
};


submitButton.addEventListener('click', () => {
    chatSocket.send(JSON.stringify({
        'action_type': 'match_persons',
        'person_interest': interestInput.value,
        'user_id': userId
    }))
    openModel()
    chatSocket.onopen = function(event) {
        chatSocket.send(JSON.stringify({
            'action_type': 'insert_chat',
            'user_id': userId
        }));
    };


    


    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
};


    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        if (message){
            chatSocket.send(JSON.stringify({
                'action_type': 'on_chat',
                'message': message,
                'user_id': userId
            }));
            messageInputDom.value = '';
        }

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);

            const message = data.message;
            const sender = data.sender;

            const messageBox = document.createElement('div');
            messageBox.className = sender === userId ? 'my-side message-box' : 'opponent message-box';
            messageBox.innerHTML = `<p class="text">${message}</p>`;

            messageScreen.appendChild(messageBox);
            messageScreen.scrollTop = messageScreen.scrollHeight;
            };
    };
})
});


const chat = document.getElementById("chat")

function openModel(){
    if (chat) {
        chat.style.visibility = 'visible'
        chat.style.opacity = '1'

        const userId = localStorage.getItem('user_id');

        
    }
}

function generateUserId() {
// Burada rastgele bir kullanıcı kimliği oluşturabilirsiniz
// Örnek olarak:
return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}