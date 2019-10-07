<template>
    <div>
        <b-table :items="items"
                 :fields="fields"
                 :busy="isBusy"
                 striped
                 responsive="sm"
                 empty-text="Заявники відсутні"
                 show-empty
                 ref="table"
                 id="persons-table"
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

        <b-row>
            <b-col class="my-1 d-flex justify-content-end">
                <button class="btn btn-secondary"
                        @click="excelExport('persons-table', 'Особи', 'applications.xls', false)"
                        :disabled="isBusy"
                >Експорт у Excel</button>

                <button class="btn btn-primary ml-2"
                        @click="getItems(true)"
                        :disabled="isBusy"
                        v-if="isMoreBtnShowed">Завантажити ще</button>
            </b-col>
        </b-row>

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
    import ExcelMixin from './../../mixins/ExcelMixin';

    export default {
        props: ['region', 'obj_type', 'legal_type', 'dateFrom', 'dateTo'],
        mixins: [ExcelMixin],
        data() {
            return {
                isBusy: true,
                fields: [
                    {key: 'full_name', label: 'ФІО/назва заявника'},
                    {key: 'total_claims', label: 'Кількість поданих заяв'},
                    {key: 'budget_enrolled', label: 'Зараховані кошти'},
                    {key: 'budget_not_enrolled', label: 'Незараховані кошти'},
                ],
                totalRows: 1,
                currentPage: 1,
                perPage: 10,
                items: [],
                loadMorePressed: false,
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
            currentPage() {
                if (!this.loadMorePressed) {
                    this.getItems();
                }
            }
        },
        mounted() {
            this.getItems();
        },
        computed: {
            isMoreBtnShowed() {
                return this.totalRows > this.currentPage * this.perPage;
            }
        },
        methods: {
            refreshTable() {
                this.items = [];
                this.loadMorePressed = 0;
                this.totalRows = 1;
                this.currentPage = 1;
                this.getItems();
            },

            // Получение списка заявок с сервера
            getItems(more=false) {
                this.isBusy = true;
                if (more) {
                    this.loadMorePressed = true;
                    this.currentPage++;
                }

                axios.get('/api/statistics/regions_persons/', {
                    params: {
                        date_from: this.dateFrom.toISOString().split('T')[0],
                        date_to: this.dateTo.toISOString().split('T')[0],
                        region: this.region,
                        obj_type: this.obj_type,
                        legal_type: this.legal_type,
                        page: this.currentPage,
                    }
                }).then((response) => {
                    this.totalRows = response.data.count;

                    if (more) {
                        let items = response.data.results || [];
                        this.items.push(...items);

                    } else {
                        this.items = response.data.results || [];
                    }

                    this.isBusy = false;
                    this.loadMorePressed = false;
                    this.$nextTick(function () {
                        window.scrollTo(0,document.body.scrollHeight);
                    });
                });
            }
        }
    }
</script>

<style>
</style>