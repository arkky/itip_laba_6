from articles.models import Article
from django.http import Http404, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def archive(request: HttpRequest):
    return render(request, 'archive.html', {"posts": Article.objects.all(), 'request': request})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post, 'request': request})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    if not request.user.is_anonymous:
        # Здесь будет основной код представления
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
                if not Article.objects.filter(title=form['title']):
                    article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('get_article', article_id=article.id)
                else:
                    form['errors'] = u"Такая статья уже существует"
                    return render(request, 'create_post.html', {'form': form, 'request': request})
                # перейти на страницу поста
            else:
                # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form, 'request': request})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {'reqeust': request})
    else:
        raise Http404

def register(request: HttpRequest):
    form = {}
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            email = request.POST["email"]
            if username and password and email:
                try:
                    User.objects.get(username=username)
                    form['errors'] = f'Пользователь с таким никнеймом {username} уже зарегистрирован'
                    return render(request, 'register.html', {'form': form, 'request': request})
                except User.DoesNotExist:
                    User.objects.create_user(username, email, password)
                    print("redirect?")
                    return redirect('archive')
            else:
                form['errors'] = "Поля должны быть заполнены!"
                return render(request, 'register.html', {'form': form, 'request': request})
        else:
            return render(request, 'register.html', {'request': request})
    else:
        return redirect('archive')

def login_view(request: HttpRequest):
    form = {}
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            if username and password:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('archive')
                else:
                    form['errors'] = "Вы указали неверный логин/пароль"
                    return render(request, 'login.html', {'form': form, 'request': request})
            else:
                form['errors'] = "Поля должны быть заполнены!"
                return render(request, 'login.html', {'form': form, 'request': request})
        else:
            return render(request, 'login.html', {'request': request})
    else:
        return redirect('archive')