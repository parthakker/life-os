"""
Telegram Bot for Life OS
Receives messages and routes them to appropriate tools using agentic router
"""

import os
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from router import route_message, execute_add_task, execute_add_note, execute_ask_question

# Telegram bot token - you'll need to create this with @BotFather
# Set as environment variable: TELEGRAM_BOT_TOKEN
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not BOT_TOKEN:
    print("[ERROR] TELEGRAM_BOT_TOKEN environment variable not set")
    print("\nTo set up:")
    print("1. Message @BotFather on Telegram")
    print("2. Create a new bot with /newbot")
    print("3. Copy the token")
    print("4. Set environment variable:")
    print("   Windows: set TELEGRAM_BOT_TOKEN=your_token_here")
    print("   Or add to Windows Environment Variables permanently")
    sys.exit(1)

# Your Telegram user ID (for security - only you can use the bot)
# You can get this by messaging @userinfobot on Telegram
AUTHORIZED_USER_ID = os.getenv('TELEGRAM_USER_ID')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "🤖 Life OS Agentic Assistant is ready!\n\n"
        "I can help you:\n"
        "✓ Add tasks (things to do)\n"
        "📝 Save notes (information, quotes, ideas)\n"
        "💭 Answer questions about your data\n\n"
        "Examples:\n"
        "- buy groceries tomorrow\n"
        "- i love the eagles\n"
        "- what are my open home tasks\n\n"
        "I'll automatically figure out what to do!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "Life OS Bot - Commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/stats - Show your Life OS statistics\n\n"
        "Just send any message to add it to Life OS!"
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    import sqlite3
    from pathlib import Path

    DB_PATH = Path(__file__).parent.parent / 'data.db'

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get task count
        cursor.execute('SELECT COUNT(*) FROM tasks WHERE completed = 0')
        active_tasks = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM tasks WHERE completed = 1')
        completed_tasks = cursor.fetchone()[0]

        # Get note count
        cursor.execute('SELECT COUNT(*) FROM notes')
        notes_count = cursor.fetchone()[0]

        # Get category count
        cursor.execute('SELECT COUNT(*) FROM categories')
        categories_count = cursor.fetchone()[0]

        conn.close()

        await update.message.reply_text(
            f"Life OS Statistics:\n\n"
            f"Active Tasks: {active_tasks}\n"
            f"Completed Tasks: {completed_tasks}\n"
            f"Notes: {notes_count}\n"
            f"Categories: {categories_count}\n\n"
            f"Keep crushing it!"
        )

    except Exception as e:
        await update.message.reply_text(f"Error getting stats: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages - route to appropriate tool"""

    # Security check - only allow authorized user
    if AUTHORIZED_USER_ID and str(update.effective_user.id) != AUTHORIZED_USER_ID:
        await update.message.reply_text("Sorry, you're not authorized to use this bot.")
        return

    message_text = update.message.text

    # Show typing indicator
    await update.message.chat.send_action("typing")

    try:
        # Route message to appropriate tool
        routing_result = route_message(message_text)
        tool = routing_result['tool']

        # Execute based on tool selection
        if tool == 'add_task':
            response = execute_add_task(
                routing_result['category'],
                routing_result['content'],
                routing_result.get('due_date')
            )
            await update.message.reply_text(response['message'])

        elif tool == 'add_note':
            response = execute_add_note(
                routing_result['category'],
                routing_result['content']
            )
            await update.message.reply_text(response['message'])

        elif tool == 'ask_question':
            response = execute_ask_question(
                routing_result['query'],
                routing_result.get('query_type', 'all'),
                routing_result.get('filters')
            )
            await update.message.reply_text(response['message'])

        else:
            await update.message.reply_text(f"Unknown tool: {tool}")

    except Exception as e:
        await update.message.reply_text(
            f"Oops, something went wrong:\n{str(e)}\n\n"
            f"Try rephrasing or check the logs."
        )

def main():
    """Start the bot"""
    print("[OK] Starting Life OS Telegram Bot...")
    print(f"[OK] Bot token: {BOT_TOKEN[:20]}...")

    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("[OK] Bot is running!")
    print("[OK] Send messages on Telegram to categorize them")
    print("[OK] Press Ctrl+C to stop")

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
