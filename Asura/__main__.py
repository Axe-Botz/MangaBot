import cloudscraper as c
from bs4 import BeautifulSoup as bs
import os 
import glob
import img2pdf
import requests 
#import asyncio

from pyrogram import filters, idle
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Asura import asura, BOT_NAME, BOT_USERNAME, SUPPORT, UPDATES, MUST_JOIN

# --------------------------------------------------------------------------------------------------- #

#loop = asyncio.get_event_loop()

@asura.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(bot: asura, msg: Message):
    if not MUST_JOIN:  # Not compulsory
        return
    try:
        try:
            await bot.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await bot.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply_photo(photo="https://telegra.ph/file/4ad5c5540908a9480b254.jpg", caption=f"According to my database you have not Joined my channel, to use me for free please kindly Join my channel for the latest updates !!",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🚀 Click here to Join", url=f"https://t.me/OxA_Code")]
                    ])
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"Promote me as an admin in the MUST_JOIN chat : {MUST_JOIN} !")


C = "<b> Asura Scans Updates</b> \n\n"
CS = "ヘ <b>Name :</b> <code>{}</code>\n\n"

CHS = "  ヘ [{}]({})\n"
"""
async def start_bot():
  return await asura.send_message(chat_id=LOG, text='Im Alive')
"""


def get_command(com):
  return filters.command([com, f"{com}@{BOT_USERNAME}"], prefixes=['!', '/', '.'])


async def sorted():
  def ssh(a):
    return int(a.split("-",1)[1].split('.')[0])
  
  f = glob.glob("./*jpg")
  f.sort(key=ssh)
  return f


async def pdf(name):
  lis = await sorted()
  for im in lis:
    if not name[:-4] in im:
      lis.remove(im)
    else:
      pass
  with open(name, 'wb') as f:
    f.write(img2pdf.convert(lis))
    f.close()
  for a in lis:
    os.remove(a)
  return name




@asura.on_message(get_command("manga"))
async def _asura(_, message):
  if not "asurascans.com" in message.text:
    return await message.reply_text("**Usage **:\n`/manga` url")
  else:
    pass
  try:
    url = message.text.split(" ", maxsplit=1)[1]
  except IndexError:
    return await message.reply_text("**Usage **:\n× `/manga` url")
  m = await message.reply_text("**Connecting..... Wait !!**")  
  s = c.create_scraper()
  html = s.get(url).text
  soup = bs(html, 'html.parser')
  title = soup.find_all("title")[0]
  title = title.text.replace(" - Asura Scans", "as.pdf")
  title = title.replace("-", "_")
  ims = soup.find_all("img", attrs={'loading':'lazy'})
  cont = ""
  num = 0
  flist = []
  for im in ims:
    if "wp-post-image" in im.get("class"):
      ims.remove(im)
    else:
      if im.get("src"):
        d = requests.get(im.get("src")).content
        open(f"{title[:-4]}-{num}.jpg", "wb").write(d)
      else:
        pass
      num += 1
  pf = await pdf(title)
  pd = pf[:-6] + ".pdf"
  os.rename(pf, pd)
  await m.edit_text("**Uploading 📤 Wait !!**")
  await message.reply_document(pd, caption=pd[:-4])
  await m.delete()
  return os.remove(pd)


@asura.on_message(get_command("start"))
async def _start(_, message):
  await message.reply_text(
    text=f"Hello {message.from_user.mention()}\n\nI'm a robot which provides you manga in pdf format for free :\nFrom Asura Scans & Reaper Scans.\n\nClick on the inline buttons given below to know more about me !!",
    reply_markup=InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton(
            text="🗂 Command",
            callback_data="hhelp"
          ),
          InlineKeyboardButton(
            text="🏳‍🌈 About",
            callback_data="abbout"
          )
        ]
      ]
    ),
    disable_web_page_preview=True
  )
  return 

@asura.on_callback_query(filters.regex("hhelp"))
async def hhelp(_, query):
  qm = query.message
  return await qm.edit_text(
    text="**Tool Commands are follow as :**\n\n• /latest\n- Get updates from asura scans\n\n• /manga (Url)\n- Get pdf of manga chapter\n\n• /rlatest\n- Get updates from reaper scans\n\n• /rmanga (Url)\n- Get pdf of manga chapter",
    reply_markup=InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton(
            text="⬅️ Back",
            callback_data="bback"
          )
        ]
      ]
    ),
    disable_web_page_preview=True
  )


@asura.on_callback_query(filters.regex("abbout"))
async def abblp(_, query):
  qm = query.message
  return await qm.edit_text(
    text=f"This bot is developed by a noob for getting mangas for free in just one click !!\n\nNoob : @Its_romeoo\n\nIf you are facing any problem regarding me then kindly report in our support chat, don't forget to subscribe my channel.", 
    reply_markup=InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton(
            text="📨 Support",
            url=f"https://t.me/{SUPPORT}"
          ),
          InlineKeyboardButton(
            text="📨 Updates",
            url=f"https://t.me/{UPDATES}"
          )
        ],
        [
          InlineKeyboardButton(
            text="⬅️ Back",
            callback_data="bback"
          )
        ]
      ]
    )
  )



@asura.on_message(get_command("latest"))
async def latest(_, message):
  s = c.create_scraper()
  a = s.get("https://asurascans.com").content
  sp = bs(a, 'html.parser')
  divs = sp.find_all("div", attrs={"class":"luf"})
  res = []
  for x in divs:
    title = x.h4.string
    msg = CS.format(title)
    for li in x.ul:
      msg += CHS.format(li.a.string, li.a.get("href"))
    res.append(msg)
  lim = int(4096/len(res[0])) + 1
  C = ""
  for x in res[:lim]:
    C += x
    C += "\n"
  return await message.reply(C, disable_web_page_preview=True)



@asura.on_callback_query(filters.regex("bback"))
async def _bvack(_, query):
  qm = query.message
  return await qm.edit_text(
      text=f"Hello [{query.message.chat.first_name}](tg://user?id={query.message.chat.id})\n\nI'm a robot which provides you manga in pdf format for free :\nFrom Asura Scans & Reaper Scans.\n\nClick on the inline buttons given below to know more about me!",
      reply_markup=InlineKeyboardMarkup(
        [
          [
            InlineKeyboardButton(
              text="🗂 Command",
              callback_data="hhelp"
            ),
            InlineKeyboardButton(
              text="🏳‍🌈 About",
              callback_data="abbout"
            )
          ]
        ]
      ),
      disable_web_page_preview=True
    )
   

@asura.on_message(get_command("rlatest"))
async def _rlatest(_, message):
  s = c.create_scraper()
  soup = bs(s.get("https://reaperscans.com").text, 'html.parser')
  tits = soup.find_all("div", attrs={"class":"series-box"})
    
  RST = "<b>Name</b>: <code>{}</code>"
  RSCH = "» [{}]({})"
    
  titles = []
  for tit in tits:
    title = tit.a.get("href").split("/")[-2]
    title = " ".join(x.capitalize() for x in title.split("-"))
    titles.append(RST.format(title))
    
  chs = []
  chaps = soup.find_all("div", attrs={"class":"series-content"})
  for chap in chaps:
    chap = chap.find_all("a")
    chs2 = []
    for cha in chap:
      ck = cha.get("href")[:-1].split("/")[-1]
      ck = ck.split("-")
      if len(ck) == 3:
        ck = ck[0] + " "+ ck[1] + "." + ck[2]
      else:
        ck = " ".join(ck)
      chs2.append(RSCH.format(ck.capitalize(), cha.get("href")))
    chs.append(chs2)
    
  msg = ""
  for title in titles[:16]:
    st = ""
    st += "× " + title
    st += "\n  " + "\n  ".join(chap for chap in chs[titles.index(title)])
    if "#" in st:
      pass
    else:
      msg += st + "\n\n"
    
  return await message.reply_text(text=msg[:4096], disable_web_page_preview=True)


@asura.on_message(get_command("rmanga"))
async def _rmanga(_, message):
  if not "reaperscans.com" in message.text:
    return await message.reply_text("**Usage **:\n× `/rmanga` url")
  else:
    pass
  try:
    url = message.text.split(" ", maxsplit=1)[1]
  except IndexError:
    return await message.reply_text("**Usage **:\n× `/rmanga` url")
  m = await message.reply_text("**Connecting..... Wait !!**")  
  s = c.create_scraper()
  soup = bs(s.get(url).text, 'html.parser')
  title = soup.title
  title= title.string + ".pdf"
  title = title.replace("-"," ")
  images = soup.find_all("img")
  cont = []
  for image in images:
    if (image.get("id")):
      url = image.get("data-src")
      cont.append(url.replace("\t", "").replace("\n", ""))
    else:
      pass
  im = []
  num = 0
  for x in cont:
    content = requests.get(x).content
    open(f'{title[:-4]}-{num}.jpg', 'wb').write(content)
    im.append(f'{title[:-4]}-{num}.jpg')
    num += 1
  titl = title.replace("Reaper Scans", "")
  pf = await pdf(title)
  os.rename(pf, titl)
  await m.edit_text("**Uploading 📤 Wait !!**")
  await message.reply_document(titl, caption=titl[:-4])
  await m.delete()
  return os.remove(titl)





if __name__ == "__main__":
  #loop.run_until_complete(start_bot())
  idle()
