import logging


LOG = logging.getLogger(__name__)


def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    LOG.info(message)

    message.reply_channel.send({
        "text": message.content['text'],
    })
