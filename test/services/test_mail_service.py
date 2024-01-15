import os

from app.services.mail_service import MailService


def test_send_email(mocker):
    sender_email = "test_sender@gmail.com"
    password = "test_password"

    # Set the environment variables.
    os.environ["GMAIL_ADDRESS"] = sender_email
    os.environ["GMAIL_PASSWORD"] = password

    receiver_email = "test_receiver@gmail.com"
    subject = "Test Subject"
    body = "This is a test email."

    mock_smtp = mocker.patch("smtplib.SMTP")

    mail_service = MailService()
    mail_service.send_email(receiver_email, subject, body)

    mock_smtp.assert_called_once_with('smtp.gmail.com', 587)

    smtp_instance = mock_smtp.return_value
    assert smtp_instance.method_calls == [
        mocker.call.starttls(),
        mocker.call.login(sender_email, password),
        mocker.call.send_message(mocker.ANY),
        mocker.call.quit(),
    ]
