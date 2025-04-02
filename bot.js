const { Telegraf } = require('telegraf');
const schedule = require('node-schedule');
const { Builder, By } = require('selenium-webdriver');
const fs = require('fs');
const path = require('path');

const BOT_TOKEN = '8086048340:AAG-4pdcyFhWJnlsIkmlHriPfqMRQs9yzck';
const bot = new Telegraf(BOT_TOKEN);
const INSTAGRAM_USERNAME = 'shaurma.na.ugliah';
let autoMode = true;

// Функция для скачивания истории Instagram
async function downloadInstagramStory() {
    let driver = await new Builder().forBrowser('chrome').build();
    try {
        await driver.get(`https://www.instagram.com/stories/${INSTAGRAM_USERNAME}/`);
        await driver.sleep(5000);
        
        let storyImage = await driver.findElement(By.css('img[srcset]'));
        let imageUrl = await storyImage.getAttribute('src');
        
        let imagePath = path.join(__dirname, 'story.jpg');
        let response = await fetch(imageUrl);
        let buffer = await response.arrayBuffer();
        fs.writeFileSync(imagePath, Buffer.from(buffer));
        
        return imagePath;
    } catch (error) {
        console.error('Ошибка при получении истории:', error);
        return null;
    } finally {
        await driver.quit();
    }
}

// Функция отправки опроса
async function sendPoll(ctx, imagePath) {
    await ctx.replyWithPhoto({ source: imagePath }, { caption: 'Что думаете об этой истории?' });
    await ctx.sendPoll('Нравится ли вам эта история?', ['Да', 'Нет']);
}

// Команда /get_story
bot.command('get_story', async (ctx) => {
    let imagePath = await downloadInstagramStory();
    if (imagePath) {
        await sendPoll(ctx, imagePath);
    } else {
        ctx.reply('Не удалось получить историю 😔');
    }
});

// Команда /auto_mode для включения/выключения автоматического режима
bot.command('auto_mode', (ctx) => {
    autoMode = !autoMode;
    ctx.reply(`Автоматический режим ${autoMode ? 'включен' : 'выключен'}.`);
});

// Автоматическая проверка историй раз в сутки в 07:00 UTC+0
schedule.scheduleJob('0 7 * * *', async () => {
    if (autoMode) {
        let imagePath = await downloadInstagramStory();
        if (imagePath) {
            bot.telegram.sendPhoto('@your_channel', { source: imagePath }, { caption: 'Что думаете об этой истории?' });
            bot.telegram.sendPoll('@your_channel', 'Нравится ли вам эта история?', ['Да', 'Нет']);
        }
    }
});

// Запуск бота
bot.launch();
console.log('Бот запущен 🚀');
