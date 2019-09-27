<template>
    <div>
        <b-table id="apps-specialists-workload"
                 :fields="fields"
                 :items="items"
                 striped
                 bordered
                 responsive="sm"
                 empty-text="Заявки відсутні"
                 show-empty
                 :current-page="currentPage"
                 :per-page="perPage"
                 ref="table"
        >
            <template v-slot:table-busy>
                <div class="text-center my-2">
                    <b-spinner class="align-middle"></b-spinner>
                    <strong>Завантаження даних...</strong>
                </div>
            </template>

            <template v-slot:thead-top="data">
                <b-tr>
                    <b-th rowspan="2">№ заявки</b-th>
                    <b-th></b-th>
                    <b-th colspan="8">Статуси розгляду</b-th>
                    <b-th rowspan="2">Середній час розгляду</b-th>
                    <b-th colspan="5">Зараховано</b-th>
                </b-tr>
            </template>

            <template v-slot:cell(app_number)="row">
                <a :href="'//spec.authors.ukrpatent.org/claims/claim?id=' + row.item.idclaim"
                   target="_blank">{{ row.item.app_number || '-' }}</a>
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

    export default {
        props: ['appType', 'specialistName', 'dateFrom', 'dateTo'],
        data() {
            return {
                fields: [
                    {key: 'app_number', label: '№ заявки'},
                    {key: 'app_type', label: 'Вид заявки'},
                    {key: 'registered', label: 'Зареєстровано'},
                    {key: 'without_registration', label: 'Без розгляду'},
                    {key: 'refused', label: 'Відмова'},
                    {key: 'returned', label: 'Повернено'},
                    {key: 'canceled', label: 'Відхилено'},
                    {key: 'disadvantages_letters', label: 'Листи-недоліки'},
                    {key: 'reviewing', label: 'На розгляді'},
                    {key: 'reviewed_total', label: 'ВСЬОГО:'},
                    {key: 'average_time', label: 'Середній час розгляду'},
                    {key: 'budget_preparing', label: 'За підготовку до реєстрації'},
                    {key: 'budget_issue', label: 'За видачу свідоцтва'},
                    {key: 'budget_overpayment', label: 'Переплата'},
                    {key: 'budget_duplicate', label: 'За видачу дубліката'},
                    {key: 'budget_changes', label: 'За внесення змін'},
                    {key: 'idclaim', label: 'idclaim'},
                ],
                items: [
                    {
                        app_number: 1,
                        app_type: 2,
                        registered: 3,
                        without_registration: 4,
                        refused: 5,
                        returned: 6,
                        canceled: 7,
                        disadvantages_letters: 8,
                        reviewing: 9,
                        reviewed_total: 10,
                        average_time: 11,
                        budget_preparing: 11,
                        budget_issue: 12,
                        budget_overpayment: 13,
                        budget_duplicate: 14,
                        budget_changes: 15,
                        idclaim: 100,
                    }
                ],
                totalRows: 1,
                currentPage: 1,
                perPage: 10,
            }
        },
        watch: {
            appType() {
                this.refreshTable();
            },
            specialistName() {
                this.refreshTable();
            }
        },
        mounted() {
            window.scrollTo(0,document.body.scrollHeight);
        },
        methods: {
            refreshTable() {
                this.totalRows = 1;
                this.currentPage = 1;
                this.$refs.table.refresh();
                window.scrollTo(0,document.body.scrollHeight);
            },

            // Получение списка заявок с сервера
            getItems(ctx) {
                let promise = axios.get('/api/dg_specialist_workload_claims/', {
                    params: {
                        appType: this.appType,
                        specialistName: this.specialistName,
                        date_from: this.dateFrom.toISOString().split('T')[0],
                        date_to: this.dateTo.toISOString().split('T')[0],
                        page: ctx.currentPage,
                    }
                });
                return promise.then((response) => {
                    this.totalRows = response.data.count;
                    return(response.data.results || []);
                });
            }
        }
    }
</script>

<style>
    table#apps-specialists-workload th[aria-colindex="1"] {
        display: none;
    }

    table#apps-specialists-workload th[aria-colindex="11"] {
        display: none;
    }

    table#apps-specialists-workload th[aria-colindex="17"], table#apps-specialists-workload td[aria-colindex="17"] {
        display: none;
    }

    table#apps-specialists-workload th {
        text-align: center;
    }
</style>