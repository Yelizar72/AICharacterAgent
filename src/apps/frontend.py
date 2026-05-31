import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="Frontend is running. AI Character Agent will use OpenRouter + DeepSeek V4 Pro."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    await cl.Message(content=f"You said: {message.content}").send()
