<template>
    <div>
        <b-table :fields="fields"
                 :items="getItems"
                 striped
                 bordered
                 responsive="sm"
                 empty-text="Заявники відсутні"
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

            <template v-slot:cell(full_name)="row">
                <a href="#" @click.prevent="row.toggleDetails">{{ row.item.full_name || '-' }}</a>
            </template>

            <template v-slot:row-details="row">
                <p>Перелік заявок:</p>
                <ul>
                    <li v-for="item in row.item.claims">
                        <a :href="'//spec.authors.ukrpatent.org/claims/claim?id=' + item.idclaim"
                           target="_blank">{{ item.claim_number }}</a>
                    </li>
                </ul>
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
        props: ['region', 'obj_type', 'legal_type', 'dateFrom', 'dateTo'],
        data() {
            return {
                fields: [
                    {key: 'full_name', label: 'ФІО/назва заявника'},
                    {key: 'total_claims', label: 'Кількість поданих заяв'},
                    {key: 'budget_enrolled', label: 'Зараховані кошти'},
                    {key: 'budget_not_enrolled', label: 'Незараховані кошти'},
                ],
                items: [
                    {
                        name: 'Заявник1',
                        claims_count: 2,
                        budget_enrolled: 3,
                        budget_not_enrolled: 4,
                        claims: [
                            {
                                idclaim: 1,
                                app_number: 1
                            },
                            {
                                idclaim: 2,
                                app_number: 2
                            },
                            {
                                idclaim: 3,
                                app_number: 3
                            },
                        ]
                    },
                    {
                        name: 'Заявник2',
                        claims_count: 2,
                        budget_enrolled: 3,
                        budget_not_enrolled: 4,
                        claims: [
                            {
                                idclaim: 1,
                                app_number: 1
                            },
                            {
                                idclaim: 2,
                                app_number: 2
                            },
                            {
                                idclaim: 3,
                                app_number: 3
                            },
                        ]
                    },
                ],
                totalRows: 1,
                currentPage: 1,
                perPage: 10,
            }
        },
        watch: {
            region() {
                this.refreshTable();
            },
            obj_type() {
                this.refreshTable();
            },
            legal_type() {
                this.refreshTable();
            },
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
                let promise = axios.get('/api/statistics/regions_persons/', {
                    params: {
                        date_from: this.dateFrom.toISOString().split('T')[0],
                        date_to: this.dateTo.toISOString().split('T')[0],
                        region: this.region,
                        obj_type: this.obj_type,
                        legal_type: this.legal_type,
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
</style>