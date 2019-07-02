import logging
import time
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from src.db_worker import update_user_by_chat_id, update_user_by_message
HANDLED_STR = ['Unhandled', 'Handled']


class mLoggingMiddleware(BaseMiddleware):
    def __init__(self, logger=None):
        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(self.__class__.__name__)

        self.logger = logger

        super(mLoggingMiddleware, self).__init__()

    def check_timeout(self, obj):
        start = obj.conf.get('_start', None)
        if start:
            del obj.conf['_start']
            return round((time.time() - start) * 1000)
        return -1

    async def on_pre_process_update(self, update: types.Update, data: dict):
        update.conf['_start'] = time.time()
        pass

    async def on_post_process_update(self, update: types.Update, result, data: dict):
        timeout = self.check_timeout(update)
        pass
        # if timeout > 0:
        #     self.logger.info(f"Process update [ID:{update.update_id}]: [success] (in {timeout} ms)")

    async def on_pre_process_message(self, message: types.Message, data: dict):
        self.logger.info(f"Received message [TEXT: \"{message.text}\"] in chat [{message.from_user.first_name} {message.from_user.username} {message.from_user.id}]")

    async def on_post_process_message(self, message: types.Message, results, data: dict):
        pass
        # self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
        #                   f"message [ID:{message.message_id}] in chat [{message.chat.type}:{message.chat.id}]")

    async def on_pre_process_edited_message(self, edited_message, data: dict):
        pass
        # self.logger.info(f"Received edited message [ID:{edited_message.message_id}] "
        #                  f"in chat [{edited_message.chat.type}:{edited_message.chat.id}]")

    async def on_post_process_edited_message(self, edited_message, results, data: dict):
        pass
        # self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
        #                   f"edited message [ID:{edited_message.message_id}] "
        #                   f"in chat [{edited_message.chat.type}:{edited_message.chat.id}]")

    async def on_pre_process_channel_post(self, channel_post: types.Message, data: dict):
        pass
        # self.logger.info(f"Received channel post [ID:{channel_post.message_id}] "
        #                  f"in channel [ID:{channel_post.chat.id}]")

    async def on_post_process_channel_post(self, channel_post: types.Message, results, data: dict):
        pass
        # self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
        #                   f"channel post [ID:{channel_post.message_id}] "
        #                   f"in chat [{channel_post.chat.type}:{channel_post.chat.id}]")

    async def on_pre_process_edited_channel_post(self, edited_channel_post: types.Message, data: dict):
        pass
        # self.logger.info(f"Received edited channel post [ID:{edited_channel_post.message_id}] "
        #                  f"in channel [ID:{edited_channel_post.chat.id}]")

    async def on_post_process_edited_channel_post(self, edited_channel_post: types.Message, results, data: dict):
        pass
        # self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
        #                   f"edited channel post [ID:{edited_channel_post.message_id}] "
        #                   f"in channel [ID:{edited_channel_post.chat.id}]")

    async def on_pre_process_inline_query(self, inline_query: types.InlineQuery, data: dict):
        pass
        # self.logger.info(f"Received inline query [ID:{inline_query.id}] "
        #                  f"from user [ID:{inline_query.from_user.id}]")

    async def on_post_process_inline_query(self, inline_query: types.InlineQuery, results, data: dict):
        pass
        # self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
        #                   f"inline query [ID:{inline_query.id}] "
        #                   f"from user [ID:{inline_query.from_user.id}]")

    async def on_pre_process_chosen_inline_result(self, chosen_inline_result: types.ChosenInlineResult, data: dict):
        pass
        # self.logger.info(f"Received chosen inline result [Inline msg ID:{chosen_inline_result.inline_message_id}] "
        #                  f"from user [ID:{chosen_inline_result.from_user.id}] "
        #                  f"result [ID:{chosen_inline_result.result_id}]")

    async def on_post_process_chosen_inline_result(self, chosen_inline_result, results, data: dict):
        pass
        # self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
        #                   f"chosen inline result [Inline msg ID:{chosen_inline_result.inline_message_id}] "
        #                   f"from user [ID:{chosen_inline_result.from_user.id}] "
        #                   f"result [ID:{chosen_inline_result.result_id}]")

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        if callback_query.message:
            if callback_query.message.from_user:
                self.logger.info(f"Received callback query [ID:{callback_query.id}, DATA:{callback_query.data}] "
                                 f"in chat [{callback_query.message.chat.type}:{callback_query.message.chat.id}] "
                                 f"from user [USERNAME:{callback_query.message.from_user.username}, ID:{callback_query.message.from_user.id}]")
            else:
                self.logger.info(f"Received callback query [ID:{callback_query.id}], DATA:{callback_query.data}] "
                                 f"in chat [{callback_query.message.chat.type}:{callback_query.message.chat.id}]")
        else:
            self.logger.info(f"Received callback query [ID:{callback_query.id}, DATA:{callback_query.data}] "
                             f"from inline message [ID:{callback_query.inline_message_id}] "
                             f"from user [ID:{callback_query.from_user.username}]")

    async def on_post_process_callback_query(self, callback_query, results, data: dict):
        pass
        # if callback_query.message:
        #     if callback_query.message.from_user:
        #         self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
        #                           f"callback query [ID:{callback_query.id}] "
        #                           f"in chat [{callback_query.message.chat.type}:{callback_query.message.chat.id}] "
        #                           f"from user [ID:{callback_query.message.from_user.id}]")
        #     else:
        #         self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
        #                           f"callback query [ID:{callback_query.id}] "
        #                           f"in chat [{callback_query.message.chat.type}:{callback_query.message.chat.id}]")
        # else:
        #     self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
        #                       f"callback query [ID:{callback_query.id}] "
        #                       f"from inline message [ID:{callback_query.inline_message_id}] "
        #                       f"from user [ID:{callback_query.from_user.id}]")

    async def on_pre_process_shipping_query(self, shipping_query: types.ShippingQuery, data: dict):
        pass
        # self.logger.info(f"Received shipping query [ID:{shipping_query.id}] "
        #                  f"from user [ID:{shipping_query.from_user.id}]")

    async def on_post_process_shipping_query(self, shipping_query, results, data: dict):
        pass
        # self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
        #                   f"shipping query [ID:{shipping_query.id}] "
        #                   f"from user [ID:{shipping_query.from_user.id}]")

    async def on_pre_process_pre_checkout_query(self, pre_checkout_query: types.PreCheckoutQuery, data: dict):
        pass
        # self.logger.info(f"Received pre-checkout query [ID:{pre_checkout_query.id}] "
        #                  f"from user [ID:{pre_checkout_query.from_user.id}]")

    async def on_post_process_pre_checkout_query(self, pre_checkout_query, results, data: dict):
        pass
        # self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
        #                    f"pre-checkout query [ID:{pre_checkout_query.id}] "
        #                    f"from user [ID:{pre_checkout_query.from_user.id}]")

    async def on_pre_process_error(self, update: types.Update, error, data: dict):
        timeout = self.check_timeout(update)
        if timeout > 0:
            self.logger.info(f"Process update [ID:{update.update_id}, NAME:{update.__class__.__name__}]: [failed] (in {timeout} ms)")


class mUpdateUserMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        update_user_by_message(message)

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        if callback_query.message and callback_query.message.from_user:
                update_user_by_chat_id(callback_query.from_user.id, callback_query.from_user.first_name, callback_query.from_user.last_name,
                                       callback_query.from_user.username)