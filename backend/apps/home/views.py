from django.shortcuts import render
from django.db.models import Sum, Prefetch, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, exceptions
from .models import StatisticsValues, LsClaimList, ClPersonList, ClOap, LsEventList
from .serializers import ClaimsSerializer


def ap(request):
    return render(request, 'home/ap.html')


@api_view(['GET'])
def ap_statistics(request):
    # Фильтр БД по датам
    statistics_queryset = StatisticsValues.objects.filter(
        timekey__fulldatealternatekey__gte=request.GET['date_from'],
        timekey__fulldatealternatekey__lte=request.GET['date_to'],
        objtype_id__in=(1, 2)
    )
    # Подано фіз.
    applied_phys = statistics_queryset.filter(cert_id__in=(1, 2), legalkind_id=0).count()
    # Подано юр.
    applied_jur = statistics_queryset.filter(cert_id__in=(1, 2), legalkind_id=1).count()
    # Зареєстровано фіз.
    registered_phys = statistics_queryset.filter(cert_id=7, legalkind_id=0).count()
    # Зареєстровано юр.
    registered_jur = statistics_queryset.filter(cert_id=7, legalkind_id=1).count()
    # Без розгляду фіз.
    without_review_phys = statistics_queryset.filter(cert_id=22, legalkind_id=0).count()
    # Без розгляду юр.
    without_review_jur = statistics_queryset.filter(cert_id=22, legalkind_id=1).count()
    # Відмова фіз.
    refusal_phys = statistics_queryset.filter(cert_id=9, legalkind_id=0).count()
    # Відмова юр.
    refusal_jur = statistics_queryset.filter(cert_id=9, legalkind_id=1).count()
    # Повернено фіз.
    return_phys = statistics_queryset.filter(cert_id=13, legalkind_id=0).count()
    # Повернено юр.
    return_jur = statistics_queryset.filter(cert_id=13, legalkind_id=1).count()
    # Відхилено фіз.
    canceled_phys = statistics_queryset.filter(cert_id=11, legalkind_id=0).count()
    # Відхилено юр.
    canceled_jur = statistics_queryset.filter(cert_id=11, legalkind_id=1).count()
    # Видано фіз.
    issued_phys = statistics_queryset.filter(cert_id=5, legalkind_id=0).aggregate(Sum('value'))['value__sum'] or 0
    # Видано юр.
    issued_jur = statistics_queryset.filter(cert_id=5, legalkind_id=1).aggregate(Sum('value'))['value__sum'] or 0

    return Response({
        "applied_phys": applied_phys,
        "applied_jur": applied_jur,
        "registered_phys": registered_phys,
        "registered_jur": registered_jur,
        "without_review_phys": without_review_phys,
        "without_review_jur": without_review_jur,
        "refusal_phys": refusal_phys,
        "refusal_jur": refusal_jur,
        "return_phys": return_phys,
        "return_jur": return_jur,
        "canceled_phys": canceled_phys,
        "canceled_jur": canceled_jur,
        "issued_phys": issued_phys,
        "issued_jur": issued_jur,
    })


class ApClaimsListView(generics.ListAPIView):

    serializer_class = ClaimsSerializer

    def get_queryset(self):
        queryset = LsClaimList.objects.prefetch_related(
            Prefetch(
                'persons',
                queryset=ClPersonList.objects.filter(linkclaimpersons__id_type_person__in=(1, 5))
            ),
            Prefetch(
                'objtype'
            ),
            Prefetch(
                'oap'
            ),
            Prefetch(
                'events',
                queryset=LsEventList.objects.prefetch_related(
                    Prefetch('user'),
                    Prefetch('event_type'),
                )
            ),
        ).filter(
            objtype_id__in=(1, 2)
        ).order_by('appnumber')

        # Дата від
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        app_type = self.request.query_params.get('appType', None)
        cert_id = None
        legalkind_id = None
        if app_type == 'applied_phys':
            cert_id = (1, 2)
            legalkind_id = 0
        elif app_type == 'applied_jur':
            cert_id = (1, 2)
            legalkind_id = 1
        elif app_type == 'registered_phys':
            cert_id = (7,)
            legalkind_id = 0
        elif app_type == 'registered_jur':
            cert_id = (7,)
            legalkind_id = 1
        elif app_type == 'without_review_phys':
            cert_id = (22,)
            legalkind_id = 0
        elif app_type == 'without_review_jur':
            cert_id = (22,)
            legalkind_id = 1
        elif app_type == 'refusal_phys':
            cert_id = (9,)
            legalkind_id = 0
        elif app_type == 'refusal_jur':
            cert_id = (9,)
            legalkind_id = 1
        elif app_type == 'return_phys':
            cert_id = (13,)
            legalkind_id = 0
        elif app_type == 'return_jur':
            cert_id = (13,)
            legalkind_id = 1
        elif app_type == 'canceled_phys':
            cert_id = (11,)
            legalkind_id = 0
        elif app_type == 'canceled_jur':
            cert_id = (11,)
            legalkind_id = 1
        elif app_type == 'issued_phys':
            cert_id = (5,)
            legalkind_id = 0
        elif app_type == 'issued_jur':
            cert_id = (5,)
            legalkind_id = 1

        if date_from and date_to and app_type:
            try:
                queryset = queryset.filter(
                    statisticsvalues__timekey__fulldatealternatekey__gte=date_from,
                    statisticsvalues__timekey__fulldatealternatekey__lte=date_to,
                    statisticsvalues__cert_id__in=cert_id,
                    statisticsvalues__legalkind_id=legalkind_id
                )
            except:
                raise exceptions.ParseError("Невірне значення параметру date_from")

        return queryset


def dg(request):
    return render(request, 'home/dg.html')


@api_view(['GET'])
def dg_statistics(request):
    # Фильтр БД по датам
    statistics_queryset = StatisticsValues.objects.filter(
        timekey__fulldatealternatekey__gte=request.GET['date_from'],
        timekey__fulldatealternatekey__lte=request.GET['date_to'],
    )

    alienation_applied_phys = statistics_queryset.filter(cert_id__in=(3, 4), legalkind_id=0, objtype_id=3).count()
    alienation_applied_jur = statistics_queryset.filter(cert_id__in=(3, 4), legalkind_id=1, objtype_id=3).count()
    using_applied_phys = statistics_queryset.filter(cert_id__in=(3, 4), legalkind_id=0, objtype_id=4).count()
    using_applied_jur = statistics_queryset.filter(cert_id__in=(3, 4), legalkind_id=1, objtype_id=4).count()

    alienation_registered_phys = statistics_queryset.filter(cert_id=8, legalkind_id=0, objtype_id=3).count()
    alienation_registered_jur = statistics_queryset.filter(cert_id=8, legalkind_id=1, objtype_id=3).count()
    using_registered_phys = statistics_queryset.filter(cert_id=8, legalkind_id=0, objtype_id=4).count()
    using_registered_jur = statistics_queryset.filter(cert_id=8, legalkind_id=1, objtype_id=4).count()

    alienation_without_review_phys = statistics_queryset.filter(cert_id=23, legalkind_id=0, objtype_id=3).count()
    alienation_without_review_jur = statistics_queryset.filter(cert_id=23, legalkind_id=1, objtype_id=3).count()
    using_without_review_phys = statistics_queryset.filter(cert_id=23, legalkind_id=0, objtype_id=4).count()
    using_without_review_jur = statistics_queryset.filter(cert_id=23, legalkind_id=1, objtype_id=4).count()

    alienation_refusal_phys = statistics_queryset.filter(cert_id=10, legalkind_id=0, objtype_id=3).count()
    alienation_refusal_jur = statistics_queryset.filter(cert_id=10, legalkind_id=1, objtype_id=3).count()
    using_refusal_phys = statistics_queryset.filter(cert_id=10, legalkind_id=0, objtype_id=4).count()
    using_refusal_jur = statistics_queryset.filter(cert_id=10, legalkind_id=1, objtype_id=4).count()

    alienation_return_phys = statistics_queryset.filter(cert_id=14, legalkind_id=0, objtype_id=3).count()
    alienation_return_jur = statistics_queryset.filter(cert_id=14, legalkind_id=1, objtype_id=3).count()
    using_return_phys = statistics_queryset.filter(cert_id=14, legalkind_id=0, objtype_id=4).count()
    using_return_jur = statistics_queryset.filter(cert_id=14, legalkind_id=1, objtype_id=4).count()

    return Response({
        "alienation_applied_phys": alienation_applied_phys,
        "alienation_applied_jur": alienation_applied_jur,
        "using_applied_phys": using_applied_phys,
        "using_applied_jur": using_applied_jur,

        "alienation_registered_phys": alienation_registered_phys,
        "alienation_registered_jur": alienation_registered_jur,
        "using_registered_phys": using_registered_phys,
        "using_registered_jur": using_registered_jur,

        "alienation_without_review_phys": alienation_without_review_phys,
        "alienation_without_review_jur": alienation_without_review_jur,
        "using_without_review_phys": using_without_review_phys,
        "using_without_review_jur": using_without_review_jur,

        "alienation_refusal_phys": alienation_refusal_phys,
        "alienation_refusal_jur": alienation_refusal_jur,
        "using_refusal_phys": using_refusal_phys,
        "using_refusal_jur": using_refusal_jur,

        "alienation_return_phys": alienation_return_phys,
        "alienation_return_jur": alienation_return_jur,
        "using_return_phys": using_return_phys,
        "using_return_jur": using_return_jur,
    })


class DgClaimsListView(generics.ListAPIView):

    serializer_class = ClaimsSerializer

    def get_queryset(self):
        queryset = LsClaimList.objects.prefetch_related(
            Prefetch(
                'persons',
                queryset=ClPersonList.objects.filter(linkclaimpersons__id_type_person__in=(1, 5))
            ),
            Prefetch(
                'objtype'
            ),
            Prefetch(
                'oap'
            ),
            Prefetch(
                'events',
                queryset=LsEventList.objects.prefetch_related(
                     Prefetch('user'),
                     Prefetch('event_type'),
                 )
            ),
        ).order_by('appnumber')

        # Дата від
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        app_type = self.request.query_params.get('appType', None)
        cert_id = None
        legalkind_id = None
        objtype_id = None
        if app_type == 'alienation_applied_phys':
            cert_id = (3, 4)
            legalkind_id = 0
            objtype_id = 3
        elif app_type == 'alienation_applied_jur':
            cert_id = (3, 4)
            legalkind_id = 1
            objtype_id = 3
        elif app_type == 'using_applied_phys':
            cert_id = (3, 4)
            legalkind_id = 0
            objtype_id = 4
        elif app_type == 'using_applied_jur':
            cert_id = (3, 4)
            legalkind_id = 1
            objtype_id = 4
        elif app_type == 'alienation_registered_phys':
            cert_id = (8,)
            legalkind_id = 0
            objtype_id = 3
        elif app_type == 'alienation_registered_jur':
            cert_id = (8,)
            legalkind_id = 1
            objtype_id = 3
        elif app_type == 'using_registered_phys':
            cert_id = (8,)
            legalkind_id = 0
            objtype_id = 4
        elif app_type == 'using_registered_jur':
            cert_id = (8,)
            legalkind_id = 1
            objtype_id = 4
        elif app_type == 'alienation_without_review_phys':
            cert_id = (23,)
            legalkind_id = 0
            objtype_id = 3
        elif app_type == 'alienation_without_review_jur':
            cert_id = (23,)
            legalkind_id = 1
            objtype_id = 3
        elif app_type == 'using_without_review_phys':
            cert_id = (23,)
            legalkind_id = 0
            objtype_id = 4
        elif app_type == 'using_without_review_jur':
            cert_id = (23,)
            legalkind_id = 1
            objtype_id = 4
        elif app_type == 'alienation_refusal_phys':
            cert_id = (10,)
            legalkind_id = 0
            objtype_id = 3
        elif app_type == 'alienation_refusal_jur':
            cert_id = (10,)
            legalkind_id = 1
            objtype_id = 3
        elif app_type == 'using_refusal_phys':
            cert_id = (10,)
            legalkind_id = 0
            objtype_id = 4
        elif app_type == 'using_refusal_jur':
            cert_id = (10,)
            legalkind_id = 1
            objtype_id = 4
        elif app_type == 'alienation_return_phys':
            cert_id = (14,)
            legalkind_id = 0
            objtype_id = 3
        elif app_type == 'alienation_return_jur':
            cert_id = (14,)
            legalkind_id = 1
            objtype_id = 3
        elif app_type == 'using_return_phys':
            cert_id = (14,)
            legalkind_id = 0
            objtype_id = 4
        elif app_type == 'using_return_jur':
            cert_id = (14,)
            legalkind_id = 1
            objtype_id = 4

        if date_from and date_to and app_type:
            try:
                queryset = queryset.filter(
                    statisticsvalues__timekey__fulldatealternatekey__gte=date_from,
                    statisticsvalues__timekey__fulldatealternatekey__lte=date_to,
                    statisticsvalues__cert_id__in=cert_id,
                    statisticsvalues__legalkind_id=legalkind_id,
                    objtype_id=objtype_id
                )
            except:
                raise exceptions.ParseError("Невірне значення параметру date_from")

        return queryset


def ap_specialist_workload(request):
    return render(request, 'home/ap_specialist_workload.html')


@api_view(['GET'])
def ap_specialist_workload_statistics(request):
    return Response([
        {
            "name": 'Стельмащук Анна Василівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Мельник Ірина Федорівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Жалдак	Валерій	Олександрович',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Шкураков Сергій Олександрович',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Єсєв Володимир	Дмитрович',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Переверзенцев Олексій Юрійович',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Юречко Інна Сергіївна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Яременко Тетяна Володимирівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Більчич Ірина Володимирівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Пащенко Андрій	Валерійович',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Ігнатьєва Олена Олегівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Кузьмова Ірина	Василівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Ізотова Ірина Олександрівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Мохова	Наталія	Сергіївна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Підгурська	Людмила	Михайлівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Попов Вадим Вікторович',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Романова Ніна Петрівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Сагайда Тетяна	Вікторівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Сіра Ірина Григорівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "duplicates": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_issue": 0,
            "budget_duplicate": 0,
            "budget_changes": 0,
        },
    ])


@api_view(['GET'])
def ap_specialist_workload_claims(request):
    return Response([
        {
            'app_number': 1,
            'app_type': 2,
            'registered': 3,
            'without_registration': 4,
            'refused': 5,
            'returned': 6,
            'canceled': 7,
            'disadvantages_letters': 8,
            'reviewing': 9,
            'reviewed_total': 10,
            'average_time': 11,
            'budget_preparing': 11,
            'budget_issue': 12,
            'budget_overpayment': 13,
            'budget_duplicate': 14,
            'budget_changes': 15,
            'idclaim': 100,
        },
        {
            'app_number': 1,
            'app_type': 2,
            'registered': 3,
            'without_registration': 4,
            'refused': 5,
            'returned': 6,
            'canceled': 7,
            'disadvantages_letters': 8,
            'reviewing': 9,
            'reviewed_total': 10,
            'average_time': 11,
            'budget_preparing': 11,
            'budget_issue': 12,
            'budget_overpayment': 13,
            'budget_duplicate': 14,
            'budget_changes': 15,
            'idclaim': 100,
        }
    ])


def dg_specialist_workload(request):
    return render(request, 'home/dg_specialist_workload.html')


@api_view(['GET'])
def dg_specialist_workload_statistics(request):
    return Response([
        {
            "name": 'Стельмащук Анна Василівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Мельник Ірина Федорівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Жалдак	Валерій	Олександрович',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Шкураков Сергій Олександрович',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Єсєв Володимир Дмитрович',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Переверзенцев Олексій Юрійович',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Юречко Інна Сергіївна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Яременко Тетяна Володимирівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Більчич Ірина Володимирівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Пащенко Андрій Валерійович',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Ігнатьєва Олена Олегівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Кузьмова Ірина	Василівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Ізотова Ірина Олександрівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Мохова Наталія	Сергіївна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Підгурська Людмила Михайлівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Попов Вадим Вікторович',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Романова Ніна Петрівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Сагайда Тетяна Вікторівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
        {
            "name": 'Сіра Ірина Григорівна',
            "applied": 0,
            "reviewed": 0,
            "reviewing": 0,
            "average_time": 0,
            "registrations": 0,
            "changes": 0,
            "budget_preparing": 0,
            "budget_changes": 0,
        },
    ])


def regions(request):
    return render(request, 'home/regions.html')


def finances(request):
    return render(request, 'home/finances.html')


def obj_types(request):
    return render(request, 'home/obj_types.html')


@api_view(['GET'])
def obj_types_statistics(request):
    statistics = list()

    claims_ap = ClOap.objects.values(
        'oap_name'
    ).filter(
        claims__statisticsvalues__cert_id__in=(1, 2),
        claims__objtype_id__in=(1, 2),
        claims__statisticsvalues__timekey__fulldatealternatekey__gte=request.GET['date_from'],
        claims__statisticsvalues__timekey__fulldatealternatekey__lte=request.GET['date_to']
    ).annotate(
        Sum('claims__statisticsvalues__value')
    ).order_by(
        'oap_name'
    )
    claims_ap = {item['oap_name']: item['claims__statisticsvalues__value__sum'] for item in claims_ap}

    claims_dg = ClOap.objects.values(
        'oap_name'
    ).filter(
        claims__statisticsvalues__cert_id__in=(3, 4),
        claims__objtype_id__in=(3, 4),
        claims__statisticsvalues__timekey__fulldatealternatekey__gte=request.GET['date_from'],
        claims__statisticsvalues__timekey__fulldatealternatekey__lte=request.GET['date_to']
    ).annotate(
        Sum('claims__statisticsvalues__value')
    ).order_by(
        'oap_name'
    )
    claims_dg = {item['oap_name']: item['claims__statisticsvalues__value__sum'] for item in claims_dg}

    registrations_ap = ClOap.objects.values(
        'oap_name'
    ).filter(
        claims__statisticsvalues__cert_id=7,
        claims__objtype_id__in=(1, 2),
        claims__statisticsvalues__timekey__fulldatealternatekey__gte=request.GET['date_from'],
        claims__statisticsvalues__timekey__fulldatealternatekey__lte=request.GET['date_to']
    ).annotate(
        Sum('claims__statisticsvalues__value')
    ).order_by(
        'oap_name'
    )
    registrations_ap = {item['oap_name']: item['claims__statisticsvalues__value__sum'] for item in registrations_ap}

    registrations_dg = ClOap.objects.values(
        'oap_name'
    ).filter(
        claims__statisticsvalues__cert_id=7,
        claims__objtype_id__in=(3, 4),
        claims__statisticsvalues__timekey__fulldatealternatekey__gte=request.GET['date_from'],
        claims__statisticsvalues__timekey__fulldatealternatekey__lte=request.GET['date_to']
    ).annotate(
        Sum('claims__statisticsvalues__value')
    ).order_by(
        'oap_name'
    )
    registrations_dg = {item['oap_name']: item['claims__statisticsvalues__value__sum'] for item in registrations_dg}

    for oap in ClOap.objects.filter(active=True).order_by('oap_name'):
        try:
            claim_ap_count = claims_ap[oap.oap_name]
        except KeyError:
            claim_ap_count = 0

        try:
            claims_dg_count = claims_dg[oap.oap_name]
        except KeyError:
            claims_dg_count = 0

        try:
            registrations_ap_count = registrations_ap[oap.oap_name]
        except KeyError:
            registrations_ap_count = 0

        try:
            registrations_dg_count = registrations_dg[oap.oap_name]
        except KeyError:
            registrations_dg_count = 0

        statistics.append({
            'obj_type': oap.oap_name,
            'claims': {
                'ap': claim_ap_count,
                'dg': claims_dg_count,
            },
            'registrations': {
                'ap': registrations_ap_count,
                'dg': registrations_dg_count,
            }
        })

    return Response(statistics)


class ObjTypesClaimsListView(generics.ListAPIView):

    serializer_class = ClaimsSerializer

    def get_queryset(self):
        queryset = LsClaimList.objects.prefetch_related(
            Prefetch(
                'persons',
                queryset=ClPersonList.objects.filter(linkclaimpersons__id_type_person__in=(1, 5))
            ),
            Prefetch(
                'objtype'
            ),
            Prefetch(
                'oap'
            ),
            Prefetch(
                'events',
                queryset=LsEventList.objects.prefetch_related(
                    Prefetch('user'),
                    Prefetch('event_type'),
                )
            ),
        ).filter(
            objtype_id__in=(1, 2)
        ).order_by('appnumber')

        # Дата від
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        app_type = self.request.query_params.get('appType', None)
        oap_name = self.request.query_params.get('objType', None)
        cert_id = None
        obj_type_id = None
        if app_type == 'claims_ap':
            cert_id = (1, 2)
            obj_type_id = (1, 2)
        if app_type == 'claims_dg':
            cert_id = (3, 4)
            obj_type_id = (1, 2)
        if app_type == 'registrations_ap':
            cert_id = (7,)
            obj_type_id = (3, 4)
        if app_type == 'registrations_dg':
            cert_id = (7,)
            obj_type_id = (3, 4)

        if date_from and date_to:
            try:
                if cert_id and obj_type_id:
                    queryset = queryset.filter(
                        oap__oap_name=oap_name,
                        statisticsvalues__timekey__fulldatealternatekey__gte=date_from,
                        statisticsvalues__timekey__fulldatealternatekey__lte=date_to,
                        statisticsvalues__cert_id__in=cert_id,
                        objtype_id__in=obj_type_id,
                    )
                else:
                    queryset = queryset.filter(
                        oap__oap_name=oap_name,
                        statisticsvalues__timekey__fulldatealternatekey__gte=date_from,
                        statisticsvalues__timekey__fulldatealternatekey__lte=date_to
                    )
            except:
                raise exceptions.ParseError("Невірне значення параметрів")

        return queryset


def admin_services(request):
    return render(request, 'home/admin_services.html')


def duplicates(request):
    return render(request, 'home/duplicates.html')
