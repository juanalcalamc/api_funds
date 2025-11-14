def send_notification(method: str, message: str):
    if method == "email":
        print(f" Email sent: {message}")
    elif method == "sms":
        print(f" SMS sent: {message}")
    else:
        print(f" Unknown notification method: {method}")