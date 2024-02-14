class LogMessage(str):
    @classmethod
    def sent_msg2admin(cls, message: object) -> str:
        return f"send_admin ({message.from_user.id}), {message.from_user.full_name}"

    @classmethod
    def err_send_all(cls, err: Exception) -> str:
        return f"error during send_all. {err}"