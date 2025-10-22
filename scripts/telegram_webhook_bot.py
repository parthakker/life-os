"""
Production Telegram Webhook Bot for Life OS
Industry-standard 2025 implementation using FastAPI + webhooks
"""

import os
import sys
import secrets
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response, HTTPException, Header
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Import your existing router functions
from router import (
    route_message,
    execute_add_task,
    execute_add_note,
    execute_ask_question,
    execute_log_sleep,
    execute_log_water,
    execute_log_exercise,
    execute_log_sauna,
    execute_log_inbody
)

# Environment variables
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
AUTHORIZED_USER_ID = os.getenv('TELEGRAM_USER_ID')
SECRET_TOKEN = os.getenv('WEBHOOK_SECRET_TOKEN')  # NEW - for security
PORT = int(os.getenv('PORT', 8000))  # Render provides PORT env var
WEBHOOK_URL = os.getenv('RENDER_EXTERNAL_URL')  # Render provides this

# Validate required env vars
if not BOT_TOKEN:
    print("[ERROR] TELEGRAM_BOT_TOKEN not set")
    sys.exit(1)

if not SECRET_TOKEN:
    # Generate one if not provided (but should be set in Render dashboard)
    SECRET_TOKEN = secrets.token_urlsafe(32)
    print(f"[WARNING] Generated SECRET_TOKEN: {SECRET_TOKEN}")
    print("[WARNING] Set this in Render environment variables!")

# Build webhook URL
if not WEBHOOK_URL:
    # Local development fallback
    WEBHOOK_URL = f"http://localhost:{PORT}"
    print(f"[LOCAL DEV] Using webhook URL: {WEBHOOK_URL}")
else:
    print(f"[PRODUCTION] Using webhook URL: {WEBHOOK_URL}")

# Initialize PTB application WITHOUT updater (we handle updates via webhook)
ptb_app = (
    Application.builder()
    .token(BOT_TOKEN)
    .updater(None)  # No polling!
    .build()
)


# ==================== BOT HANDLERS (same as before) ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "🤖 Life OS Agentic Assistant (Webhook Mode)\n\n"
        "I can help you:\n"
        "✓ Add tasks\n"
        "📝 Save notes\n"
        "💭 Answer questions\n"
        "📊 Log health data\n\n"
        "Just send me a message!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "Life OS Bot - Webhook Mode\n\n"
        "/start - Start the bot\n"
        "/help - Show this help\n"
        "/stats - Show statistics\n\n"
        "Send any message to add it to Life OS!"
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    from db_helper import execute_query

    try:
        # Get task counts
        active = execute_query(
            'SELECT COUNT(*) as c FROM tasks WHERE completed = ?',
            (False,),
            fetch='one'
        )
        completed = execute_query(
            'SELECT COUNT(*) as c FROM tasks WHERE completed = ?',
            (True,),
            fetch='one'
        )
        notes = execute_query('SELECT COUNT(*) as c FROM notes', fetch='one')
        cats = execute_query('SELECT COUNT(*) as c FROM categories', fetch='one')

        await update.message.reply_text(
            f"Life OS Statistics:\n\n"
            f"Active Tasks: {active['c']}\n"
            f"Completed Tasks: {completed['c']}\n"
            f"Notes: {notes['c']}\n"
            f"Categories: {cats['c']}\n\n"
            f"Mode: Webhook (Production)\n"
            f"Keep crushing it!"
        )
    except Exception as e:
        await update.message.reply_text(f"Error getting stats: {e}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages - route to appropriate tool"""

    # Security check
    if AUTHORIZED_USER_ID and str(update.effective_user.id) != AUTHORIZED_USER_ID:
        await update.message.reply_text("Sorry, you're not authorized.")
        return

    message_text = update.message.text
    await update.message.chat.send_action("typing")

    try:
        # Route message (same logic as polling version)
        routing_result = route_message(message_text)
        tool = routing_result['tool']

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

        elif tool == 'log_sleep':
            response = execute_log_sleep(
                routing_result['hours'],
                routing_result.get('date'),
                routing_result.get('notes')
            )
            await update.message.reply_text(response['message'])

        elif tool == 'log_water':
            response = execute_log_water(
                routing_result['cups'],
                routing_result.get('date')
            )
            await update.message.reply_text(response['message'])

        elif tool == 'log_exercise':
            response = execute_log_exercise(
                routing_result['activity_type'],
                routing_result['duration_minutes'],
                routing_result.get('date'),
                routing_result.get('notes')
            )
            await update.message.reply_text(response['message'])

        elif tool == 'log_sauna':
            response = execute_log_sauna(
                routing_result['duration_minutes'],
                routing_result.get('num_visits', 1),
                routing_result.get('date')
            )
            await update.message.reply_text(response['message'])

        elif tool == 'log_inbody':
            response = execute_log_inbody(
                routing_result['weight'],
                routing_result['smm'],
                routing_result['pbf'],
                routing_result['ecw_tbw_ratio'],
                routing_result.get('date'),
                routing_result.get('notes')
            )
            await update.message.reply_text(response['message'])

        else:
            await update.message.reply_text(f"Unknown tool: {tool}")

    except Exception as e:
        await update.message.reply_text(
            f"Oops: {str(e)}\n\nTry rephrasing."
        )


# Register handlers
ptb_app.add_handler(CommandHandler("start", start))
ptb_app.add_handler(CommandHandler("help", help_command))
ptb_app.add_handler(CommandHandler("stats", stats_command))
ptb_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


# ==================== FASTAPI WEBHOOK SERVER ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown"""
    print("[OK] Starting webhook bot...")

    # Set webhook with Telegram
    webhook_url = f"{WEBHOOK_URL}/telegram-webhook"
    print(f"[OK] Setting webhook URL: {webhook_url}")

    await ptb_app.bot.set_webhook(
        url=webhook_url,
        allowed_updates=Update.ALL_TYPES,
        secret_token=SECRET_TOKEN  # Security: validates requests from Telegram
    )

    async with ptb_app:
        await ptb_app.start()
        print("[OK] Webhook bot running!")
        yield
        print("[OK] Shutting down...")
        await ptb_app.stop()


# Create FastAPI app
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    """Root endpoint - helps verify service is up"""
    return {"status": "Life OS Telegram Bot (Webhook Mode)", "healthy": True}


@app.get("/health")
async def health_check():
    """Health check for Render"""
    return {"status": "healthy", "mode": "webhook"}


@app.post("/telegram-webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(None)
):
    """
    Webhook endpoint for Telegram updates

    Security: Validates secret token to prevent fake updates
    """
    # Validate secret token
    if x_telegram_bot_api_secret_token != SECRET_TOKEN:
        print(f"[SECURITY] Invalid secret token from {request.client.host}")
        raise HTTPException(status_code=403, detail="Invalid secret token")

    # Parse update
    try:
        data = await request.json()
        update = Update.de_json(data, ptb_app.bot)

        # Process update asynchronously
        await ptb_app.update_queue.put(update)

        return Response(status_code=200)

    except Exception as e:
        print(f"[ERROR] Processing update: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== RUN SERVER ====================

if __name__ == "__main__":
    import uvicorn

    print("="*60)
    print("Life OS Telegram Webhook Bot")
    print("="*60)
    print(f"Bot Token: {BOT_TOKEN[:20]}...")
    print(f"Webhook URL: {WEBHOOK_URL}")
    print(f"Port: {PORT}")
    print(f"Secret Token: {SECRET_TOKEN[:10]}...")
    print("="*60)

    # Run with uvicorn (production-ready ASGI server)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
