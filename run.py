from app import create_app, db, socketio

app = create_app()

# Инициализация БД при запуске
with app.app_context():
    db.create_all()
    print("✅ База данных создана!")

if __name__ == '__main__':
    print('🚀 Запуск мессенджера...')
    print('📱 Откройте в браузере: http://localhost:5000')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)