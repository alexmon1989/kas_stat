<template>
    <div>
        <b-table :items="items"
                 :fields="fields"
                 :busy="isBusy"
                 striped
                 responsive="sm"
                 empty-text="Заявки відсутні"
                 show-empty
                 ref="table"
                 id="applications-table"
        >
            <template v-slot:table-busy>
                <div class="text-center my-2">
                    <b-spinner class="align-middle"></b-spinner>
                    <strong>Завантаження даних...</strong>
                </div>
            </template>

            <template v-slot:cell(app_number)="row">
                <a href="#" @click.prevent="row.toggleDetails">{{ row.item.claim_number || '-' }}</a>
            </template>

            <template v-slot:cell(subject)="row">
                {{ getPerson(row.item) }}
            </template>

            <template v-slot:cell(object)="row">
                {{ getObject(row.item) }}
            </template>

            <template v-slot:row-details="row">
                <app-details :app="row.item"></app-details>
            </template>
        </b-table>

        <b-row>
            <b-col class="my-1 d-flex justify-content-end">
                <button class="btn btn-secondary"
                        @click="excelExport('applications-table', 'Заявки', 'applications.xls', false)"
                        :disabled="isBusy"
                ><i class="fa fa-file-excel-o mr-2"></i>Експорт у Excel</button>

                <button class="btn btn-primary ml-2"
                        @click="getItems(true)"
                        :disabled="isBusy"
                        v-if="isMoreBtnShowed"><i class="mr-2 fa fa-refresh"></i>Завантажити ще</button>
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
    import AppDetails from './AppDetails.vue';
    import ExcelMixin from './../../mixins/ExcelMixin';

    export default {
        props: ['appType', 'objType', 'dateFrom', 'dateTo'],
        mixins: [ExcelMixin],
        components: {
            AppDetails
        },
        data() {
            return {
                isBusy: true,
                fields: [
                    {key: 'app_number', label: '№ заявки'},
                    {key: 'subject', label: ''},
                    {key: 'object', label: ''},
                ],
                totalRows: 1,
                currentPage: 1,
                perPage: 10,
                items: [],
                loadMorePressed: false,
            }
        },
        watch: {
            appType() {
                this.refreshTable();
            },
            objType() {
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
                if (this.appType === 'claims_ap' || this.appType === 'registrations_ap') {
                    this.fields[1]['label'] = 'Суб\'єкт АП, який подає заявку';
                    this.fields[2]['label'] = 'Об\'єкт(и) АП, на які передаються права';
                } else {
                    this.fields[1]['label'] = 'Сторона договору, яка подає заявку';
                    this.fields[2]['label'] = 'Об\'єкт АП';
                }
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

                axios.get('/api/obj_types_claims/', {
                    params: {
                        appType: this.appType,
                        objType: this.objType,
                        date_from: this.dateFrom.toISOString().split('T')[0],
                        date_to: this.dateTo.toISOString().split('T')[0],
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
            },

            getPerson(app) {
                if (!app.persons.length) {
                    return '-';
                }
                return app.persons[0]['full_name'];
            },

            getObject(app) {
                if (!app.oap.length) {
                    return '-';
                }
                return app.oap.map(function (item) {
                    return item.oap_name
                }).join('; ')
            }
        }
    }
</script>