words = """ここ ここ here, this place
そこ そこ there, that place near you
あそこ あそこ that place over there
どこ どこ where, what place?
こちら こちら this way, this place (polite ここ)
そちら そちら that way, that place near you (polite そこ)
あちら あちら that way, that place over there (polite あそこ)
どちら どちら which way, where (polite どこ)
きょうしつ 教室 classroom
しょくどう 食堂 dining hall, canteen
じむしょ 事務所 office
かいぎしつ 会議室 conference room, assembly rooms
うけつけ 受付 reception desk
ロビー ロビー lobby
へや 部屋 room
トイレ(おてあらい) (お手洗い) toilet
かいだん 階段 staircase
エレベーター エレベーター elevator, lift
エスカレーター エスカレーター escalator
[お]くに [お]国 country
かいしゃ 会社 work
うち 家 house, home
でんわ 電話 telephone, telephone call
くつ 靴 shoes
ネクタイ ネクタイ necktie
ワイン ワイン wine
たばこ 煙草 tobacco, cigarette
うりば 売り場 department, counter (in a department store)
ちか 地下 basement
〜かい(〜がい) 〜階 ~th floor
なんがい 何階 what floor
〜えん 〜円 ~yen
いくら 幾ら how much
ひゃく 百 hundred
せん 千 thousand
まん 万 ten thousand
すみません。 すみません。 Excuse me.
~でございます。 ~でございます。 (polite equivalent of です)
[~を]みせてください。 [~を]見せてください。 Please show me [~].
じゃ じゃ well, then, in that case
[~を]くだざい。 [~を]くだざい。 Give me [~], please."""
from connector import PostgreSQLConnector
dbc = PostgreSQLConnector(database="nihongo", host="77.232.128.211", port=22432, password="q7ECSk3H")

for each in words.split("\n"):
    e = each.split(" ", 2)
    dbc.words.add(lesson_id = 8, kana = e[0], kanji = e[1], english = e[2]).exec()