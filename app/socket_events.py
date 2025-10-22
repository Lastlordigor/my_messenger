def register_socket_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        print('✅ Клиент подключился')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('❌ Клиент отключился')

    @socketio.on('message')
    def handle_send_message(data):
        print(f'📨 Новое сообщение: {data}')

        # Отправляем всем подключенным клиентам
        socketio.emit('new_message', {'text': data})

        # Дублируем на старый event для совместимости
        socketio.emit('message', data)