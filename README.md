vkDevastator
============

Набор скриптов позволяющий найти и удалить всю* вашу активность** из социальной сети ВКонтакте.

(*) поиск происходит путем полного перебора групп и друзей, если вас ничто не связывает с пользователем или группой,
то найти вашу активность не представляется возможным.

(**) на данный момент поддерживаются: фотографии, комментарии к фотографиям, видео, комментарии к видео, заметки, 
комментарии к заметкам, обсуждения, комментарии к обсуждениям, записи на стене и комментарии к записям на стене.

Рекомендации
------------
* Если вы совершили некоторую активность в группе или в профиле пользователя - не удаляйте их (группу, пользователя).
В дальнейшем это облегчит поиск и удаление вашей активности.

Установка и запуск
------------------
Для загрузки скрипта вам потребуется git а так же python 2.x для запуска

В Debian/Ubuntu поставить их можно следующим образом:
    
    sudo apt-get install git python

Загрузка и установка скрипта:

    cd ~
    git clone https://github.com/AlekseyDurachenko/vkDevastator vkDevastator
    
Запуск скрипта

    cd ~/vkDevastator/src
    #python ./vksearchactivities.py --access-token XXXYYYZZZ --target-id ID --state-file state.txt --activities-file activities.txt --activities-detail-file detail.txt
    #vkdeleteactivities.py --access-token XXXYYYZZZ --activities-file activities.txt
    
Получение ACCESS TOKEN
----------------------
* Во-первых, вам необходимо зарегистрировать новое приложение типа **Standalone-приложение** 
(http://vk.com/editapp?act=create), или использовать уже имеющееся. 
Так или иначе вам потребуется его уникальный **APP_ID**. 
* После того, как вам стал известен ваш **APP_ID** следует пройти OAuth авторизацию для получения access_token.
Для этого перейдите по ссылке https://oauth.vk.com/authorize?client_id=APP_ID&scope=friends,photos,audio,video,docs,notes,pages,status,wall,groups,offline&display=page&redirect_uri=https://oauth.vk.com/blank.html&response_type=token& 
и авторизируйтесь(вместо **APP_ID** поставьте ID вашего приложения). 
В случае успешной авторизации в адресной строке вы увидите access_token=XXXYYYZZZ. 
Запомните это значение в дальнейшем оно вам потребуется неоднократно.
    
    **Примечание! Перед получением access_token следуе выйти из ВКонтакте или открыть приватную вкладку.**

Поиск вашей активности (vksearchactivities.py)
----------------------------------------------

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

Данный скрипт используется для поиска всей вашей активности. В простейшем случае запуск осуществляется следующим образом:

    python ./vksearchactivities.py --access-token XXXYYYZZZ --target-id ID --state-file state.txt --activities-file activities.txt --activities-detail-file detail.txt

Подставьте в этот скрипт вместо XXXYYYZZZ ваш access_token а вместо ID ваш идентификатор пользователя ВКонтакте
(узнать его можно на странице http://vk.com/settings в поле "Номер страницы"). 
В результате поиск вашей активности будет произведен во всех ваших группах, друзьях, подписчиках и подписках. 

* Ознакомиться с результатами поиска можно в файле detail.txt
* Эти же результаты, но в машинно читаемом виде хранятся в файле activities.txt
* В файле state.txt хранятся идентификаторы пользователь и групп, которые уже были проверены на наличие вашей активности.
Если вы хотите произвести поиск заново - просто удалите этот файл.
* Скрипт можно остановить с помощью CTRL+C. Когда вы запустите его вновь поиск продолжится с места остановки.

Иногда бывает недостаточно проверки только своих групп и своих друзей. На этот случай предоставляется возможность
искать группы друзей, друзей друзй, группы друзей друзей и т.п. За это отвечают параметры --search-user-depth N,
--search-group-depth N. Где N - глубина поиска. "0" означает, что проверка друзей/групп не производится. "1" означет
что поиск производится только в своих группах/друзьях. "2" означает, что поиск друзей/групп производится у друзей 
и так далее.

    python ./vksearchactivities.py --access-token XXXYYYZZZ --target-id ID --state-file state.txt --activities-file activities.txt --activities-detail-file detail.txt -search-user-depth 1 --search-group-depth 2

В данном случае поиск будет произведен в ваших группах, друзьях, подписчиках, подписках а так же в 
группах друзей, подписчиков, подписках.

Если в группе слишком много участников, то это, как правило, означает большое кол-во контента, а следовательно
и поиск вашей активности может затянуться надолго. Чтобы этого избежать рекомендуется исключить поиск в группах
с кол-во участников превышающим определенное число. Сделать это можно при помощи --limit-member-count N,
где N максимальное кол-во участников в группе.

    python ./vksearchactivities.py --access-token XXXYYYZZZ --target-id ID --state-file state.txt --activities-file activities.txt --activities-detail-file detail.txt --search-user-depth 1 --search-group-depth 2 --limit-member-count 1000

Бывает так, что некоторые пользователи или группы имеют слишком большую стену,
слишком много фотографий и т.п., что приводит к очень долгому сканированию
данного пользователя(группы). Чтобы этого избежать, достаточно задать 
колюч --scan-time-limit N, где N - кол-во минут, которое допускается потратить
на одного пользователя(группу). Если сканирование провести не удалось, то
пользователь(группа) пропускается а ее id помечается как "просканированная",
и при повторном запуске не будет сканироваться повторно.

    ./vksearchactivities.py --access-token XXXYYYZZZ --target-id ID --state-file state.txt --activities-file activities.txt --activities-detail-file detail.txt --search-user-depth 0 --search-group-depth 0 --enable-scan-himself --disable-scan-photos --disable-scan-photocomments --disable-scan-videos --disable-scan-topics
    
    Таким образом вы можете очистить свою стену. (не забудьте, что после данной команды потребуется так же выполнить vkdeleteactivities.py)

Удаление вашей активности (vkdeleteactivities.py)
-------------------------------------------------

    == vkdeleteactivities.py - v.0.1.1  ==
    Usage: 
        vkdeleteactivities.py --access-token <> --activities-file <>

После того, как вы произвели поиск вашей активности и получили файл activities.txt вам следует запустить:

    vkdeleteactivities.py --access-token XXXYYYZZZ --activities-file activities.txt
    
Подставьте в этот скрипт вместо XXXYYYZZZ ваш access_token.

***ВНИМАНИЕ! После выполнение этой команды восстановить вашу активность хоть и будет возможно,
но готового скрипта я пока еще не написал, и не планирую =)***

Заключение
----------

Поздравляем! Теперь все, что вы когда-либо писали (конечно, из того, что получилось отыскать), более недоступно
пользователям социальной сети. Впредь будьте бдительны и осторожны в ваших высказываниях. Ведь
слово, как говорится, не воробей...

P.S.: предложения, пожелания, ошибки - в багтрекер.
