<template>
    <div>
        <div class="d-flex justify-content-center mt-5" v-if="isBusy">
            <strong>Завантаження даних...</strong>
            <b-spinner class="ml-2"></b-spinner>
        </div>

        <b-table-simple small caption-top responsive striped bordered v-else>
            <caption>Статистичні дані щодо надходження зборів за період від {{ dateFrom | moment("DD.MM.YYYY") }} до {{ dateTo | moment("DD.MM.YYYY") }}</caption>
            <b-thead class="text-center">
                <b-tr>
                    <b-th rowspan="2">Вид заявки</b-th>
                    <b-th rowspan="2">Вид особи (ф/ю)</b-th>
                    <b-th colspan="2">Кошти, що сплачені заявником</b-th>
                    <b-th colspan="2">Зараховані платежі</b-th>
                    <b-th colspan="2">Використані кошти</b-th>
                    <b-th rowspan="2">Переплата (кошти, що залишились після використання)</b-th>
                    <b-th rowspan="2">Не використані (кошти, що залишились по закінченню 3-х місяців після оплати)</b-th>
                </b-tr>
                <b-tr>
                    <b-th>За підготовку до реєстрації</b-th>
                    <b-th>За видачу свідоцтва</b-th>
                    <b-th>За підготовку до реєстрації</b-th>
                    <b-th>За видачу свідоцтва</b-th>
                    <b-th>За підготовку до реєстрації</b-th>
                    <b-th>За видачу свідоцтва</b-th>
                </b-tr>
            </b-thead>
            <b-tbody class="text-center">
                <b-tr>
                    <b-td rowspan="3">АП</b-td>
                    <b-td>ф</b-td>
                    <b-td>{{ statistics.paid.ap.preparing.phys }}</b-td>
                    <b-td>{{ statistics.paid.ap.certificate.phys }}</b-td>
                    <b-td>{{ statistics.payments.ap.preparing.phys }}</b-td>
                    <b-td>{{ statistics.payments.ap.certificate.phys }}</b-td>
                    <b-td>{{ statistics.used.ap.preparing.phys }}</b-td>
                    <b-td>{{ statistics.used.ap.certificate.phys }}</b-td>
                    <b-td>{{ statistics.overpayment.ap.phys }}</b-td>
                    <b-td>{{ statistics.not_used.ap.phys }}</b-td>
                </b-tr>
                <b-tr>
                    <b-td>ю</b-td>
                    <b-td>{{ statistics.paid.ap.preparing.jur }}</b-td>
                    <b-td>{{ statistics.paid.ap.certificate.jur }}</b-td>
                    <b-td>{{ statistics.payments.ap.preparing.jur }}</b-td>
                    <b-td>{{ statistics.payments.ap.certificate.jur }}</b-td>
                    <b-td>{{ statistics.used.ap.preparing.jur }}</b-td>
                    <b-td>{{ statistics.used.ap.certificate.jur }}</b-td>
                    <b-td>{{ statistics.overpayment.ap.jur }}</b-td>
                    <b-td>{{ statistics.not_used.ap.jur }}</b-td>
                </b-tr>
                <b-tr>
                    <b-td>∑</b-td>
                    <b-td v-html="statistics.paid.ap.preparing.phys + statistics.paid.ap.preparing.jur"></b-td>
                    <b-td v-html="statistics.paid.ap.certificate.phys + statistics.paid.ap.certificate.jur"></b-td>
                    <b-td v-html="statistics.payments.ap.preparing.phys + statistics.payments.ap.preparing.jur"></b-td>
                    <b-td v-html="statistics.payments.ap.certificate.phys + statistics.payments.ap.certificate.jur"></b-td>
                    <b-td v-html="statistics.used.ap.preparing.phys + statistics.used.ap.preparing.jur"></b-td>
                    <b-td v-html="statistics.used.ap.certificate.phys + statistics.used.ap.certificate.jur"></b-td>
                    <b-td v-html="statistics.overpayment.ap.phys + statistics.overpayment.ap.jur"></b-td>
                    <b-td v-html="statistics.not_used.ap.phys + statistics.not_used.ap.jur"></b-td>
                </b-tr>
                <b-tr>
                    <b-td rowspan="3">АП</b-td>
                    <b-td>ф</b-td>
                    <b-td>{{ statistics.paid.dg.preparing.phys }}</b-td>
                    <b-td>{{ statistics.paid.dg.certificate.phys }}</b-td>
                    <b-td>{{ statistics.payments.dg.preparing.phys }}</b-td>
                    <b-td>{{ statistics.payments.dg.certificate.phys }}</b-td>
                    <b-td>{{ statistics.used.dg.preparing.phys }}</b-td>
                    <b-td>{{ statistics.used.dg.certificate.phys }}</b-td>
                    <b-td>{{ statistics.overpayment.dg.phys }}</b-td>
                    <b-td>{{ statistics.not_used.dg.phys }}</b-td>
                </b-tr>
                <b-tr>
                    <b-td>ю</b-td>
                    <b-td>{{ statistics.paid.dg.preparing.jur }}</b-td>
                    <b-td>{{ statistics.paid.dg.certificate.jur }}</b-td>
                    <b-td>{{ statistics.payments.dg.preparing.jur }}</b-td>
                    <b-td>{{ statistics.payments.dg.certificate.jur }}</b-td>
                    <b-td>{{ statistics.used.dg.preparing.jur }}</b-td>
                    <b-td>{{ statistics.used.dg.certificate.jur }}</b-td>
                    <b-td>{{ statistics.overpayment.dg.jur }}</b-td>
                    <b-td>{{ statistics.not_used.dg.jur }}</b-td>
                </b-tr>
                <b-tr>
                    <b-td>∑</b-td>
                    <b-td v-html="statistics.paid.dg.preparing.phys + statistics.paid.dg.preparing.jur"></b-td>
                    <b-td v-html="statistics.paid.dg.certificate.phys + statistics.paid.dg.certificate.jur"></b-td>
                    <b-td v-html="statistics.payments.dg.preparing.phys + statistics.payments.dg.preparing.jur"></b-td>
                    <b-td v-html="statistics.payments.dg.certificate.phys + statistics.payments.dg.certificate.jur"></b-td>
                    <b-td v-html="statistics.used.dg.preparing.phys + statistics.used.dg.preparing.jur"></b-td>
                    <b-td v-html="statistics.used.dg.certificate.phys + statistics.used.dg.certificate.jur"></b-td>
                    <b-td v-html="statistics.overpayment.dg.phys + statistics.overpayment.dg.jur"></b-td>
                    <b-td v-html="statistics.not_used.dg.phys + statistics.not_used.dg.jur"></b-td>
                </b-tr>
                <b-tr>
                    <b-td>Невизначені платежі</b-td>
                    <b-td>X</b-td>
                    <b-td>X</b-td>
                    <b-td>X</b-td>
                    <b-td>{{ statistics.payments.undefined.preparing }}</b-td>
                    <b-td>{{ statistics.payments.undefined.certificate }}</b-td>
                    <b-td>X</b-td>
                    <b-td>X</b-td>
                    <b-td>X</b-td>
                    <b-td>{{ statistics.not_used.undefined }}</b-td>
                </b-tr>
                <b-tr>
                    <b-td>∑</b-td>
                    <b-td>X</b-td>
                    <b-td v-html="statistics.paid.ap.preparing.phys + statistics.paid.ap.preparing.jur + statistics.paid.dg.preparing.phys + statistics.paid.dg.preparing.jur"></b-td>
                    <b-td v-html="statistics.paid.ap.certificate.phys + statistics.paid.ap.certificate.jur + statistics.paid.dg.certificate.phys + statistics.paid.dg.certificate.jur"></b-td>
                    <b-td v-html="statistics.payments.ap.preparing.phys + statistics.payments.ap.preparing.jur + statistics.payments.dg.preparing.phys + statistics.payments.dg.preparing.jur + statistics.payments.undefined.preparing"></b-td>
                    <b-td v-html="statistics.payments.ap.certificate.phys + statistics.payments.ap.certificate.jur + statistics.payments.dg.certificate.phys + statistics.payments.dg.certificate.jur + statistics.payments.undefined.certificate"></b-td>
                    <b-td v-html="statistics.used.ap.preparing.phys + statistics.used.ap.preparing.jur + statistics.used.dg.preparing.phys + statistics.used.dg.preparing.jur"></b-td>
                    <b-td v-html="statistics.used.ap.certificate.phys + statistics.used.ap.certificate.jur + statistics.used.dg.certificate.phys + statistics.used.dg.certificate.jur"></b-td>
                    <b-td v-html="statistics.overpayment.ap.phys + statistics.overpayment.ap.jur + statistics.overpayment.dg.phys + statistics.overpayment.dg.jur"></b-td>
                    <b-td v-html="statistics.not_used.ap.phys + statistics.not_used.ap.jur + statistics.not_used.dg.phys + statistics.not_used.dg.jur + statistics.not_used.undefined"></b-td>
                </b-tr>
            </b-tbody>
            <b-tfoot>
                <b-tr>
                    <b-td colspan="10" variant="secondary" class="text-right">
                        <b-button size="sm">Експорт у Excel</b-button>
                    </b-td>
                </b-tr>
            </b-tfoot>
        </b-table-simple>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                isBusy: false,
                statistics: {
                    paid: {
                        ap: {
                            preparing: {
                                phys: 0,
                                jur: 0,
                            },
                            certificate: {
                                phys: 0,
                                jur: 0,
                            }
                        },
                        dg: {
                            preparing: {
                                phys: 0,
                                jur: 0,
                            },
                            certificate: {
                                phys: 0,
                                jur: 0,
                            }
                        }
                    },
                    payments: {
                        ap: {
                            preparing: {
                                phys: 0,
                                jur: 0,
                            },
                            certificate: {
                                phys: 0,
                                jur: 0,
                            }
                        },
                        dg: {
                            preparing: {
                                phys: 0,
                                jur: 0,
                            },
                            certificate: {
                                phys: 0,
                                jur: 0,
                            }
                        },
                        undefined: {
                            preparing: 0,
                            certificate: 0
                        }
                    },
                    used: {
                        ap: {
                            preparing: {
                                phys: 0,
                                jur: 0,
                            },
                            certificate: {
                                phys: 0,
                                jur: 0,
                            }
                        },
                        dg: {
                            preparing: {
                                phys: 0,
                                jur: 0,
                            },
                            certificate: {
                                phys: 0,
                                jur: 0,
                            }
                        }
                    },
                    overpayment: {
                        ap: {
                            phys: 0,
                            jur: 0,
                        },
                        dg: {
                            phys: 0,
                            jur: 0,
                        },
                    },
                    not_used: {
                        ap: {
                            phys: 0,
                            jur: 0,
                        },
                        dg: {
                            phys: 0,
                            jur: 0,
                        },
                        undefined: 0,
                    }
                },
                computed: {

                }
            }
        }
    }
</script>

<style scoped>

</style>