Для добавления новой модели необходимо в файл models/model добавить класс с описанием, далее выполнить команду

python -m alembic revision --autogenerate -m "{{Название миграции}}" && python -m alembic upgrade head

Необходимо помнить что дальнейшее переименование полей сгенерит миграцию которая УДАЛИТ старую колонку и создаст новую.

Для отката одной последней миграции команда

python -m alembic downgrade -1


Далее необходимо создать папку с апкой, в проекте можно склонить example

для того чтобы апка начала работать необходимо в api/router импортировать endpoints апки
полный рабочий CRUD прилагается.


python -m uvicorn main:app --reload

docker build --no-cache -t templ -f ./dockerfiles/Dockerfile .


python -m alembic revision --autogenerate -m "1" && python -m alembic upgrade head