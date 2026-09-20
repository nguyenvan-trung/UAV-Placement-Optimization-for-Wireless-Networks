# Dataset documentation

ThÆ° má»¥c nÃ y **chá»‰ chá»©a tÃ i liá»‡u quy Æ°á»›c dataset**, khÃ´ng chá»©a CSV. Dá»¯ liá»‡u
thá»±c táº¿ náº±m á»Ÿ cáº¥p dá»± Ã¡n:

```text
data/
â”œâ”€â”€ raw/       # dá»¯ liá»‡u gá»‘c chÆ°a xá»­ lÃ½
â”œâ”€â”€ stores/    # CSV Ä‘áº§u vÃ o chÃ­nh thá»©c cho thuáº­t toÃ¡n
â””â”€â”€ views/     # áº£nh quan sÃ¡t cá»§a tá»«ng CSV
```

## `data/stores` dÃ¹ng Ä‘á»ƒ lÃ m gÃ¬?

ÄÃ¢y lÃ  nguá»“n Ä‘áº§u vÃ o á»•n Ä‘á»‹nh cho toÃ n bá»™ pipeline. CÃ¡c thuáº­t toÃ¡n khÃ´ng tá»±
sinh hoáº·c sá»­a file trong thÆ° má»¥c nÃ y. Má»™t CSV cÃ³ schema:

```text
user_id,x_m,y_m,z_m,demand
```

CÃ¡c bÆ°á»›c Ä‘á»c, kiá»ƒm tra schema vÃ  chuyá»ƒn thÃ nh kiá»ƒu dá»¯ liá»‡u ná»™i bá»™ náº±m trong
`src/input/`. CÃ¡c bÆ°á»›c K-Means vÃ  táº¡o nghiá»‡m khá»Ÿi táº¡o náº±m trong
`src/preprocessing/`.

## `data/views` dÃ¹ng Ä‘á»ƒ lÃ m gÃ¬?

ÄÃ¢y lÃ  áº£nh kiá»ƒm tra trá»±c quan (`top`, `front`, `side`, `3d`) tÆ°Æ¡ng á»©ng vá»›i
tá»«ng CSV. áº¢nh giÃºp phÃ¡t hiá»‡n dá»¯ liá»‡u quÃ¡ Ä‘á»u, sai pháº¡m vi tá»a Ä‘á»™ hoáº·c sai tÃªn
dataset; áº£nh khÃ´ng Ä‘Æ°á»£c dÃ¹ng lÃ m Ä‘áº§u vÃ o cho optimizer.

## Táº¡o láº¡i dataset

Chá»‰ cháº¡y khi muá»‘n thay Ä‘á»•i seed, sá»‘ lÆ°á»£ng user hoáº·c quy táº¯c sinh dá»¯ liá»‡u:

```powershell
cd implementation
python scripts/generate_dataset.py
```

Lá»‡nh nÃ y ghi CSV vÃ o `../data/stores/` vÃ  áº£nh vÃ o `../data/views/`.

