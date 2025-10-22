from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Message

main_bp = Blueprint('main', __name__)


@main_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201


@main_bp.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Мой Мессенджер</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: #f0f0f0;
        }
        #messages { 
            background: white;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ccc;
        }
        .message-input { 
            display: flex; 
            gap: 10px;
        }
        #message-input { 
            flex: 1; 
            padding: 12px; 
            border: 1px solid #ccc;
            border-radius: 20px;
            font-size: 16px;
        }
        button { 
            padding: 12px 20px; 
            background: #007bff;
            color: white;
            border: none;
            border-radius: 20px;
            font-size: 16px;
        }
        .message { 
            margin-bottom: 8px; 
            padding: 8px 12px;
            background: #e3f2fd;
            border-radius: 15px;
            word-wrap: break-word;
        }
        .system-message {
            color: #666;
            font-style: italic;
            font-size: 12px;
            text-align: center;
            margin: 5px 0;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
</head>
<body>
    <h2>🚀 Мой Мессенджер</h2>
    <div id="messages">
        <div class="system-message">💬 Чат загружен...</div>
    </div>
    <div class="message-input">
        <input type="text" id="message-input" placeholder="Введите сообщение..." onkeypress="handleKeyPress(event)">
        <button onclick="sendMessage()">Отправить</button>
    </div>

    <script>
        // Подключаемся к серверу
        var socket = io();
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        function sendMessage() {
            let messageInput = document.getElementById("message-input");
            let message = messageInput.value;
            
            if (message.trim() !== '') {
                console.log('Отправляю сообщение:', message);
                socket.emit('message', message);
                messageInput.value = '';
            }
        }
        
        // Получаем сообщения от сервера
        socket.on('new_message', function(data) {
            console.log('Получено сообщение:', data);
            addMessage(data.text);
        });
        
        // Старая версия на случай если new_message не работает
        socket.on('message', function(data) {
            console.log('Получено сообщение (старый метод):', data);
            addMessage(data);
        });

        socket.on('connect', function() {
            console.log('✅ Подключено к серверу');
            addSystemMessage('✅ Подключено к чату');
        });

        socket.on('disconnect', function() {
            console.log('❌ Отключено от сервера');
            addSystemMessage('❌ Потеряно соединение...');
        });

        function addMessage(text) {
            let messages = document.getElementById("messages");
            let div = document.createElement('div');
            div.className = 'message';
            div.textContent = text;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }

        function addSystemMessage(text) {
            let messages = document.getElementById("messages");
            let div = document.createElement('div');
            div.className = 'system-message';
            div.textContent = text;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }
    </script>
</body>
</html>
'''