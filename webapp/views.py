from .models import *
from django.http import HttpResponse, JsonResponse, Http404
from .forms import SignupForm
import logging
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .models import User, Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Buy_list, Uploaded_product, User  # 올바른 모델 가져오기
from django.utils import timezone
from functools import wraps
from django.shortcuts import render, redirect
from .models import Event, GoodExamples, Notice
from django.utils.timezone import now


# Create your views here.
logger = logging.getLogger('webapp')


def session_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('webapp:login')
        return view_func(request, *args, **kwargs)
    return wrapper
#시연
def index(request):
    users=User.objects.all().order_by('uid')
    products=Product.objects.all().order_by('pid')
    context={'users':users,'products':products}
    return render(request,'index.html',context)

def header(request):
    user=User.objects.get(id=request.user.uid)
    context={'user':user}
    return render(request,'header.html',context)

def footer(request):
    return render(request,'footer.html')

def main(request):
    products = Product.objects.filter(status=2).order_by('-pid')[:4]
    good_examples=GoodExamples.objects.order_by('id')[:3]
    notices=Notice.objects.order_by('id')[:1]
    events=Event.objects.order_by('id')[:2]
    context={'products':products,'good_examples':good_examples,'notices':notices,'events':events}
    #if products.
    return render(request,'main.html',context)

def notice(request):
    #db에서 뭘 가져온 다음에
    notices=Notice.objects.all().order_by('-id')
    context={'notices':notices}
    return render(request,'notice.html',context)

def notice_detail(request,notice_id):
    notice=get_object_or_404(Notice,id=notice_id)
    notice.count+=1
    notice.save()
    context={'notice':notice}
    return render(request,'notice-detail.html',context)

def manage(request):
    context={'var':'hello'}
    return render(request,'manage.html',context);

def login_before(request):
    context={'var':'hello'}
    return render(request,'login-before.html',context)

def faq(request):
    context={'var':'hello'}
    return render(request,'faq.html',context)

def donate_service(request):
    context={'var':'hello'}
    return render(request,'donate-service.html',context);

#승윤==================================================
from django.core.exceptions import ObjectDoesNotExist
def donate_detail(request):
    product_id = request.GET.get('product_id')
    user_auth = -1
    uid = None

    if product_id:
        try:
            product = Product.objects.get(pid=product_id)
        except Product.DoesNotExist:
            return Http404("Product not found")

        p_image = product.p_image
        p_description = product.description
        p_name = product.p_name
        p_cost = product.cost
        p_category = product.category

        try:
            u_product = Uploaded_product.objects.get(pid=product_id)
        except Uploaded_product.DoesNotExist:
            return Http404("Uploaded product not found")

        uploaded_date = u_product.updated_date
        seller_id = u_product.uid.uid  # User 객체의 실제 UID 값 사용

        if request.session.items():
            uid = request.session.get('user_id')
            try:
                user_auth = User.objects.get(uid=uid).authorization
            except User.DoesNotExist:
                user_auth = -1

        context = {
            'product_id': product_id,
            'p_image': p_image,
            'p_description': p_description,
            'p_name': p_name,
            'p_cost': p_cost,
            'p_category': p_category,
            'p_date': uploaded_date,
            'seller_id': seller_id,  # 이제는 seller_id가 User 객체의 UID 값입니다.
            'user_auth': user_auth,
            'user_id': uid
        }

        return render(request, 'donate-detail.html', context)
    else:
        return Http404("Error")

def donate_apply(request):
    context={'var':'hello'}
    return render(request,'donate-apply.html',context)

@session_login_required
def save_product(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        p_name = request.POST.get('item_name')
        p_image = request.FILES.get('image')
        cost = 0
        description = request.POST.get('content')
        status = 0

        if not all([category, p_name, p_image, description]):
            return render(request, 'donate-apply.html', {
                'error': '모든 필드 입력 필요'
            })

        # 세션에서 user_id 가져오기
        user_id = request.session.get('user_id')
        print("user_id:", user_id)
        if not user_id:
            return redirect('webapp:login')

        # User 객체 가져오기
        user = get_object_or_404(User, uid=user_id)

        # Product 모델에 새로운 데이터 저장
        try:
            product = Product.objects.create(
                category=int(category),
                p_name=p_name,
                p_image=p_image,
                cost=cost,
                description=description,
                status=status
            )
            product.save()
            print(f"Product 저장 완료: {product.pk}")
            print(f"User 객체: {user}")

        except Exception as e:
            print(f"Product 저장 실패: {e}")
            return render(request, 'donate-apply.html', {'error': 'Product 저장 중 오류 발생'})

        # Uploaded_product 모델에 데이터 저장
        try:
            uploaded=Uploaded_product.objects.create(
                uid=user,  # User 객체
                pid=product,  # Product 객체
                created_date=time_now(),
                updated_date=time_now()
            )
            uploaded.save()
            print("Uploaded_product 저장 성공")
        except Exception as e:
            print(f"Uploaded_product 저장 오류: {e}")
            return render(request, 'donate-apply.html', {'error': 'Uploaded_product 저장 중 오류 발생'})

        return redirect('webapp:donation_success')

    return render(request, 'donate-apply.html')

def donation_success(request):
    return render(request, 'donation-success.html')

def donate_category(request):
    products=Product.objects.all().order_by('pid')
    context={'products':products}
    return render(request,'donate-category.html',context)

def payment(request):
    if request.method == 'GET':
        uid = request.GET.get('uid')
        pid = request.GET.get('pid')

        uploaded_product = Uploaded_product.objects.get(pid=pid)
        seller_id = uploaded_product.uid.uid
        context = {'seller_id': seller_id, 'pid': pid, 'uid': uid}
        return render(request, 'payment.html', context)

def payment_success(request):

    return render(request, 'payment_success.html')

#흥주=================================================
def business_introduce(request):
    context={'var':'hello'}
    return render(request,'business-introduce.html',context)

def certificate(request):
        user_id=request.session.get('user_id')  # 현재 로그인한 사용자
        user = get_object_or_404(User, uid=user_id)

        context = {
            'user': user,
            'current_date': now().strftime('%Y년 %m월 %d일'),
        }
        return render(request, 'certificate.html', context)

def event(request):
    events=Event.objects.all().order_by('-id')
    context={'events':events}
    return render(request,'event.html',context)

def event_detail(request,event_id):
    event = get_object_or_404(Event, id=event_id)

    # 조회수 증가
    event.count += 1
    event.save()
    return render(request,'event-detail.html', {'event':event})

def good_example(request):
    context={'var':'hello'}
    return render(request,'good-example.html',context)

@session_login_required
def mypage(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, uid=user_id)

    # 구매 목록
    purchases = Buy_list.objects.select_related('pid__pid').filter(buyer_id=user).order_by('-buy_date')
    # 기부 신청 내역
    donations = Uploaded_product.objects.filter(uid=user).order_by('-created_date')

    # 기부 물품 목록
    donated_items = Uploaded_product.objects.filter(uid=user, pid__status=1).order_by('-created_date')

    context = {
        'user': user,
        'purchases': purchases,
        'donations': donations,
        'donated_items': donated_items,

    }

    return render(request, 'mypage.html', context)

#나===================
def login_view(request):
    if request.session.get('user_id'):
        return redirect('webapp:main')

    if request.method=="POST":
        user_id=request.POST.get("user_id")
        password=request.POST.get("password")

        try:
            user=User.objects.get(id=user_id)

            if user.pw==password:
                request.session["user_id"]=user.uid
                request.session["user_name"]=user.name
                print(f"세션 저장: user_id={user.uid}, user_name={user.name}")  # 디버깅용 출력
                print("auth값: ",user.authorization)
                #context ={'user':user}
                return redirect("webapp:main")
                # return redirect("webapp:main")

            else:
                return render(request,"login.html",{"error":"비밀번호가 틀렸습니다."})
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "존재하지 않는 id입니다."})

    return render(request,'login.html')

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return redirect('webapp:login')  # 회원가입 성공 후 로그인 페이지로 이동
        else:
            return render(request, 'signup.html', {'form': form})  # 유효성 검증 실패 시 다시 렌더링
    else:
        form = SignupForm()
    success=request.GET.get('success',None)
    return render(request, 'signup.html', {'form': form,'success':success})

def logout_view(request):
    request.session.clear()  # 세션 삭제
    request.session['logout_message'] = "로그아웃되었습니다."  # 메시지 저장
    return redirect('webapp:main')

def clear_message(request):
    if request.method == "POST":
        request.session.pop('logout_message', None)  # 메시지 삭제
        return JsonResponse({"success": True})



@session_login_required
def admin_page(request):
    # 관리자 페이지에 필요한 데이터 가져오기
    users = User.objects.all()
    products = Product.objects.all()
    donations = Uploaded_product.objects.all()

    context = {
        'users': users,
        'products': products,
        'donations': donations,
    }
    return render(request, 'admin_page.html', context)



@csrf_exempt
def approve_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user.authorization = 1
        user.save()
        return JsonResponse({'status': 'success', 'message': 'User approved'})

@csrf_exempt
def reject_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user.authorization = 0
        user.save()
        return JsonResponse({'status': 'success', 'message': 'User rejected'})

@csrf_exempt
def approve_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pid=product_id)
        product.status = 2
        product.save()
        return JsonResponse({'status': 'success', 'message': 'Product approved'})

@csrf_exempt
def reject_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pid=product_id)
        product.status = 1
        product.save()
        return JsonResponse({'status': 'success', 'message': 'Product rejected'})

@csrf_exempt
def cancel_approval(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pid=product_id)
        product.status = 0
        product.save()
        return JsonResponse({'status': 'success', 'message': 'Approval cancelled'})

@csrf_exempt
def cancel_rejection(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pid=product_id)
        product.status = 0
        product.save()
        return JsonResponse({'status': 'success', 'message': 'Rejection cancelled'})

#donate_category페이지에서 사용.
def get_products(request):
    category = request.GET.get('category', 'all')
    status = request.GET.get('status', None)
    page = int(request.GET.get('page', 1))

    # 기본 쿼리셋: 승인된 상품만 필터
    products = Product.objects.filter(status=2)

    # 카테고리 필터
    if category != 'all':
        products = products.filter(category=category)

    # 페이지네이션
    paginator = Paginator(products, 12)  # 페이지당 12개 상품 표시
    try:
        current_page = paginator.page(page)
    except Exception:
        return JsonResponse({'products': [], 'page': page, 'total_pages': paginator.num_pages})

    # JSON 형태로 반환
    product_list = [
        {
            'id': product.pid,
            'name': product.p_name,
            'price': product.cost,
            'category': product.category,
            'image': product.p_image.url
        }
        for product in current_page.object_list
    ]

    return JsonResponse({
        'products': product_list,
        'page': current_page.number,
        'total_pages': paginator.num_pages
    })




@csrf_exempt
def process_payment(request):
    """
    결제 요청을 처리하고 데이터를 데이터베이스에 저장.
    """
    if request.method == 'POST':
        try:
            # POST 요청에서 데이터 가져오기
            uid = request.POST.get('uid')
            pid = request.POST.get('pid')
            seller_id = request.POST.get('seller_id')
            pay_method = request.POST.get('pay_method')

            # 필수 매개변수 확인
            if not all([uid, pid, seller_id, pay_method]):
                return JsonResponse({'error': 'Missing parameters'}, status=400)

            # 사용자 (buyer) 조회
            try:
                buyer = User.objects.get(uid=uid)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Buyer not found'}, status=404)

            # 판매자 (seller) 조회
            try:
                seller = User.objects.get(uid=seller_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Seller not found'}, status=404)

            # 상품 (product) 조회
            try:
                product = Uploaded_product.objects.get(pid=pid)
            except Uploaded_product.DoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=404)

            # 데이터베이스에 Buy_list 객체 생성 및 저장
            try:
                buy_entry = Buy_list(
                    buyer_id=buyer,
                    seller_id=seller,
                    pid=product,
                    pay_method=int(pay_method),
                    buy_date=timezone.now(),
                )
                buy_entry.save()  # DB에 저장

                product.pid.status = 3 # product 상태변경
                product.pid.save()

            except Exception as e:
                return JsonResponse({'error': f'Error saving Buy_list: {str(e)}'}, status=500)

            # 성공 응답 반환
            return JsonResponse({'message': 'Payment successful'}, status=200)

        except Exception as e:
            # 예외 발생 시 전체 오류 응답 반환
            return JsonResponse({'error': f'Critical error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)




# View for managing events
def manage_events(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        mileage_price = request.POST.get('mileage_price', 0)
        event_image = request.FILES.get('event_image', None)

        Event.objects.create(
            title=title,
            content=content,
            mileage_price=mileage_price,
            event_image=event_image,
            count=0
        )
        return redirect('webapp:manage_events')

    events = Event.objects.all()
    return render(request, 'manage_events.html', {'events': events})


# View for managing good examples
def manage_good_examples(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        event_image = request.FILES.get('event_image', None)

        GoodExamples.objects.create(
            title=title,
            content=content,
            event_image=event_image
        )
        return redirect('webapp:manage_good_examples')

    good_examples = GoodExamples.objects.all()
    return render(request, 'manage_good_examples.html', {'good_examples': good_examples})


# View for managing notices
def manage_notices(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']

        Notice.objects.create(
            title=title,
            content=content,
            count=0
        )
        return redirect('webapp:manage_notices')

    notices = Notice.objects.all()
    return render(request, 'manage_notices.html', {'notices': notices})



def update_product(request, pid):
    product = get_object_or_404(Product, pid=pid)

    if request.method == 'POST':
        # 수정된 데이터 저장
        product.p_name = request.POST.get('p_name')
        product.cost = request.POST.get('cost')
        product.description = request.POST.get('description')
        if 'p_image' in request.FILES:
            product.p_image = request.FILES['p_image']
        product.status=0
        product.save()
        return redirect('webapp:mypage')  # 수정 완료 후 마이페이지로 리다이렉트

    return render(request, 'update_product.html', {'product': product})


def update_notice(request, notice_id):
    # 공지사항 객체 가져오기
    notice = get_object_or_404(Notice, id=notice_id)

    if request.method == 'POST':
        # 수정된 데이터 저장
        notice.title = request.POST.get('title')
        notice.content = request.POST.get('content')
        notice.save()

        return redirect('webapp:manage_notices')  # 수정 후 공지사항 목록 페이지로 리다이렉트

    return render(request, 'update_notice.html', {'notice': notice})


def delete_product(request, pid):
    """
    물건 삭제 뷰.
    대기중(0) 또는 반려(1) 상태의 물건만 삭제 가능.
    """
    uploaded_product = get_object_or_404(Uploaded_product, pid=pid)
    product=uploaded_product.pid
    # 상태 확인 (대기중 또는 반려)
    if product.status in [0, 1]:
        product.status=-1
        product.save()
        return redirect('webapp:mypage')  # 삭제 후 마이페이지로 리다이렉트
    else:
        return redirect('webapp:mypage')  # 상태가 삭제 불가능할 경우 리다이렉트


def update_good_example(request, example_id):
    # 좋은 예시 객체 가져오기
    good_example = get_object_or_404(GoodExamples, id=example_id)

    if request.method == 'POST':
        # 수정된 데이터 저장
        good_example.title = request.POST.get('title')
        good_example.content = request.POST.get('content')
        if 'event_image' in request.FILES:
            good_example.event_image = request.FILES['event_image']
        good_example.save()

        return redirect('webapp:manage_good_examples')  # 수정 후 목록 페이지로 리다이렉트

    return render(request, 'update_good_example.html', {'good_example': good_example})


def update_event(request, event_id):
    # 이벤트 객체 가져오기
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        # 수정된 데이터 저장
        event.title = request.POST.get('title')
        event.content = request.POST.get('content')
        event.mileage_price = request.POST.get('mileage_price')
        if 'event_image' in request.FILES:
            event.event_image = request.FILES['event_image']
        event.save()

        return redirect('webapp:manage_events')  # 수정 후 목록 페이지로 리다이렉트

    return render(request, 'update_event.html', {'event': event})


def delete_notice(request, notice_id):
    # 공지사항 삭제
    notice = get_object_or_404(Notice, id=notice_id)
    notice.delete()
    return redirect('webapp:manage_notices')  # 삭제 후 공지사항 목록으로 리다이렉트

def delete_good_example(request, example_id):
    # 좋은 예시 삭제
    good_example = get_object_or_404(GoodExamples, id=example_id)
    good_example.delete()
    return redirect('webapp:manage_good_examples')  # 삭제 후 좋은 예시 목록으로 리다이렉트

def delete_event(request, event_id):
    # 이벤트 삭제
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('webapp:manage_events')  # 삭제 후 이벤트 목록으로 리다이렉트

def event_apply(request, event_id):
    if request.method == "POST":
        user = request.user
        event_id = request.POST.get("event_id")
        mileage_required = int(request.POST.get("mileage_required"))

        # 유저 인증 여부 확인
        if not user.is_authenticated:
            return JsonResponse({"status": "error", "message": "로그인이 필요합니다."}, status=403)

        # 이벤트 가져오기
        event = get_object_or_404(Event, id=event_id)

        # 마일리지 부족 확인
        if user.mileage < mileage_required:
            return JsonResponse({"status": "error", "message": "마일리지가 부족합니다."}, status=400)

        # 이벤트 신청 처리
        Event_User_List.objects.create(uid=user, event_id=event)

        # 유저 마일리지 차감
        user.mileage -= mileage_required
        user.save()

        return JsonResponse({"status": "success"}, status=200)

    return JsonResponse({"status": "error", "message": "잘못된 요청입니다."}, status=400)