import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import youtube_dl

# Define your Telegram bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Initialize the bot and dispatcher
updater = Updater(token=BOT_TOKEN, use_context=True)

# Command to start the bot
def start(update, context):
    update.message.reply_text('Hello! Send me a video URL to get started.')

# Function to handle received video URLs
def handle_video_url(update, context):
    video_url = update.message.text
    # Here you can add logic to get video quality options
    # This is just a placeholder for simplicity
    keyboard = [
        [InlineKeyboardButton('240p', callback_data='240'), InlineKeyboardButton('360p', callback_data='360')],
        [InlineKeyboardButton('480p', callback_data='480'), InlineKeyboardButton('720p', callback_data='720')],
        [InlineKeyboardButton('1080p', callback_data='1080')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please select video quality:', reply_markup=reply_markup)

# Function to handle quality selection
def button(update, context):
    query = update.callback_query
    query.answer()
    quality = query.data
    video_url = context.user_data.get('video_url')
    # Logic for downloading the video based on the selected quality
    download_video(video_url, quality, query)

# Function to download video
def download_video(video_url, quality, query):
    try:
        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        # Send back the video
        query.message.reply_text('Video downloaded successfully!')
        # Here put the logic to send the downloaded file back to user
    except Exception as e:
        query.message.reply_text(f'Error: {e}')

# Main function to run the bot
def main():
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_video_url))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling()  
    updater.idle()

if __name__ == '__main__':
    main()