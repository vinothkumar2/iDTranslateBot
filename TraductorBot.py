from telegram.ext import Updater , CommandHandler , MessageHandler , Filters , CallbackQueryHandler , InlineQueryHandler


from telegram import InlineKeyboardMarkup ,InlineKeyboardButton ,InlineQueryResultArticle , InputTextMessageContent

import telegram

from random import choice

import textblob
import json
import os

def start(Update,context):
	
	name=Update.effective_user.first_name
	
	boton=InlineKeyboardButton(
		text="Translate inline",
		callback_data="call_inline")
	
	text=f"<b>👋Halo {name}\n\n📝Write what you want to translate.\n\n👇Or try using our inline mode.</b>"
	
	Update.message.reply_text(
		text=text,
		parse_mode="html",
		reply_markup=
		InlineKeyboardMarkup([
		[boton]]))

def messagehandler(Update,context):	
	
	try :
		chat_id = Update.message.chat.id
		text=Update.message.text
		
		if chat_id > 0:
			
			try:
				
				lang= Update.effective_user.language_code
				
				blob = textblob.TextBlob(text)
				
				text_transl = str(blob.translate(to=lang))
				
				Update.message.reply_text(f"<b>❤ Done!\n\n</b><code>{text_transl}</code>",
				parse_mode="html")
					
				
				
				
			except Exception:

				context.user_data['text']=text
				
				boton1= InlineKeyboardButton(text=
				"🇪🇸Español" ,callback_data="es")
							
				boton2= InlineKeyboardButton(text=
				"🇬🇧English" ,callback_data="en")
								
				boton3= InlineKeyboardButton(text=
				"🇷🇺русский" ,callback_data="ru")	
				
				boton4= InlineKeyboardButton(text=
				"🇮🇹 Italiano" ,callback_data="it")
				
				boton5= InlineKeyboardButton(text=
				"🇰🇷한국어" ,callback_data="ko")		
						
				boton6= InlineKeyboardButton(text=
				"🇮🇳भारतीय" ,callback_data="hi")					
				
				emojis = ["😁","😆","🙃","🙂"]
				
				emoji=choice(emojis)
				
				
				Update.message.reply_text(text=
				f"<b>{emoji}Choose the language you want to translate to.</b>",
				parse_mode="html",
				reply_markup=
				InlineKeyboardMarkup([
				[boton1 , boton2],
				[boton3 , boton4],
				[boton5 , boton6]
				]))
		

		elif chat_id < 0 and text == "/tr":
			try:
				
				lang= Update.effective_user.language_code
				
				text=Update.message.reply_to_message.text
				
				message_id=Update.message.reply_to_message.message_id
				
				t = Update.message.text				
				
				blob = textblob.TextBlob(text)
				try:
					text_transl = str(blob.translate(to=lang))
					
					context.bot.send_message(chat_id=chat_id,
			                    text=
			                    f"<b>Translation:</b>\n\n--> <code>{text_transl}</code>",parse_mode="html",
				            reply_to_message_id=message_id)				
				
				except Exception:
					
					context.bot.send_message(chat_id=chat_id,
			                    text=
			                    f"<b>Translation:</b>\n\n--> <code>{text}</code>",parse_mode="html",
				            reply_to_message_id=message_id)		
			
			except AttributeError:
				
				answer="Is that a bot?"
				if lang!="en":
					blob = textblob.TextBlob(answer)				
					answer = str(blob.translate(to=lang))
					
				Update.message.reply_text(answer)	
	
	
	except Exception :
		pass


def callbackhandler(Update,context):
	
	query=Update.callback_query
	chat_id=Update.effective_user.id
	
	data = query.data
	
	if data != "call_inline":
		
		lang = data
		
		text=context.user_data.get("text","not found") 
			
		blob = textblob.TextBlob(text)
				
		try:
			
			t = str(blob.translate(to=lang))
			
			
			context.bot.send_message(chat_id=chat_id,text=f"<b>❤ Done!</b>\n\n<code>{t}</code>",parse_mode="html")		
		
		except Exception as error:
			
			context.bot.send_message(chat_id=chat_id,text=f"<b>❤ Done!</b>\n\n<code>{text}</code>",parse_mode="html")	
			
	elif data == "call_inline":
			
		boton1=InlineKeyboardButton(text=
		"🇪🇸Español" ,switch_inline_query="es ")
		
		boton2=InlineKeyboardButton(text=
		"🇬🇧English" ,switch_inline_query="en ")
					
		boton3=InlineKeyboardButton(text=
		"🇷🇺русский" ,switch_inline_query="ru ")	
		
		boton4=InlineKeyboardButton(text=
		"🇮🇹Italiano" ,switch_inline_query="it ")
		
		boton5=InlineKeyboardButton(text=
		"🇰🇷한국어" ,switch_inline_query="ko ")		
				
		boton6=InlineKeyboardButton(text=
		"🇮🇳भारतीय" ,switch_inline_query="hi ")					
		
		emojis = ["😁","😆","🙃","🙂"]
		
		emoji=choice(emojis)		
			
		query=Update.callback_query
				
		query.edit_message_text(
		text=f"<b>{emoji}Choose the language you want to translate to.</b>",
		parse_mode="html",
		reply_markup=
		InlineKeyboardMarkup([
		[boton1 , boton2],
		[boton3 , boton4],
		[boton5 , boton6]
		]))	

def mode_inline(Update,context):
	
	query_id=Update.inline_query.id	
	query=Update.inline_query.query
	

	text_inline=query
	
	lang = text_inline[:2]
	text_inline=text_inline[3:]

	results=[]
	
	blob = textblob.TextBlob(text_inline)
	
	try :
		
		text = str(blob.translate(to=lang))
		
	except Exception:
		text=text_inline		
				
	consulta = InlineQueryResultArticle(id=query_id,title= lang,  input_message_content=InputTextMessageContent(text),
		description=text)
		
	try :
		results.append(consulta)
		
		try:
			context.bot.answer_inline_query(
				Update.inline_query.id,
				results=results)
				
		except telegram.error.BadRequest:
			pass
	
	except UnboundLocalError :
		pass

if __name__ == "__main__":
	
	updater=Updater(token=os.environ ["TOKEN"])
	
	update=updater
	
	dp = updater.dispatcher
	
	dp.add_handler(CommandHandler('start',start))
	
	dp.add_handler(CallbackQueryHandler(pattern=0,callback=callbackhandler))
	
	dp.add_handler(InlineQueryHandler(mode_inline))	
	
	dp.add_handler(MessageHandler(Filters.text , messagehandler))
	
	
	updater.start_polling()
	print("bot is running")
	updater.idle()
