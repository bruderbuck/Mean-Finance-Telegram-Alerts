# Mean-Finance-Telegram-Alerts

For those who may not be familiar with it, mean.finance is a decentralized finance (DeFi) platform that allows users to dollar-cost average (DCA) into cryptocurrency by automating purchases using smart contracts. In addition to DCA, mean.finance also allows users to earn yield on their idle cryptocurrency. However, these positions can sometimes run out of funds, which might be annoying since there is no direct notification system that informs you of that.

To solve this problem, I decided to write a Telegram bot that monitors the funds in my mean.finance positions and sends me a notification as soon as one of them becomes depleted. In this post, I'll explain how I built the bot and how you can set up a similar one for your own mean.finance positions. 

> ## What you need:
> - Raspberry Pi or Server; something to run the python script on
>
> - a telegram bot instance; just follow step 2 of this [tutorial](https://www.process.st/telegram-bot/). You should now have the token for the http API
>
> - your own telegram chat id: follow this [tutorial](https://diyusthad.com/2022/03/how-to-get-your-telegram-chat-id.html) to get it

The code currently exists of two python scripts meant to run in parallel. One will send you alerts when a position is about to run out of funds. The other one handles manual updates. To use it you can text "Update" to the bot and it will give you the remaining swaps.
