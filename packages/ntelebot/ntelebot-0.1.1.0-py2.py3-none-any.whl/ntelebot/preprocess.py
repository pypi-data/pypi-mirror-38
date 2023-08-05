"""Non-universal, but fairly versatile update preprocessor."""

from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import cgi

import ntelebot


class Preprocessor(object):  # pylint: disable=too-few-public-methods
    """Non-universal, but fairly versatile update preprocessor."""

    def __init__(self):
        self.conversations = {}
        self.bots = {}

    def __call__(self, bot, update):  # pylint: disable=too-many-branches,too-many-statements
        """Convert a Telegram Update instance into a normalized Context."""

        bot_info = self.bots.get(bot.token)
        if not bot_info:
            self.bots[bot.token] = bot_info = bot.get_me()

        ctx = Context(self.conversations, bot, bot_info)

        if update.get('message') and update['message'].get('new_chat_members'):
            payload = update['message']
            ctx.type = 'join'
            ctx.user = payload['from']
            ctx.chat = payload['chat']
            ctx.reply_id = payload['message_id']
            ctx.data = payload['new_chat_members']
            return ctx

        if update.get('message') and update['message'].get('pinned_message'):
            payload = update['message']
            ctx.type = 'pin'
            ctx.user = payload['from']
            ctx.chat = payload['chat']
            ctx.reply_id = payload['message_id']
            ctx.data = payload['pinned_message']
            return ctx

        if update.get('message'):
            payload = update['message']
            ctx.type = 'message'
            ctx.user = payload['from']
            ctx.chat = payload['chat']
            ctx.reply_id = payload['message_id']

            text = payload.get('text', '')
            if payload.get('forward_from'):
                text = ''
                ctx.forward_from = payload['forward_from']['id']
            elif payload.get('reply_to_message'):
                ctx.reply_from = payload['reply_to_message']['from']['id']

            if (text.startswith('/start ') or
                    text.startswith('/start@%s ' % bot_info['username'].lower())):
                text = text.split(None, 1)[1]
            if not text.startswith('/'):
                tmp = decode(text)
                if tmp.startswith('/'):
                    text = tmp
            if ctx.chat['type'] == 'private':
                prev_text = self.conversations.pop(ctx.user['id'], None)
                if not text.startswith('/') and prev_text:
                    text = text and '%s %s' % (prev_text, text) or prev_text
            if text != payload.get('text', ''):
                payload['entities'] = []
            ctx.command, ctx.text = get_command(text, bot_info['username'])
            ctx.prefix = ctx.text.partition(' ')[0]

            if payload.get('sticker'):
                ctx.sticker = payload['sticker']['file_id']

            if payload.get('photo'):
                size = 0
                for photo in payload['photo']:
                    if size < photo['height'] * photo['width']:
                        size = photo['height'] * photo['width']
                        ctx.photo = photo['file_id']

            return ctx

        if update.get('callback_query'):
            payload = update['callback_query']
            ctx.type = 'callback_query'
            ctx.user = payload['from']
            ctx.chat = payload['message']['chat']
            ctx.edit_id = payload['message']['message_id']
            text = ntelebot.keyboardutil.decode(payload['message'], payload['data'])
            ctx.command, ctx.text = get_command(text, bot_info['username'])
            ctx.prefix = ctx.text.partition(' ')[0]
            return ctx

        if update.get('inline_query'):
            payload = update['inline_query']
            ctx.type = 'inline_query'
            ctx.user = payload['from']
            ctx.answer_id = payload['id']
            ctx.text = payload['query']
            ctx.prefix = ctx.text.partition(' ')[0]
            return ctx


class Context(object):
    """Normalized presentation of an incoming message or event.

    This primarily standardizes how the payload text is found (update.message.text,
    update.callback_query.data, update.inline_query.query, etc.) and how replies are sent
    (update.message.reply_text, update.callback_query.message.edit_message_text, bot.send_message,
    bot.answer_inline_query, etc.).
    """

    # pylint: disable=too-many-instance-attributes
    private = False
    type = user = chat = text = prefix = command = data = None
    forward_from = reply_from = None
    sticker = photo = None
    reply_id = edit_id = answer_id = None

    def __init__(self, conversations, bot, bot_info):
        self._conversations = conversations
        self.bot = bot
        self.bot_info = bot_info

    def encode_link(self, command, text=None):
        """Generate an HTML fragment that links to a deeplink back to the bot."""

        # pylint: disable=deprecated-method
        return '<a href="%s">%s</a>' % (cgi.escape(self.encode_url(command), True), text or command)

    def encode_url(self, command):
        """Generate a deeplink URL."""

        return 'https://t.me/%s?start=%s' % (self.bot_info['username'], encode(command))

    def reply_html(self, text, *args, **kwargs):
        """Reply or edit the context's message with the given HTML fragment."""

        kwargs.setdefault('parse_mode', 'HTML')
        return self.reply_text(text, *args, **kwargs)

    def reply_inline(self, results, **kwargs):
        """Reply or edit the context's message with the given result list."""

        if self.answer_id:
            return self.bot.answer_inline_query(
                inline_query_id=self.answer_id, results=results, **kwargs)

    def reply_markdown(self, text, *args, **kwargs):
        """Reply or edit the context's message with the given Markdown fragment."""

        kwargs.setdefault('parse_mode', 'Markdown')
        return self.reply_text(text, *args, **kwargs)

    def reply_text(self, text, *args, **kwargs):
        """Reply or edit the context's message with the given text."""

        if args:
            text %= args

        if (kwargs.get('parse_mode') == 'HTML' and kwargs.get('reply_markup') and
                kwargs['reply_markup'].get('inline_keyboard')):
            text_prefix = ntelebot.keyboardutil.fix(kwargs['reply_markup']['inline_keyboard'])
            if text_prefix:
                text = text_prefix + text

        if self.reply_id:
            if text.startswith('photo:') and ' ' not in text:
                method = self.bot.send_photo
                kwargs['photo'] = text[len('photo:'):]
            elif text.startswith('sticker:') and ' ' not in text:
                method = self.bot.send_sticker
                kwargs['sticker'] = text[len('sticker:'):]
            else:
                method = self.bot.send_message
                kwargs['text'] = text

            if self.chat['type'] == 'private':
                return method(chat_id=self.user['id'], **kwargs)
            if not self.private:
                kwargs.setdefault('reply_to_message_id', self.reply_id)
                return method(chat_id=self.chat['id'], **kwargs)
            try:
                return method(chat_id=self.user['id'], **kwargs)
            except ntelebot.errors.Forbidden:
                orig_text = self.text
                if self.command:
                    orig_text = '/%s %s' % (self.command, orig_text)
                return self.bot.send_message(
                    chat_id=self.chat['id'],
                    text=self.encode_link(orig_text, "Let's take this to a private chat!"),
                    reply_to_message_id=self.reply_id,
                    parse_mode='HTML')

        if self.edit_id:
            return self.bot.edit_message_text(
                chat_id=self.chat['id'], message_id=self.edit_id, text=text, **kwargs)

    def set_conversation(self, text):
        """If the next message from this user does not begin with a slash, prepend text."""

        if not text.startswith('/') and self.command:
            text = '/%s %s' % (self.command, text)
        self._conversations[self.user['id']] = text

    def split(self, num):
        """Split self.text into exactly num pieces, substituting blank strings for empty slots.

        This is intended for something like:

            def handler(ctx):
                target, action, text = ctx.split(3)

        where a message containing '/command' would result in target = action = text = '',
        '/command mytarget' would have target = 'mytarget' and action = text = '',
        '/command mytarget add some more data' would have target = 'mytarget', action = 'add', and
        text = 'some more data'.
        """

        ret = self.text.split(None, num - 1)
        while len(ret) < num:
            ret.append('')
        return ret


def encode(text):
    """Prepare text for use as a Telegram bot deeplink's start= value."""

    if not isinstance(text, bytes):
        text = text.encode('utf-8')

    return base64.urlsafe_b64encode(text).rstrip(b'=').decode('ascii')


def decode(text):
    """Extract the original command from a deeplink's start= value."""

    if not isinstance(text, bytes):
        try:
            text = text.encode('ascii')
        except UnicodeEncodeError:
            return ''

    try:
        text = base64.urlsafe_b64decode(text + b'====')
    except (TypeError, ValueError):
        return ''

    try:
        return text.decode('utf-8')
    except UnicodeDecodeError:
        return ''


def get_command(text, username):
    """The normalized command name if this is a command addressed to this bot."""

    if not text.startswith('/'):
        return None, text

    command, _, rest = text[1:].partition(' ')
    command = command.lower()
    if '@' in command:
        command, target_username = command.split('@', 1)
        if target_username != username.lower():
            return None, text
    return command, rest.lstrip()
