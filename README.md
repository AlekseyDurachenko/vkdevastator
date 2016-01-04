# vkdevastator
Набор скриптов позволяющий найти и удалить всю* вашу активность** из социальной сети ВКонтакте.

(*) поиск происходит путем полного перебора групп и друзей. 
Поэтому, если вас ничто не связывает с пользователем или группой, 
то найти вашу активность там не представляется возможным.

(**) на данный момент поддерживаются следующие объекты: 
- фотографии;
- комментарии к фотографиям;
- видео;
- комментарии к видео;
- заметки;
- комментарии к заметкам;
- обсуждения;
- комментарии к обсуждениям;
- записи на стене;
- комментарии к записям на стене.

## Рекомендации
* Если вы совершили некоторую активность в группе или в профиле пользователя - не удаляйте их (группу, пользователя). В дальнейшем это облегчит поиск и удаление вашей активности.

## Установка и запуск
Для загрузки скрипта вам потребуется git а так же python 2.x для запуска

В Debian/Ubuntu поставить их можно следующим образом:
```bash    
sudo apt-get install git python2
```

Загрузка и установка скрипта:
```bash
cd ~
git clone https://github.com/AlekseyDurachenko/vkdevastator vkdevastator
```

Запуск скрипта:
```bash
cd ~/vkdevastator/src
python ./vksearchactivities.py --access-token XXXYYYZZZ --target-id ID --state-file state.txt --activities-file activities.txt --activities-detail-file detail.txt
vkdeleteactivities.py --access-token XXXYYYZZZ --activities-file activities.txt
```

## Получение ACCESS TOKEN
* Во-первых, вам необходимо зарегистрировать новое приложение типа **Standalone-приложение** 
(http://vk.com/editapp?act=create), или использовать уже имеющееся. 
Так или иначе вам потребуется его уникальный **APP_ID**. 
* После того, как вам стал известен ваш **APP_ID** следует пройти OAuth авторизацию для получения access_token.

### Через браузер
* перейдите по ссылке (заменив APP_ID на ID вашего приложения, полученного на предыдущем шаге): https://oauth.vk.com/authorize?client_id=APP_ID&scope=friends,photos,audio,video,docs,notes,pages,status,wall,groups,offline&display=page&redirect_uri=https://oauth.vk.com/blank.html&response_type=token& 
* далее, следуя указаниям, пройдите авторизацию
* В случае успешной авторизации в адресной строке вы увидите access_token=XXXYYYZZZ. Это и есть ваш ключ приложения.
    
**Примечание! Перед получением access_token следуе выйти из ВКонтакте или открыть приватную вкладку.**

### Через утилиту vkoauth (http://alekseydurachenko.github.io/vkoauth/)
* введите ID вашего приложения;
* выберите следующие разрешения: friends, photos, audio, video, docs,notes, pages, status, wall, groups, offline;
* пройдите авторизацию приложения
* в поле access_token должен появиться ваш ключ приложения
    
## Поиск вашей активности (vksearchactivities.py)
```
== vksearchactivities.py - v.0.1.1  ==
Usage: 
    vksearchactivities.py --access-token <> --target-id <> --state-file <> --activities-file <> --activities-detail-file <>
    
    --log-file <>   Path to the log file
    --search-user-depth  N   (default 1) The users search depth
    --search-group-depth N   (default 1) The groups search depth
    --custom-user-ids    N   The list of custom user_id splitted by ","
    --custom-group-ids   N   The list of custom group_id splitted by "," (positive values)
    --disable-scan-friends   Ignore the friends
    --disable-scan-followers  Ignore the followers
    --disable-scan-user-subscriptions   Ignore the subscriptions to users
    --disable-scan-group-subscriptions  Ignore the subscriptions to groups
    --show-api-queries   Show the API queries
    --show-api-errors    Show the API errors
    --limit-member-count   Limit the maximum member count of the group
    --scan-time-limit    N   limit the time of the scanning of user(group), in minutes
    --enable-scan-himself    Don't ignore himself
    --disable-scan-walls
    --disable-scan-photos
    --disable-scan-photocomments
    --disable-scan-videos
    --disable-scan-topics
```

Данный скрипт используется для поиска всей вашей активности. В простейшем случае запуск осуществляется следующим образом:
```bash
python ./vksearchactivities.py --access-token XXXYYYZZZ --target-id ID --state-file state.txt --activities-file activities.txt --activities-detail-file detail.txt
```

Подставьте в этот скрипт вместо XXXYYYZZZ ваш access_token а вместо ID ваш идентификатор пользователя ВКонтакте
(узнать его можно на странице http://vk.com/settings в поле "Номер страницы"). 

В результате поиск вашей активности будет произведен во всех ваших группах, друзьях, подписчиках и подписках. 

Ознакомиться с результатами поиска можно в файле detail.txt

Эти же результаты, но в машинно читаемом виде хранятся в файле activities.txt

В файле state.txt хранятся идентификаторы пользователя и групп, которые уже были проверены на наличие вашей активности.
Если вы хотите произвести поиск заново - просто удалите этот файл.

Скрипт можно остановить с помощью CTRL+C. Когда вы запустите его вновь, поиск продолжится с места остановки.

Иногда бывает недостаточно проверки только своих групп и своих друзей. На этот случай предоставляется возможность
искать группы друзей, друзей друзй, группы друзей друзей и т.п. За это отвечают параметры --search-user-depth N,
--search-group-depth N. Где N - глубина поиска. "0" означает, что проверка друзей/групп не производится. "1" означет
что поиск производится только в своих группах/друзьях. "2" означает, что поиск друзей/групп производится у друзей 
и так далее.

```bash
python ./vksearchactivities.py --access-token XXXYYYZZZ --target-id ID --state-file state.txt --activities-file activities.txt --activities-detail-file detail.txt -search-user-depth 1 --search-group-depth 2
```

В данном случае поиск будет произведен в ваших группах, друзьях, подписчиках, подписках а так же в 
группах друзей, подписчиков, подписках.

Если в группе слишком много участников, то это, как правило, означает большое кол-во контента, а следовательно
и поиск вашей активности может затянуться надолго. Чтобы этого избежать рекомендуется исключить поиск в группах
с кол-во участников превышающим определенное число. Сделать это можно при помощи --limit-member-count N,
где N максимальное кол-во участников в группе:
```bash
python ./vksearchactivities.py --access-token XXXYYYZZZ --target-id ID --state-file state.txt --activities-file activities.txt --activities-detail-file detail.txt --search-user-depth 1 --search-group-depth 2 --limit-member-count 1000
```

Бывает так, что некоторые пользователи или группы имеют слишком большую стену,
слишком много фотографий и т.п., что приводит к очень долгому сканированию
данного пользователя(группы). Чтобы этого избежать, достаточно задать 
колюч --scan-time-limit N, где N - кол-во минут, которое допускается потратить
на одного пользователя(группу). Если сканирование провести не удалось, то
пользователь(группа) пропускается а ее id помечается как "просканированная",
и при повторном запуске не будет сканироваться повторно:
```bash
./vksearchactivities.py --access-token XXXYYYZZZ --target-id ID --state-file state.txt --activities-file activities.txt --activities-detail-file detail.txt --search-user-depth 0 --search-group-depth 0 --enable-scan-himself --disable-scan-photos --disable-scan-photocomments --disable-scan-videos --disable-scan-topics
```

## Удаление вашей активности (vkdeleteactivities.py)
```
== vkdeleteactivities.py - v.0.1.1  ==
Usage: 
    vkdeleteactivities.py --access-token <> --activities-file <>
```

После того, как вы произвели поиск вашей активности и получили файл activities.txt вам следует запустить:
```bash
vkdeleteactivities.py --access-token XXXYYYZZZ --activities-file activities.txt
```
    
Не забудьте подставьте вместо XXXYYYZZZ ваш access_token.

**ВНИМАНИЕ! После выполнения данной команды восстановить данные хоть и будет возможно,
но готового скрипта я не написал, и не планирую =)**

## Заключение
Поздравляем! Теперь все, что вы когда-либо писали (конечно, из того, что удалось отыскать), более недоступно
пользователям социальной сети. Впредь будьте бдительны и осторожны в ваших высказываниях. Ведь
слово, как говорится, не воробей...

P.S.: предложения, пожелания, ошибки - в https://github.com/AlekseyDurachenko/vkdevastator/issues.
