from django.urls import path
from .views import (ap, ap_statistics, ApClaimsListView, dg, dg_statistics, DgClaimsListView, ap_specialist_workload,
                    ap_specialist_workload_statistics, ap_specialist_workload_claims, dg_specialist_workload,
                    dg_specialist_workload_statistics, regions, regions_statistics, finances, obj_types, admin_services,
                    duplicates, obj_types_statistics, ObjTypesClaimsListView, RegionsPersonsListView)


urlpatterns = [
    path('ap/', ap),
    path('api/statistics/ap/', ap_statistics),
    path('api/ap_claims/', ApClaimsListView.as_view()),

    path('dg/', dg),
    path('api/statistics/dg/', dg_statistics),
    path('api/dg_claims/', DgClaimsListView.as_view()),

    path('ap_specialist_workload/', ap_specialist_workload),
    path('api/statistics/ap_specialist_workload_statistics/', ap_specialist_workload_statistics),
    path('api/ap_specialist_workload_claims/', ap_specialist_workload_claims),

    path('dg_specialist_workload/', dg_specialist_workload),
    path('api/statistics/dg_specialist_workload_statistics/', dg_specialist_workload_statistics),

    path('regions/', regions),
    path('api/statistics/regions/', regions_statistics),
    path('api/statistics/regions_persons/', RegionsPersonsListView.as_view()),

    path('finances/', finances),

    path('obj_types/', obj_types),
    path('api/statistics/obj_types/', obj_types_statistics),
    path('api/obj_types_claims/', ObjTypesClaimsListView.as_view()),

    path('admin_services/', admin_services),
    path('duplicates/', duplicates),
]
