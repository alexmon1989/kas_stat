<template>
    <div>
        <b-table :items="items"
                 :fields="fields"
                 striped
                 small
                 bordered
                 responsive="sm"
                 empty-text="Заявки відсутні"
                 show-empty
                 :current-page="currentPage"
                 :per-page="perPage"
                 caption-top
                 ref="table"
                 id="statistics-table"
        >
            <template v-slot:table-busy>
                <div class="text-center my-2">
                    <b-spinner class="align-middle"></b-spinner>
                    <strong>Завантаження даних...</strong>
                </div>
            </template>

            <template v-slot:table-caption>Видача дублікатів / внесення змін за період від {{ dateFrom | moment("DD.MM.YYYY") }} до {{ dateTo | moment("DD.MM.YYYY") }}</template>

            <template v-slot:custom-foot>
                <b-tr>
                    <b-td colspan="9" variant="secondary" class="text-right">
                        <b-button size="sm"
                                  @click="excelExport('statistics-table', 'Статистика', 'statistics.xls')"
                        >Експорт у Excel</b-button>
                    </b-td>
                </b-tr>
            </template>
        </b-table>

        <b-row class="justify-content-center" v-if="totalRows > perPage">
            <b-col sm="7" md="6" class="my-1">
                <b-pagination v-model="currentPage"
                              :total-rows="totalRows"
                              :per-page="perPage"
                              align="fill"
                ></b-pagination>
            </b-col>
        </b-row>
    </div>
</template>

<script>
    import axios from 'axios';
    import mixin from './../../mixins.js';

    export default {
        props: ['dateFrom', 'dateTo'],
        mixins: [mixin],
        data() {
            return {
                fields: [
                    {key: 'petitions_count', label: 'Кількість поданих клопотань'},
                    {key: 'petition_type', label: 'Вид клопотання (видача дубліката / внесення змін)'},
                    {key: 'reviewed', label: 'Розглянуті'},
                    {key: 'reviewing', label: 'На розгляді'},
                    {key: 'budget', label: 'Кошти сплачені заявником'},
                    {key: 'accrued_payments', label: 'Зараховані платежі'},
                    {key: 'used_money', label: 'Використані кошти'},
                    {key: 'overpayment', label: 'Переплата'},
                    {key: 'undefined_payments', label: 'Невизначені платежі'},
                ],
                items: [
                    {
                        petitions_count: 0,
                        petition_type: 'Видача дублікатів',
                        reviewed: 0,
                        reviewing: 0,
                        budget: 0,
                        accrued_payments: 0,
                        used_money: 0,
                        overpayment: 0,
                        undefined_payments: 0,
                    },
                    {
                        petitions_count: 0,
                        petition_type: 'Внесення змін',
                        reviewed: 0,
                        reviewing: 0,
                        budget: 0,
                        accrued_payments: 0,
                        used_money: 0,
                        overpayment: 0,
                        undefined_payments: 0,
                    },
                ],
                totalRows: 1,
                currentPage: 1,
                perPage: 10,
            }
        },
        methods: {
            // Получение списка заявок с сервера
            getItems(ctx) {
                let promise = axios.get('/api/dg_claims/', {
                    params: {
                        appType: this.appType,
                        date_from: this.dateFrom.toISOString().split('T')[0],
                        date_to: this.dateTo.toISOString().split('T')[0],
                        page: ctx.currentPage,
                    }
                });
                return promise.then((response) => {
                    this.totalRows = response.data.count;
                    return(response.data.results || []);
                });
            },
        }
    }
</script>