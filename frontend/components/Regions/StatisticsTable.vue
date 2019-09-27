<template>
    <div>
        <div class="d-flex justify-content-center mt-5" v-if="isBusy">
            <strong>Завантаження даних...</strong>
            <b-spinner class="ml-2"></b-spinner>
        </div>

        <b-table-simple small
                        caption-top
                        responsive
                        striped
                        bordered
                        id="statistics-table"
                        v-else>
            <caption>Статистичні дані щодо за територіями за період від {{ dateFrom | moment("DD.MM.YYYY") }} до {{ dateTo | moment("DD.MM.YYYY") }}</caption>
            <b-thead class="text-center">
                <b-tr>
                    <b-th rowspan="2">Регіон</b-th>
                    <b-th colspan="5">Кількість заявників</b-th>
                    <b-th colspan="5">Кількість поданих заявок</b-th>
                    <b-th colspan="2" rowspan="2">Кількість реєстрацій</b-th>
                    <b-th colspan="3" rowspan="2">Надійшло коштів</b-th>
                </b-tr>
                <b-tr>
                    <b-th colspan="2">АП</b-th>
                    <b-th colspan="2">ДГ</b-th>
                    <b-th rowspan="2">Σ</b-th>
                    <b-th colspan="2">АП</b-th>
                    <b-th colspan="2">ДГ</b-th>
                    <b-th rowspan="2">Σ</b-th>
                </b-tr>
                <b-tr>
                    <b-th></b-th>
                    <b-th>ф</b-th>
                    <b-th>ю</b-th>
                    <b-th>ф</b-th>
                    <b-th>ю</b-th>
                    <b-th>ф</b-th>
                    <b-th>ю</b-th>
                    <b-th>ф</b-th>
                    <b-th>ю</b-th>
                    <b-th>АП</b-th>
                    <b-th>ДГ</b-th>
                    <b-th>АП</b-th>
                    <b-th>ДГ</b-th>
                    <b-th>Σ</b-th>
                </b-tr>
            </b-thead>
            <b-tbody class="text-center">
                <b-tr v-for="item in statistics" :key="item.region">
                    <b-td>{{ item.region }}</b-td>
                    <b-td :class="{ 'bg-info text-white': region === item.region && obj_type === 'ap' && legal_type === 'phys'}">
                        <a href="#" @click.prevent="$emit('show-apps', item.region, 'ap', 'phys')">{{ item.applicants.ap.phys }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': region === item.region && obj_type === 'ap' && legal_type === 'jur'}">
                        <a href="#" @click.prevent="$emit('show-apps', item.region, 'ap', 'jur')">{{ item.applicants.ap.jur }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': region === item.region && obj_type === 'dg' && legal_type === 'phys'}">
                        <a href="#" @click.prevent="$emit('show-apps', item.region, 'dg', 'phys')">{{ item.applicants.dg.phys }}</a>
                    </b-td>
                    <b-td :class="{ 'bg-info text-white': region === item.region && obj_type === 'dg' && legal_type === 'jur'}">
                        <a href="#" @click.prevent="$emit('show-apps', item.region, 'dg', 'jur')">{{ item.applicants.dg.jur }}</a>
                    </b-td>
                    <b-td>{{ getCountApplicants(item) }}</b-td>
                    <b-td>{{ item.claims.ap.phys }}</b-td>
                    <b-td>{{ item.claims.ap.jur }}</b-td>
                    <b-td>{{ item.claims.dg.phys }}</b-td>
                    <b-td>{{ item.claims.dg.jur }}</b-td>
                    <b-td>{{ getCountClaims(item) }}</b-td>
                    <b-td>{{ item.registrations.ap }}</b-td>
                    <b-td>{{ item.registrations.dg }}</b-td>
                    <b-td>{{ item.budget.ap }}</b-td>
                    <b-td>{{ item.budget.dg }}</b-td>
                    <b-td>{{ getCountBudget(item) }}</b-td>
                </b-tr>
                <b-tr>
                    <b-td>∑</b-td>
                    <b-td>{{ getApplicantsApPhysTotal }}</b-td>
                    <b-td>{{ getApplicantsApJurTotal }}</b-td>
                    <b-td>{{ getApplicantsDgPhysTotal }}</b-td>
                    <b-td>{{ getApplicantsDgJurTotal }}</b-td>
                    <b-td>{{ getApplicantsTotal }}</b-td>
                    <b-td>{{ getClaimsApPhysTotal }}</b-td>
                    <b-td>{{ getClaimsApJurTotal }}</b-td>
                    <b-td>{{ getClaimsDgPhysTotal }}</b-td>
                    <b-td>{{ getClaimsDgJurTotal }}</b-td>
                    <b-td>{{ getClaimsTotal }}</b-td>
                    <b-td>{{ getRegistrationsApTotal }}</b-td>
                    <b-td>{{ getRegistrationsDgTotal }}</b-td>
                    <b-td>{{ getBudgetApTotal }}</b-td>
                    <b-td>{{ getBudgetDgTotal }}</b-td>
                    <b-td>{{ getBudgetTotal }}</b-td>
                </b-tr>
            </b-tbody>
            <b-tfoot>
                <b-tr>
                    <b-td colspan="16" variant="secondary" class="text-right">
                        <b-button size="sm"
                                  @click="excelExport('statistics-table', 'Статистика', 'statistics.xls')"
                        >Експорт у Excel</b-button>
                    </b-td>
                </b-tr>
            </b-tfoot>
        </b-table-simple>
    </div>
</template>

<script>
    import axios from 'axios';
    import ExcelMixin from './../../mixins/ExcelMixin';

    export default {
        props: ['dateFrom', 'dateTo', 'region', 'obj_type', 'legal_type'],
        mixins: [ExcelMixin],

        data() {
            return {
                isBusy: false,
                statistics: [
                    {
                        region: 'Регіон1',
                        applicants: {
                            ap: {
                                phys: 5,
                                jur: 0,
                            },
                            dg: {
                                phys: 0,
                                jur: 0,
                            }
                        },
                        claims: {
                            ap: {
                                phys: 0,
                                jur: 0,
                            },
                            dg: {
                                phys: 0,
                                jur: 0,
                            }
                        },
                        registrations: {
                            ap: 0,
                            dg: 0
                        },
                        budget: {
                            ap: 0,
                            dg: 0
                        }
                    },
                    {
                        region: 'Регіон2',
                        applicants: {
                            ap: {
                                phys: 0,
                                jur: 0,
                            },
                            dg: {
                                phys: 0,
                                jur: 0,
                            }
                        },
                        claims: {
                            ap: {
                                phys: 0,
                                jur: 0,
                            },
                            dg: {
                                phys: 0,
                                jur: 0,
                            }
                        },
                        registrations: {
                            ap: 0,
                            dg: 0
                        },
                        budget: {
                            ap: 0,
                            dg: 0
                        }
                    },
                    {
                        region: 'Регіон3',
                        applicants: {
                            ap: {
                                phys: 0,
                                jur: 0,
                            },
                            dg: {
                                phys: 0,
                                jur: 0,
                            }
                        },
                        claims: {
                            ap: {
                                phys: 0,
                                jur: 0,
                            },
                            dg: {
                                phys: 0,
                                jur: 0,
                            }
                        },
                        registrations: {
                            ap: 0,
                            dg: 0
                        },
                        budget: {
                            ap: 0,
                            dg: 0
                        }
                    },
                ]
            }
        },
        computed: {
            getApplicantsApPhysTotal() {
                return this.statistics.map(function (item) {
                    return item.applicants.ap.phys;
                }).reduce(function(sum, current) {
                    return sum + current;
                }, 0);
            },
            getApplicantsApJurTotal() {
                return this.statistics.map(function (item) {
                    return item.applicants.ap.jur;
                }).reduce(function(sum, current) {
                    return sum + current;
                }, 0);
            },
            getApplicantsDgPhysTotal() {
                return this.statistics.map(function (item) {
                    return item.applicants.dg.phys;
                }).reduce(function(sum, current) {
                    return sum + current;
                }, 0);
            },
            getApplicantsDgJurTotal() {
                return this.statistics.map(function (item) {
                    return item.applicants.dg.jur;
                }).reduce(function(sum, current) {
                    return sum + current;
                }, 0);
            },
            getApplicantsTotal() {
                return this.getApplicantsApPhysTotal
                    + this.getApplicantsApJurTotal
                    + this.getApplicantsDgPhysTotal
                    + this.getApplicantsDgJurTotal;
            },
            getClaimsApPhysTotal() {
                return this.statistics.map(function (item) {
                    return item.claims.ap.phys;
                }).reduce(function(sum, current) {
                    return sum + current;
                }, 0);
            },
            getClaimsApJurTotal() {
                return this.statistics.map(function (item) {
                    return item.claims.ap.jur;
                }).reduce(function(sum, current) {
                    return sum + current;
                }, 0);
            },
            getClaimsDgPhysTotal() {
                return this.statistics.map(function (item) {
                    return item.claims.dg.phys;
                }).reduce(function(sum, current) {
                    return sum + current;
                }, 0);
            },
            getClaimsDgJurTotal() {
                return this.statistics.map(function (item) {
                    return item.claims.dg.jur;
                }).reduce(function(sum, current) {
                    return sum + current;
                }, 0);
            },
            getClaimsTotal() {
                return this.getClaimsApPhysTotal
                    + this.getClaimsApJurTotal
                    + this.getClaimsDgPhysTotal
                    + this.getClaimsDgJurTotal;
            },
            getRegistrationsApTotal() {
                return this.statistics.map(function (item) {
                    return item.registrations.ap;
                }).reduce(function(sum, current) {
                    return sum + current;
                }, 0);
            },
            getRegistrationsDgTotal() {
                return this.statistics.map(function (item) {
                    return item.registrations.dg;
                }).reduce(function(sum, current) {
                    return sum + current;
                }, 0);
            },
            getBudgetApTotal() {
                return this.statistics.map(function (item) {
                    return item.budget.ap;
                }).reduce(function(sum, current) {
                    return sum + current;
                }, 0);
            },
            getBudgetDgTotal() {
                return this.statistics.map(function (item) {
                    return item.budget.dg;
                }).reduce(function(sum, current) {
                    return sum + current;
                }, 0);
            },
            getBudgetTotal() {
                return this.getBudgetApTotal + this.getBudgetDgTotal;
            },
        },

        created() {
            // Загрузка статистических данных
            //this.getStatisticsData();
        },

        methods: {
            getStatisticsData: function () {
                this.isBusy = true;
                axios.get('/api/statistics/dg_specialist_workload_statistics/', {
                    params: {
                        date_from: this.dateFrom.toISOString().split('T')[0],
                        date_to: this.dateTo.toISOString().split('T')[0],
                    }
                }).then(response => {
                    this.statistics = response.data;
                    this.isBusy = false;
                })
            },

            getCountApplicants(item) {
                return item.applicants.ap.phys
                    + item.applicants.ap.jur
                    + item.applicants.dg.phys
                    + item.applicants.dg.jur;
            },

            getCountClaims(item) {
                return item.claims.ap.phys
                    + item.claims.ap.jur
                    + item.claims.dg.phys
                    + item.claims.dg.jur;
            },

            getCountBudget(item) {
                return item.budget.ap + item.budget.dg;
            }
        },

        watch: {
            dateFrom() {
                if (!this.isBusy) {
                    this.getStatisticsData();
                }
            },
            dateTo() {
                if (!this.isBusy) {
                    this.getStatisticsData();
                }
            }
        }
    }
</script>