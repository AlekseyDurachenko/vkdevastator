vkDevastator
============

Набор скриптов позволяющий найти и удалить всю* вашу активность** из социальной сети ВКонтакте.

(*) поиск происходит путем полного перебора групп и друзей, если вас ничто не связывает с пользователем или группой,
то найти вашу активность не представляется возможным.

(**) на данный момент поддерживаются: фотографии, комментарии к фотографиям, видео, комментарии к видео, заметки, 
комментарии к заметкам, обсуждения, комментарии к обсуждениям, записи на стене и комментарии к записям на стене.


Получение ACCESS TOKEN
----------------------
* Во первых, вам необходимо зарегистрировать новое приложение типа **Standalone-приложение** 
(http://vk.com/editapp?act=create), или использовать уже имеющееся. 
Так или иначе вам потребуется его уникальный **APP_ID**. 
* После того, Как вам стал известен ваш **APP_ID** следует пройти OAuth авторизацию для получения access_token.
Для этого перейдите по ссылке https://oauth.vk.com/authorize?client_id=APP_ID&scope=friends,photos,audio,video,docs,notes,pages,status,wall,groups,offline&display=page&redirect_uri=https://oauth.vk.com/blank.html&response_type=token& 
и авторизируйтесь(вместо **APP_ID** поставьте ID вашего приложения). 
В случае успешной авторизации в адресной строке вы увидите access_token=XXXYYYZZZ. 
Запомните это значение в дальнейшем оно вам потребуется неоднократно.
    
    **Примечание! Перед получением access_token следуе выйти из ВКонтакте или открыть приватную вкладку.**

Поиск вашей активности (vksearchactivities.py)
----------------------------------------------

    == vksearchactivities.py - v.0.1.0  ==
    Usage: 
        vksearchactivities.py --access-token <> --target-id <> --state-file <> --activities-file <> --activities-detail-file <>
    
        --log-file <>   Path to the log file
        --search-user-depth  N   (default 1) The users search depth
        --search-group-depth N   (default 1) The groups search depth
        --custom-user-ids    N   The list of custom user_id splitted by ","
        --custom-group-ids   N   The list of custom group_id splitted by "," (positive values)
        --disable-scan-friends   Ignore the friends
        --disable-scan-friends   Ignore the followers
        --disable-scan-user-subscriptions   Ignore the subscriptions to users
        --disable-scan-group-subscriptions  Ignore the subscriptions to groups
        --show-api-queries   Show the API queries
        --show-api-errors    Show the API errors

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
